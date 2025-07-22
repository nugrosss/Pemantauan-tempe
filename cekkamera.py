import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Kamera tidak bisa dibuka")
else:
    ret, frame = cap.read()
    if ret:
        print("Berhasil ambil frame")
        cv2.imwrite("test.jpg", frame)
    else:
        print("Gagal ambil frame")
cap.release()

# import cv2
# import time
# from ultralytics import YOLO

# # Load model
# model = YOLO("/home/pi/nabila nadia/progam baru /Pemantauan-tempe/best.pt")

# # Buka kamera (0 untuk kamera default)
# cap = cv2.VideoCapture(0)

# # Cek apakah kamera berhasil dibuka
# if not cap.isOpened():
#     print("❌ Tidak dapat membuka kamera.")
#     exit()

# # Loop untuk membaca frame dari kamera
# while True:
#     start_time = time.time()

#     ret, frame = cap.read()
#     if not ret:
#         print("❌ Gagal membaca frame.")
#         break

#     # Jalankan deteksi YOLO pada frame
#     results = model(frame, verbose=False)

#     # Ambil hasil anotasi
#     annotated_frame = results[0].plot()

#     # Hitung dan tampilkan FPS
#     end_time = time.time()
#     fps = 1 / (end_time - start_time)
#     cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#     # Tampilkan frame
#     cv2.imshow("YOLO Detection", annotated_frame)

#     # Tekan 'q' untuk keluar
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Bersihkan
# cap.release()
# cv2.destroyAllWindows()


