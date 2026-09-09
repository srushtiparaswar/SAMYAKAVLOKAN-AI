from ultralytics import YOLO
import cv2
import sqlite3

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found!")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)

    person_count = 0
    object_counts = {}

    for r in results:
        for box in r.boxes:

            conf = float(box.conf[0])

            if conf < 0.60:
                continue

            cls = int(box.cls[0])

            class_name = model.names[cls]

            if class_name == "person":
                person_count += 1
            else:
                object_counts[class_name] = object_counts.get(class_name, 0) + 1

    frame = results[0].plot()

    cv2.putText(
        frame,
        f"Persons: {person_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    y = 80

    for obj, count in object_counts.items():
        cv2.putText(
            frame,
            f"{obj}: {count}",
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )
        y += 30

    # DATABASE UPDATE
    total_objects = sum(object_counts.values())

    conn = sqlite3.connect("samyakavlokan.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM live_stats")

    cursor.execute("""
    INSERT INTO live_stats(person_count, object_count)
    VALUES (?, ?)
    """, (person_count, total_objects))

    conn.commit()
    conn.close()

    cv2.imshow("SAMYAKAVLOKAN AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()