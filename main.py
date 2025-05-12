from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from bson import ObjectId
import os

# โหลด environment variables
load_dotenv()

# สร้าง FastAPI app
app = FastAPI()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["sos_database"]
collection = db["sos_alerts"]

# ติดตั้ง static และ template
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# โมเดลรับข้อมูล
class SOSPayload(BaseModel):
    prediction: str
    confidence: float
    timestamp: str = None
    location: str = None
    image_url: str = None
    latitude: float = None
    longitude: float = None

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# ROUTES

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

@app.post("/api/sos")
async def receive_sos(payload: SOSPayload):
    data = payload.dict()
    print("✅ PAYLOAD RECEIVED:", data)

    try:
        result = await collection.insert_one(data)
        print("✅ INSERTED ID:", result.inserted_id)
    except Exception as e:
        print("❌ INSERT ERROR:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

    if payload.prediction.lower() == "sos" and payload.confidence > 0.9:
        await manager.broadcast(f"SOS Detected! Confidence: {payload.confidence}")

    return {"status": "SOS received", "id": str(result.inserted_id)}

@app.get("/api/sos/history")
async def get_sos_history():
    sos_list = []
    async for doc in collection.find().sort("timestamp", -1):
        doc["_id"] = str(doc["_id"])
        sos_list.append(doc)
    return JSONResponse(content=sos_list)

@app.delete("/api/sos/{id}")
async def delete_sos(id: str):
    try:
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"status": "deleted"}
        return JSONResponse(status_code=404, content={"status": "not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # เพื่อไม่ให้ connection หลุด
    except WebSocketDisconnect:
        manager.disconnect(websocket)