from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import traceback

from handdetection.version4 import detect_hand_sos
from facedetection.v3_testing import process_face_image

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
