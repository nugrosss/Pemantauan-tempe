import cv2

cap = cv2.VideoCapture(0)  # 0 = kamera default (ubah ke 1 jika pakai USB eksternal)

if not cap.isOpened():
    print("Kamera tidak terdeteksi.")
else:
    print("Kamera berhasil dibuka.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal mengambil frame.")
            break

        cv2.imshow("Tampilan Kamera", frame)

        # Tekan tombol 'q' untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
