from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from tensorflow import keras
from PIL import Image as PILImage
import numpy as np
import io
from database import SessionLocal, TestingTable2, SubmissionData, NumberedData, ClassData, TableData, DailyStatsData, UserIdData
from schemas import TestingTableBase2, SubmissionDataBase, NumberedDataBase, ClassDataBase, TableDataBase, ScanningRateDataBase, userIdCreateDataBase, userIdReadDataBase
from datetime import date, datetime, timedelta, time
from zoneinfo import ZoneInfo
from sqlalchemy import func, desc
import hashlib
from sqlalchemy.orm import Session 
import requests
import os
app = FastAPI()


MODEL_PATH = "my_model.keras"
MODEL_URL = "https://github.com/AliH7861/garbageClassifier/releases/download/v1.0/my_model.keras"  

def download_model_if_missing():
    if not os.path.exists(MODEL_PATH):
        print(f"Model file not found at {MODEL_PATH}. Downloading from {MODEL_URL} ...")
        response = requests.get(MODEL_URL, stream=True)
        if response.status_code == 200:
            with open(MODEL_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Model downloaded successfully.")
        else:
            raise RuntimeError(f"Failed to download model! Status code: {response.status_code}")

# Download model if it's not present
download_model_if_missing()

# Now import and load
resnet_model = keras.models.load_model(MODEL_PATH)


# load information about the model
import json

# Load your config file
with open("model_config.json", "r") as f:
    config = json.load(f)

# Print everything to verify
img_height = config["img_height"]
img_width = config["img_width"]
class_names = config["class_names"]
class_to_bin = config["class_to_bin"]
bin_to_pic = config["bin_to_pic"]

# Setup a Dependency to get a Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



async def predictImage(file, img_height, img_width, resnet_model, class_names, class_to_bin, bin_to_pic):   
    img_bytes = await file.read() 
    
    # Get the Time and Date
    now_local = datetime.now(ZoneInfo("America/Toronto")).replace(microsecond=0)
   
    just_date = now_local.date()
    just_time = now_local.time().replace(microsecond=0)  # Remove microseconds for clarity

    # Opens the image using PIL, and converts the image into RGB mode
    img = PILImage.open(io.BytesIO(img_bytes)).convert("RGB")
    # Resizes the img to default image height and width
    img = img.resize((img_height, img_width))

    # Convert the image into an array
    image_array = np.array(img)

    # adds an dim, to let the model know the batch size
    image_array = np.expand_dims(image_array, axis=0)

    # 2. PREDICT:
    # Tells the trained model to make an prediction on the input image
    pred = resnet_model.predict(image_array)

    # argmax, gives you the index of highest value in pred
    predicted_class = class_names[np.argmax(pred)]

    # Maps the predicted class to the bin names, and if the predicted class isn't mapped it writes unknown
    predicted_bin = class_to_bin.get(predicted_class, 'Unknown')

    # Maps the predicted class with the images
    predicted_image = bin_to_pic.get(predicted_bin, 'Unknown')


    # Print out the text and image of the prediction
    return {
        "class": predicted_class,
        "bin": predicted_bin, 
        "time": just_time,
        "date": just_date,
        "dateandtime": now_local,
        "bin_image": predicted_image,
        "confidence": float(np.max(pred)),
    }

# def percent_change
def percent_change(current, previous):
    if previous == 0:
        if current == 0:
            return 0.0    # No change at all
        else:
            return None   # Or float('inf'), or 'undefined', as you wish
    return ((current - previous) / previous) * 100



@app.post("/submit")
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        result = await predictImage(
            file, img_height, img_width, 
            resnet_model, class_names, class_to_bin, bin_to_pic
        )


        # saving the data into the database
        
        testingbase = TestingTable2(
            predicted_class=result["class"],
            predicted_bin=result["bin"],
            time =result["time"],
            date = result["date"]
        )

        submissionbase = SubmissionData(
            Class=result["class"],
            Bin=result["bin"],
            time =result["time"],
            date = result["date"]
        )

        db.add(submissionbase)
        db.commit()
        db.refresh(submissionbase)

        today = result["date"]
        # List of queries from submission base
        items_scanned_today = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today).scalar()
        mostbin_scanned_today = db.query(SubmissionData.Bin, func.count(SubmissionData.id).label("bin_count")).filter(SubmissionData.date == today).group_by(SubmissionData.Bin).order_by(desc("bin_count")).first()
        greenbinCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Bin == "Green bin").scalar()
        lightblueCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Bin == "Light blue box").scalar()
        garbageCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Bin == "Black garbage").scalar()
        darkblueCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Bin == "Dark blue box").scalar()
        
        if mostbin_scanned_today:
            mostBinName = mostbin_scanned_today[0]
        else:
            mostBinName = "N/A"

        # Create a predicted_bin switch statement to +1 everytime, the predicted_bin is used
        numberedbase = NumberedData (
            date = result["date"],
            todayScannedItem = items_scanned_today,
            mostScannedBinToday = mostBinName,
            totalGreenBinScan = greenbinCount, 
            totalLightBlueBinScan = lightblueCount,
            totalGarbageBinScan = garbageCount,
            totalDarkBlueBinScan = darkblueCount 
        )

        # List of queries for Class
        plasticCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "plastic").scalar()
        metalCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "metal").scalar()
        trashCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "trash").scalar()
        cardBoardCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "cardboard").scalar()
        shoesCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "shoes").scalar()
        brownClassCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "brown-glass").scalar()
        whiteGlassCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "white-glass").scalar()
        greenClassCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "green-glass").scalar()
        biologicalCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "biological").scalar()
        clothesCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "clothes").scalar()
        paperCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "paper").scalar()
        mostCommonClassName = db.query(SubmissionData.Class, func.count(SubmissionData.id).label("class_count")).filter(SubmissionData.date == today).group_by(SubmissionData.Class).order_by(desc("class_count")).first()


        if mostCommonClassName:
            commonClass = mostCommonClassName[0]
        else:
            commonClass = "N/A"  # or "No Data"

        classbase = ClassData (
            date = result["date"],
            plasticCount = plasticCount,
            metalCount = metalCount,
            trashCount = trashCount,
            cardBoardCount = cardBoardCount,
            shoesCount = shoesCount,
            brownClassCount = brownClassCount,
            whiteGlassCount = whiteGlassCount,
            greenClassCount = greenClassCount,
            biologicalCount = biologicalCount,
            clothesCount = clothesCount,
            paperCount = paperCount,
            mostCommonClass = commonClass
        )

        # List of Queries for Table data

        tablebase = TableData(
         date_time = result["dateandtime"],
         predicted_class = result["class"],
         predicted_bin = result["bin"]
        )

        # List of Queries for daily rate
        todayScanValue = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today).scalar()

        yesterday = today - timedelta(days=1)
        yesterdayScanValue = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == yesterday).scalar()

        if yesterdayScanValue != 0:
            differenceRate = ((todayScanValue - yesterdayScanValue) / yesterdayScanValue) * 100
        else:
            differenceRate = 0 

        dailyratebase = DailyStatsData (
            date = result["date"],
            dailyScan = todayScanValue,
            scanningRate = differenceRate
        )



        db.add_all([testingbase, numberedbase, classbase, tablebase, dailyratebase])
        db.commit()
        for obj in [testingbase, numberedbase, classbase, tablebase, dailyratebase]:
            db.refresh(obj)

        return result
    except Exception as e:
        print("Prediction error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

    

# Get Request for Items Scanned All Time
@app.get("/stats/alltimescans")
async def total_scans(db: Session = Depends(get_db)):
    total_scans_count = db.query(SubmissionData).count()
    
    result = db.query(
        SubmissionData.Bin,
        func.count(SubmissionData.id).label("bin_count")
    ).group_by(SubmissionData.Bin)\
     .order_by(desc("bin_count"))\
     .first()
    
    if result:
        return {
            "total_scans_count": total_scans_count,
            "mostCommonBin": result[0],    # The bin name (string)
            "binCount": result[1]          # The count (integer)
        }
    else:
        return {
            "total_scans_count": total_scans_count,
            "mostCommonBin": None,
            "binCount": 0
        }
   

# Get Request for Items Scanned Today
@app.get("/stats/todayscans")
async def today_scans(db: Session = Depends(get_db)):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    total_today_scans = db.query(SubmissionData).filter(
        SubmissionData.date >= today,
        SubmissionData.date < tomorrow
    ).count()
    return {
        "total_today_scans": total_today_scans
    }


# Get Request For Bar Graph and Pie Graph
@app.get("/stats/bargraphdata")
async def bargraph_data(db: Session = Depends(get_db)):
    today = date.today()
    todayGreenBinCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Bin == "Green bin").scalar()
    todayGarbageBinCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Bin == "Black garbage").scalar()
    todayLightBlueBinCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Bin == "Light blue box").scalar()
    todayDarkBlueBinCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Bin == "Dark blue box").scalar()
    return {
        "Organics Bin": todayGreenBinCount,
        "Garbage": todayGarbageBinCount,
        "Paper Box": todayLightBlueBinCount,
        "Containers Box": todayDarkBlueBinCount 
    }

