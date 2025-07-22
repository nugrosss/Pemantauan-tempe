import cv2

# Buka kamera (0 biasanya untuk kamera utama)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Tidak bisa membuka kamera.")
    exit()

print("Tekan 's' untuk menyimpan gambar, atau 'q' untuk keluar.")

while True:
    # Ambil frame dari kamera
    ret, frame = cap.read()
    if not ret:
        print("❌ Gagal mengambil frame.")
        break

    # Tampilkan hasil frame
    cv2.imshow('Kamera', frame)

    # Tunggu input tombol
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        # Simpan frame sebagai file
        cv2.imwrite("gambar_disimpan.jpg", frame)
        print("✅ Gambar berhasil disimpan sebagai 'gambar_disimpan.jpg'")
    elif key == ord('q'):
        break

# Lepaskan kamera dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()
