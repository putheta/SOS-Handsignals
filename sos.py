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
