import cv2
import winsound

from event_logger import log_event, send_alert

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.putText(
        frame,
        "Press P for HELP Gesture",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("HELP Gesture Detection", frame)

    key = cv2.waitKey(1)

    if key == ord('p'):

        # Alarm Sound
        winsound.Beep(2500, 1000)

        # Save Event
        log_event(
            "HELP_GESTURE",
            1,
            "ACTIVE"
        )

        # Send Email
        send_alert()

        print("HELP ALERT SAVED + EMAIL SENT!")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()