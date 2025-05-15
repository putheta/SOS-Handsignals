from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import traceback

from handdetection.version4 import detect_hand_sos
from facedetection.v3_testing import process_face_image

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from pydantic import BaseModel
from app.database import collection

router = APIRouter()

# -- เก็บการเชื่อมต่อ WebSocket
active_connections = []

@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("✅ WebSocket client connected")

    try:
        while True:
            data = await websocket.receive_text()
            print("📥 Received:", data)

            # ✅ broadcast ไปยัง client อื่น
            for conn in active_connections:
                if conn != websocket:
                    await conn.send_text(data)
    except WebSocketDisconnect:
        print("❌ WebSocket client disconnected")
        active_connections.remove(websocket)

# -------- SOS API --------

class SOSPayload(BaseModel):
    prediction: str
    confidence: float
    timestamp: str = None
    location: str = None
    image_url: str = None
    latitude: float = None
    longitude: float = None
    source: str = "user"

@router.post("/api/sos")
async def receive_sos(payload: SOSPayload):
    data = payload.dict()
    try:
        result = await collection.insert_one(data)
        return {"status": "received", "id": str(result.inserted_id)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/api/sos")
async def get_sos_all():
    sos_list = []
    async for doc in collection.find().sort("timestamp", -1):
        doc["_id"] = str(doc["_id"])
        sos_list.append(doc)
    return sos_list

@router.delete("/api/sos/{id}")
async def delete_sos(id: str):
    try:
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"status": "deleted"}
        return JSONResponse(status_code=404, content={"status": "not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

app = FastAPI()

# Mount static folder (สำคัญมากเพื่อให้รูปโหลดได้)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template path
project_root = os.path.abspath(os.path.dirname(__file__))
template_path = os.path.join(project_root, "template")
templates = Jinja2Templates(directory=template_path)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        # เรียกฟังก์ชันทุกครั้งที่รีเฟรช
        abs_path, location, full_time = detect_hand_sos()
        name = process_face_image(abs_path)

        # ตัด string เวลา
        full_time = str(full_time)
        date = full_time[:10]
        time = full_time[11:19]

        # แปลง absolute path -> URL path
        split_index = abs_path.lower().find("static")
        if split_index == -1:
            raise ValueError("Static path not found in image path.")
        url_path = "/" + abs_path[split_index:].replace("\\", "/")

        data = {
            "name": name,
            "date": date,
            "time": time,
            "location": location,
            "path": url_path
        }

        return templates.TemplateResponse("index.html", {"request": request, "data": data})

    except Exception as e:
        print("🔥 ERROR OCCURRED 🔥")
        traceback.print_exc()
        return HTMLResponse(
            content=f"<h1>❌ Internal Server Error</h1><pre>{e}</pre>", status_code=500
        )
