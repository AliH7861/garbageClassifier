# For each table and column, we specify the input type (e.g., Integer, String, DateTime).
# This ensures our functions and API endpoints can easily handle, validate, and return
# the correct data types, allowing the backend and frontend to work together smoothly.


from pydantic import BaseModel
from datetime import datetime, date, time

class TestingTableBase2(BaseModel):
    predicted_bin: str
    predicted_class: str
    time: time
    date: date


class SubmissionDataBase(BaseModel):
    id: int
    time: time
    date: date
    Bin: str
    Class: str

    class Config:
        orm_mode = True


class NumberedDataBase(BaseModel):
    id: int
    date: date
    
    todayScannedItem: int
    mostScannedBinToday: str
    totalGreenBinScan: int
    totalLightBlueBinScan: int
    totalGarbageBinScan: int
    totalDarkBlueBinScan: int

    class Config:
        orm_mode = True

class ClassDataBase(BaseModel):
    id: int
    date: date
    plasticCount: int
    metalCount: int
    trashCount: int
    cardBoardCount: int
    shoesCount: int
    brownClassCount: int
    whiteGlassCount: int
    greenClassCount: int
    biologicalCount: int
    clothesCount: int
    paperCount: int
    mostCommonClass:str

    class Config:
        orm_mode = True


# Creating 4th Table
class TableDataBase(BaseModel):
    id: int
    date_time: datetime
    predicted_bin: str
    predicted_class: str

    class Config:
        orm_mode = True

# Creating 5th Table
class ScanningRateDataBase(BaseModel):
    id: int
    date: date
    dailyScan: int
    scanningRate: float

    class Config:
        orm_mode = True

# Creating 5th Table
class userIdCreateDataBase(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class userIdReadDataBase(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


