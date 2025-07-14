import cv2

def cek_kamera():
    print("Mengecek kamera yang tersedia...\n")
    for i in range(2):  # Cek hingga 5 kamera (index 0 - 4)
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"[✔] Kamera tersedia di index {i}")
            else:
                print(f"[✘] Kamera di index {i} terbuka, tapi tidak mengirim frame")
            cap.release()
        else:
            print(f"[✘] Tidak ada kamera di index {i}")

if __name__ == "__main__":
    cek_kamera()