# Get Request For Circle Graph
@app.get("/stats/classCircleGraphData")
async def circleClass_data(db: Session = Depends(get_db)):
    today = date.today()
    todayplasticCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "plastic").scalar()
    todaymetalCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "metal").scalar()
    todayTrashCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "trash").scalar()
    todayCardboardCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "cardboard").scalar()
    todayShoesCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "shoes").scalar()
    todaybrownglassCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "brown-glass").scalar()
    todaywhiteglassCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "white-glass").scalar()
    todaygreenglassCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "green-glass").scalar()
    todaybiologicalCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "biological").scalar()
    todayclothesCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "clothes").scalar()
    todaypaperCount = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today, SubmissionData.Class == "paper").scalar()
    return {
       "Plastic": todayplasticCount,
       "Metal": todaymetalCount,
       "Trash": todayTrashCount,
       "Cardboard": todayCardboardCount,
       "Shoes": todayShoesCount,
       "Brown-glass": todaybrownglassCount,
       "White-glass": todaywhiteglassCount,
       "Green-glass": todaygreenglassCount,
       "Biological": todaybiologicalCount,
       "Clothes": todayclothesCount,
       "Paper": todaypaperCount
       

   }

# Get Request for Daily Scans 
@app.get("/stats/dailyScanStats")
async def dailyScan_data(db: Session = Depends(get_db)):
    results = (
        db.query(DailyStatsData.date, func.max(DailyStatsData.dailyScan).label("scan_count"))
        .group_by(DailyStatsData.date)
        .order_by(DailyStatsData.date)
        .all()
    )

    return [
        {
            "date": r[0].strftime("%Y-%m-%d"),  # Convert to string
            "scan_count": r[1]
        }
        for r in results
    ]

