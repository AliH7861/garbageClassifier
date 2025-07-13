from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, MetaData, Time, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from zoneinfo import ZoneInfo
from datetime import datetime

now = datetime.now(ZoneInfo("America/Toronto"))
from dotenv import load_dotenv
load_dotenv("project.env")
import os
DATABASE_URL = os.getenv("DATABASE_URL")


# PostgreSQL
# Link to the database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# Creating TestingTable

class TestingTable2(Base):
    __tablename__ = "testing_table2"
    id = Column(Integer, primary_key=True, index=True) 
    predicted_bin =  Column(String)
    predicted_class =  Column(String)
    time = Column(Time)
    date = Column(Date) 


# Creating Table 1 (Index, Scanned Item Today, Time, Bin, Class, Most Scanned Bin)
class SubmissionData(Base):
    __tablename__ = 'Submission Data'
    id = Column(Integer, primary_key=True)
    time = Column(Time, index=True)
    date = Column(Date, index=True) 
    Bin = Column(String, index=True)
    Class = Column(String, index=True)

    # Find most Scan Bin from querying


# Creating Table 2 (Total Scans Today, Scans of Green Bin, Scans of LightBlue Bin, Scans of Garbage, Scans of DarkBlue Bin, Date)
class NumberedData(Base):
   __tablename__ = 'Graph Data'    
   id = Column(Integer, primary_key=True)
   date = Column(Date)
   todayScannedItem = Column(Integer)
   mostScannedBinToday = Column(String) 
   totalGreenBinScan = Column(Integer)
   totalLightBlueBinScan = Column(Integer)
   totalGarbageBinScan = Column(Integer)
   totalDarkBlueBinScan = Column(Integer)

# Creating Table 3(For Class Pie Chart)
class ClassData(Base):
    __tablename__ = 'Class Data'    
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    plasticCount = Column(Integer)
    metalCount = Column(Integer)
    trashCount = Column(Integer)
    cardBoardCount = Column(Integer)
    shoesCount = Column(Integer)
    brownClassCount = Column(Integer)
    whiteGlassCount = Column(Integer)
    greenClassCount = Column(Integer)
    biologicalCount = Column(Integer)
    clothesCount = Column(Integer)
    paperCount = Column(Integer)
    mostCommonClass = Column(Integer)


# Creating Table 4 for Panda Table
class TableData(Base):
    __tablename__ = 'Table Data'    
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    predicted_bin =  Column(String)
    predicted_class =  Column(String)

# Creating Table 5 for Scanning Rate
class DailyStatsData(Base):
    __tablename__ = 'Scanning Data'    
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    dailyScan = Column(Integer)
    scanningRate = Column(Float)

# Creating Table for UserId
class UserIdData(Base):
    __tablename__ = 'users_data'    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    password = Column(String(100)) 
    
# Creating Table 6 (Four Images, and Four Links - To Change Default Output Pictures)so 



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created!")



