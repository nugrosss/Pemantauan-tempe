import cv2
import os
import time
from datetime import datetime

# Inisialisasi kamera (0 untuk webcam default)
camera = cv2.VideoCapture(0)

# Cek apakah kamera berhasil dibuka
if not camera.isOpened():
    print("❌ Tidak dapat membuka kamera.")
    exit()

print("📸 Program mulai mengambil gambar tiap 1 menit...")

try:
    while True:
        # Dapatkan waktu sekarang
        now = datetime.now()
        folder_name = now.strftime("%Y-%m-%d_%H")  # Folder per jam
        filename = now.strftime("%Y-%m-%d_%H-%M-%S.jpg")  # Nama file per menit

        # Buat folder jika belum ada
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Ambil gambar dari kamera
        ret, frame = camera.read()
        if ret:
            filepath = os.path.join(folder_name, filename)
            cv2.imwrite(filepath, frame)
            print(f"✅ Gambar disimpan: {filepath}")
        else:
            print("⚠️ Gagal mengambil gambar.")

        # Tunggu 60 detik sebelum mengambil gambar berikutnya
        time.sleep(60)

except KeyboardInterrupt:
    print("\n🛑 Pengambilan gambar dihentikan oleh pengguna.")

finally:
    # Lepaskan kamera
    camera.release()
    print("🎥 Kamera dimatikan.")



