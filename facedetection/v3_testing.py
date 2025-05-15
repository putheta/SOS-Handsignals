import os
import cv2
import face_recognition
import mediapipe as mp
import numpy as np

def process_face_image(image_path: str):
    # ตรวจสอบว่าไฟล์ภาพมีอยู่จริง
    if not os.path.exists(image_path):
        print(f"❌ ไม่พบไฟล์ภาพ: {image_path}")
        return

    # โหลดภาพและแปลงเป็น RGB
    frame = cv2.imread(image_path)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # โหลดใบหน้าที่รู้จัก
    known_encodings = []
    known_names = []

    known_faces_dir = os.path.join(os.path.dirname(__file__), "known_faces")
    if not os.path.exists(known_faces_dir):
        print("⚠️ ไม่พบโฟลเดอร์ 'known_faces'")
    else:
        for filename in os.listdir(known_faces_dir):
            if filename.endswith(".jpg"):
                print(f"กำลังโหลด: {filename}")
                image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_encodings.append(encodings[0])
                    known_names.append(os.path.splitext(filename)[0])

    # ใช้ MediaPipe ตรวจจับใบหน้า
    mp_face_detection = mp.solutions.face_detection
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
        result = detector.process(rgb)

        if result.detections:
            for det in result.detections:
                bbox = det.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                x2 = int((bbox.xmin + bbox.width) * w)
                y2 = int((bbox.ymin + bbox.height) * h)

                # ครอปใบหน้าแล้วหาค่า encoding
                face_crop = rgb[y1:y2, x1:x2]
                face_encoding = face_recognition.face_encodings(face_crop)

                if face_encoding:
                    matches = face_recognition.compare_faces(known_encodings, face_encoding[0])
                    face_distances = face_recognition.face_distance(known_encodings, face_encoding[0])
                    best_match_index = np.argmin(face_distances)

                    name = "Unknown"
                    if matches and matches[best_match_index]:
                        name = known_names[best_match_index]

                    # วาดกรอบใบหน้าและชื่อ
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    
                    return name
                else:
                    print("❌ ไม่พบ encoding ของใบหน้า")
                    return name
        else:
            print("😕 ไม่เจอใบหน้าในภาพ")

    # แสดงผลลัพธ์
    cv2.imshow("Result", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return None