# Get Request for the Table
@app.get("/stats/tableStats")
async def tableData(db: Session = Depends(get_db)):
    results = (
        db.query(TableData)
        .order_by(TableData.date_time.desc())
        .limit(7)
        .all()
    )

    BIN_MAPPING = {
    "Green bin": "Organics Bin",
    "Black garbage": "Garbage",
    "Dark blue box": "Containers Box",
    "Light blue box": "Paper Box"
}
    
    CLASS_MAPPING  = {
        "biological": "Biological",
        "brown-glass": "Brownglass",
        "cardboard": "Cardboard",
        "green-glass": "Greenglass",
        "metal": "Metal",
        "paper": "Paper",
        "plastic": "Plastic",
        "shoes": "Shoes",
        "trash": "Trash",
        "white-glass": "Whiteglass",
        "clothes": "Clothes",
    }
         
         

    # Convert results to list of dicts with required fields
    data = [
        {
            "date_time": row.date_time,
            "predicted_class": CLASS_MAPPING.get(row.predicted_class, row.predicted_class),
            "predicted_bin": BIN_MAPPING.get(row.predicted_bin, row.predicted_bin)
        }
        for row in results
    ]

    return {"recent_table_data": data}

# Request for Most Scanned Bin Today
@app.get("/stats/mostScanBinToday")
async def mostScannedBin(db: Session = Depends(get_db)):
    today = date.today()
    results = (
        db.query(SubmissionData.Bin, func.count(SubmissionData.id).label("bin_count")).filter(SubmissionData.date == today).group_by(SubmissionData.Bin).order_by(desc("bin_count")).first()
    )

    if results:
        bin_name, bin_count = results
        return {
            "most_scanned_bin": bin_name,
            "bin_count": bin_count
        }
    else:
        return {
            "most_scanned_bin": None,
            "bin_count": 0
        }
    

# Change Between Upto Yesterday, and Between Scans Upto Today
@app.get("/stats/changeinAllScanItems")
async def mostScannedBin(db: Session = Depends(get_db)):
    today = date.today()
    yesterday = today - timedelta(days=1)

    # All-time up to today
    today_total = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date <= today).scalar()
    # All-time up to yesterday
    yesterday_total = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date <= yesterday).scalar()

    # Percentage change calculation
    if yesterday_total == 0:
        scan_change = 0 if today_total == 0 else 100  # 0 if no scans at all, 100% if scans started today
    else:
        scan_change = ((today_total - yesterday_total) / yesterday_total) * 100

    return {"scanChange": round(scan_change, 2)}


# Change Between Yesterday and Today Scanned Items of Daily Scanning
@app.get("/stats/changeinAllScanItemsDaily")
async def mostScannedBin(db: Session = Depends(get_db)):
    today = date.today()
    yesterday = today - timedelta(days=1)

    today_count = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == today).scalar()
    yesterday_count = db.query(func.count(SubmissionData.id)).filter(SubmissionData.date == yesterday).scalar()

    if yesterday_count == 0:
        scan_change = 0 if today_count == 0 else 100  # 0 if no scans either day, 100% if scans started today
    else:
        scan_change = ((today_count - yesterday_count) / yesterday_count) * 100

    return {"scanDailyChange": round(scan_change, 2)}


