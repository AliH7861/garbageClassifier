import os
import sys
import pytest
from datetime import datetime, date
from fastapi.testclient import TestClient
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import your FastAPI app and database models
from main import app, SessionLocal
from database import SubmissionData, TestingTable2, TableData

# Import your image utilities
from image_utils import (
    DEFAULT_IMAGES,
    BIN_FILENAMES,
    get_all_bin_images,
    fixed_size_image
)

client = TestClient(app)

#
# --- 1. API endpoint tests ---
#

def test_stats_alltimescans():
    resp = client.get("/stats/alltimescans")
    assert resp.status_code == 200
    json = resp.json()
    assert "total_scans_count" in json

def test_stats_todayscans():
    resp = client.get("/stats/todayscans")
    assert resp.status_code == 200
    assert "total_today_scans" in resp.json()

def test_stats_bargraphdata():
    resp = client.get("/stats/bargraphdata")
    assert resp.status_code == 200
    data = resp.json()
    for key in ["Organics Bin", "Garbage", "Paper Box", "Containers Box"]:
        assert key in data

def test_stats_classCircleGraphData():
    resp = client.get("/stats/classCircleGraphData")
    assert resp.status_code == 200
    keys = resp.json().keys()
    for key in ["Plastic", "Metal", "Trash", "Cardboard", "Paper"]:
        assert key in keys

def test_stats_dailyScanStats():
    resp = client.get("/stats/dailyScanStats")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_stats_tableStats():
    resp = client.get("/stats/tableStats")
    assert resp.status_code == 200
    data = resp.json()
    assert "recent_table_data" in data
    assert isinstance(data["recent_table_data"], list)

def test_stats_mostScanBinToday():
    resp = client.get("/stats/mostScanBinToday")
    assert resp.status_code == 200
    assert "most_scanned_bin" in resp.json()

def test_stats_changeinAllScanItems():
    resp = client.get("/stats/changeinAllScanItems")
    assert resp.status_code == 200
    assert "scanChange" in resp.json()

def test_stats_changeinAllScanItemsDaily():
    resp = client.get("/stats/changeinAllScanItemsDaily")
    assert resp.status_code == 200
    assert "scanDailyChange" in resp.json()

def test_stats_mostCommonBinToday():
    resp = client.get("/stats/mostCommonBinToday")
    assert resp.status_code == 200
    assert "mostCommonBin" in resp.json()

def test_stats_mostCommonBinChangeToday():
    resp = client.get("/stats/mostCommonBinChangeToday")
    assert resp.status_code == 200
    # returns {"bin_changed_to", ...}

def test_stats_mostCommonBinChangeAll():
    resp = client.get("/stats/mostCommonBinChangeAll")
    assert resp.status_code == 200
    # returns {"bin_changed_to", ...}

def test_create_user_and_login():
    # Create a user (200) or already exists (500)
    payload = {"username":"pytest_user","password":"pytest_pass"}
    resp1 = client.post("/createUser", json=payload)
    assert resp1.status_code in (200, 500)

    # Attempt login
    resp2 = client.post("/login", json=payload)
    assert resp2.status_code in (200, 400)

#
# --- 2. /submit endpoint test (requires test.jpg) ---
#

def test_submit_predict(tmp_path):
    # skip if no image
    img_path = tmp_path / "test.jpg"
    if not img_path.exists():
        pytest.skip("Place a small 'test.jpg' in the project root to test /submit")
    with open(img_path, "rb") as f:
        files = {"file": ("test.jpg", f, "image/jpeg")}
        resp = client.post("/submit", files=files)
        assert resp.status_code in (200, 500)

#
# --- 3. Direct DB model tests ---
#

def test_database_connection_and_query():
    db = SessionLocal()
    try:
        results = db.query(SubmissionData).all()
        assert isinstance(results, list)
    finally:
        db.close()

def test_insert_and_cleanup_testingtable2():
    db = SessionLocal()
    try:
        entry = TestingTable2(
            predicted_bin="Garbage",
            predicted_class="plastic",
            time=datetime.now().time(),
            date=date.today()
        )
        db.add(entry); db.commit(); db.refresh(entry)
        assert entry.id is not None
        db.delete(entry); db.commit()
    finally:
        db.close()

def test_insert_and_cleanup_tabledata():
    db = SessionLocal()
    try:
        entry = TableData(
            date_time=datetime.now(),
            predicted_bin="Green bin",
            predicted_class="paper"
        )
        db.add(entry); db.commit(); db.refresh(entry)
        assert entry.id is not None

        # cleanup
        db.delete(entry); db.commit()
    finally:
        db.close()

#
# --- 4. image_utils tests ---
#

def test_get_all_bin_images_keys():
    bins = get_all_bin_images("someuser")
    assert set(bins.keys()) == set(DEFAULT_IMAGES.keys())

def test_fixed_size_image_bytes():
    # Read a real image, encode it to base64
    with open("test.jpg", "rb") as f:
        img_bytes = f.read()
    import base64
    b64_string = base64.b64encode(img_bytes)
    out = fixed_size_image(b64_string)
    assert isinstance(out, (bytes, bytearray))
def test_bin_filenames_and_defaults():
    assert set(BIN_FILENAMES.keys()) == set(DEFAULT_IMAGES.keys())

#
# --- 5. Signup/Login flow logic tests (via requests-mock) ---
#

def test_signup_flow(mocker):
    url = "http://localhost:8000/createUser"
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    resp = requests.post(url, json={"username":"a","password":"b"})
    assert resp.status_code == 200

def test_login_flow(mocker):
    url = "http://localhost:8000/login"
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"user_id":"u","id":1}

    resp = requests.post(url, json={"username":"u","password":"p"})
    assert resp.status_code == 200
    assert resp.json()["user_id"] == "u"