from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)

    person_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])

            if cls == 0:   # person class
                person_count += 1

    frame = results[0].plot()

    cv2.putText(
        frame,
        f"Persons: {person_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("SAMYAKAVLOKAN AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()