#Get Most Scanned Bin Today
@app.get("/stats/mostCommonBinToday")
async def mostCommonBinToday(db: Session = Depends(get_db)):
    today = date.today()
    result = db.query(
        SubmissionData.Bin,
        func.count(SubmissionData.id).label("bin_count")
    ).filter(SubmissionData.date == today)\
     .group_by(SubmissionData.Bin)\
     .order_by(desc("bin_count"))\
     .first()
    
    if result:
        return {
            "mostCommonBin": result[0],    # The bin name (string)
            "binCount": result[1]          # The count (integer)
        }
    else:
        return {
            "mostCommonBin": None,
            "binCount": 0
        }                   
   
#Get Change in Most Scan Bin
@app.get("/stats/mostCommonBinChangeToday")
async def mostCommonBinChangeToday(db: Session = Depends(get_db)):
      
    today = date.today()

    # Step 1: Get the latest submission TODAY
    latest_submission = db.query(SubmissionData)\
        .filter(SubmissionData.date == today)\
        .order_by(SubmissionData.id.desc())\
        .first()

    if not latest_submission:
        return {"message": "No submissions yet today."}

    latest_id = latest_submission.id

    # Step 2: Get most common bin for all today's submissions BEFORE the latest
    previous_row = db.query(
        SubmissionData.Bin,
        func.count(SubmissionData.id).label("bin_count")
    ).filter(
        SubmissionData.date == today,
        SubmissionData.id < latest_id
    ).group_by(SubmissionData.Bin)\
     .order_by(desc("bin_count"))\
     .first()

    # Step 3: Get most common bin for all today's submissions INCLUDING the latest
    current_row = db.query(
        SubmissionData.Bin,
        func.count(SubmissionData.id).label("bin_count")
    ).filter(
        SubmissionData.date == today,
        SubmissionData.id <= latest_id
    ).group_by(SubmissionData.Bin)\
     .order_by(desc("bin_count"))\
     .first()

    previous_bin = previous_row[0] if previous_row else None
    current_bin = current_row[0] if current_row else None

    if previous_bin and current_bin and previous_bin != current_bin:
        return {
            "bin_changed_to": current_bin,
            "previous_bin": previous_bin,
            "change": True
        }
    else:
        return {
            "bin_changed_to": current_bin or "No Data",
            "previous_bin": previous_bin or "No Data",
            "change": False
        }
      

   
#Get Change in Most Scan Bin
@app.get("/stats/mostCommonBinChangeAll")
async def mostCommonBinChangeAll(db: Session = Depends(get_db)):
     
     # Step 1: Get the latest submission (highest id or latest datetime)
    latest_submission = db.query(SubmissionData).order_by(SubmissionData.id.desc()).first()

    if not latest_submission:
        return {"message": "No submissions yet."}

    latest_id = latest_submission.id

    # Step 2: Get most common bin for all submissions BEFORE the latest
    previous_row = db.query(
        SubmissionData.Bin,
        func.count(SubmissionData.id).label("bin_count")
    ).filter(SubmissionData.id < latest_id)\
     .group_by(SubmissionData.Bin)\
     .order_by(desc("bin_count"))\
     .first()

    # Step 3: Get most common bin for all submissions INCLUDING the latest
    current_row = db.query(
        SubmissionData.Bin,
        func.count(SubmissionData.id).label("bin_count")
    ).filter(SubmissionData.id <= latest_id)\
     .group_by(SubmissionData.Bin)\
     .order_by(desc("bin_count"))\
     .first()

    previous_bin = previous_row[0] if previous_row else None
    current_bin = current_row[0] if current_row else None

    if previous_bin and current_bin and previous_bin != current_bin:
        return {
            "bin_changed_to": current_bin,
            "previous_bin": previous_bin,
            "change": True
        }
    else:
        return {
            "bin_changed_to": current_bin or "No Data",
            "previous_bin": previous_bin or "No Data",
            "change": False
        }

# User ID Endpoints

# POST REQUEST TO POST USER ID
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@app.post("/createUser")
async def add_user(user: userIdCreateDataBase, db: Session = Depends(get_db)):
    try:
        existing = db.query(UserIdData).filter(UserIdData.username == user.username).first()
        if not existing:
            hashed_pw = hash_password(user.password)
            user_record = UserIdData(username=user.username, password=hashed_pw)
            db.add(user_record)
            db.commit()
        user_count = db.query(UserIdData).count()
        return {"success": True, "user_id": user.username, "user_count": user_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/login")
async def login(user: userIdCreateDataBase, db: Session = Depends(get_db)):
    db_user = db.query(UserIdData).filter(UserIdData.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_pw = hash_password(user.password)
    if db_user.password != hashed_pw:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"success": True, "user_id": db_user.username, "id": db_user.id}


#Request to get the Username
@app.get("/user/{id}", response_model=userIdReadDataBase)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserIdData).filter(UserIdData.id == id).first()
    if user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user

