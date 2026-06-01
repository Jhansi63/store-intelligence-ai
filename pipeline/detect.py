import sys
import cv2
import uuid
import sqlite3

from ultralytics import YOLO
from datetime import datetime

# -----------------------------
# LOAD YOLO MODEL
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# VIDEO PATH
# -----------------------------
video_path = sys.argv[1]

cap = cv2.VideoCapture(video_path)

# -----------------------------
# SQLITE DATABASE
# -----------------------------
conn = sqlite3.connect("store.db")
cursor = conn.cursor()

# -----------------------------
# TRACK COUNTED VISITORS
# -----------------------------
counted_visitors = set()

# -----------------------------
# FRAME CONTROL
# -----------------------------
frame_count = 0
max_frames = 100

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # Stop after limited frames
    if frame_count > max_frames:
        break

    # Skip frames for speed
    if frame_count % 5 != 0:
        continue

    # Resize frame for faster inference
    frame = cv2.resize(frame, (640, 360))

    # -----------------------------
    # YOLO TRACKING
    # -----------------------------
    results = model.track(
        frame,
        persist=True,
        verbose=False
    )[0]

    # -----------------------------
    # CHECK TRACK IDS
    # -----------------------------
    if results.boxes.id is not None:

        boxes = results.boxes.xyxy.cpu().numpy()
        ids = results.boxes.id.cpu().numpy()

        for box, track_id in zip(boxes, ids):

            x1, y1, x2, y2 = box

            visitor_id = f"VISITOR_{int(track_id)}"

            # -----------------------------
            # DRAW BOUNDING BOX
            # -----------------------------
            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )

            # -----------------------------
            # DRAW TRACK ID
            # -----------------------------
            cv2.putText(
                frame,
                visitor_id,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # -----------------------------
            # SAVE ONLY ONCE
            # -----------------------------
            if visitor_id not in counted_visitors:

                counted_visitors.add(visitor_id)

                event = {
                    "event_id": str(uuid.uuid4()),
                    "store_id": "STORE_BLR_002",
                    "camera_id": "CAM_ENTRY_01",
                    "visitor_id": visitor_id,
                    "event_type": "ENTRY",
                    "timestamp": datetime.utcnow().isoformat(),
                    "zone_id": "ENTRY_GATE",
                    "dwell_ms": 0,
                    "is_staff": False,
                    "confidence": 0.95
                }

                cursor.execute(
                    '''
                    INSERT INTO events (
                        event_id,
                        store_id,
                        camera_id,
                        visitor_id,
                        event_type,
                        timestamp,
                        zone_id,
                        dwell_ms,
                        is_staff,
                        confidence
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        event["event_id"],
                        event["store_id"],
                        event["camera_id"],
                        event["visitor_id"],
                        event["event_type"],
                        event["timestamp"],
                        event["zone_id"],
                        event["dwell_ms"],
                        event["is_staff"],
                        event["confidence"]
                    )
                )

                conn.commit()

    # -----------------------------
    # SHOW VIDEO
    # -----------------------------
    cv2.imshow("Store Intelligence Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -----------------------------
# CLEANUP
# -----------------------------
cap.release()
conn.close()
cv2.destroyAllWindows()