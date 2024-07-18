import cv2

cap = cv2.VideoCapture('rtsp://admin:KGMJLP@103.167.31.202:554/H.264')

if not cap.isOpened():
    print("Error: Could not open video stream")
else:
    print("Connected to the stream successfully")

while True:
    # Baca frame dari stream
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Tampilkan frame
    cv2.imshow('RTSP Stream', frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()