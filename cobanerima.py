import socket
import os
from datetime import datetime

# Konfigurasi folder
HOST = "0.0.0.0"
PORT = 5001
BASE_FOLDER = "upload_gambar"
HISTORY_FOLDER = os.path.join(BASE_FOLDER, "history")
LATEST_FOLDER = os.path.join(BASE_FOLDER, "terbaru")

# Buat folder jika belum ada
os.makedirs(HISTORY_FOLDER, exist_ok=True)
os.makedirs(LATEST_FOLDER, exist_ok=True)

def receive_exact(sock, size):
    buffer = b''
    while len(buffer) < size:
        chunk = sock.recv(min(4096, size - len(buffer)))
        if not chunk:
            raise ConnectionError("Koneksi terputus saat menerima data.")
        buffer += chunk
    return buffer

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"[SERVER] Listening di port {PORT}...")

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"\n[CONNECTED] Dari {addr}")

        try:
            jumlah_file = int(client_socket.recv(1024).decode())
            client_socket.send(b"ACK")

            for _ in range(jumlah_file):
                filename = client_socket.recv(1024).decode()
                client_socket.send(b"ACK")

                filesize = int(client_socket.recv(1024).decode())
                client_socket.send(b"ACK")

                if "_" in filename:
                    save_path = os.path.join(HISTORY_FOLDER, filename)
                else:
                    save_path = os.path.join(LATEST_FOLDER, filename)

                print(f"[RECEIVING] {filename} ({filesize} bytes)")
                with open(save_path, "wb") as f:
                    data = receive_exact(client_socket, filesize)
                    f.write(data)

                print(f"[SAVED] {save_path}")

                # Tulis timestamp
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if "bagus" in filename.lower():
                    waktu_file = os.path.join(LATEST_FOLDER, "waktu_bagus.txt")
                elif "jelek" in filename.lower():
                    waktu_file = os.path.join(LATEST_FOLDER, "waktu_jelek.txt")
                else:
                    waktu_file = None

                if waktu_file:
                    with open(waktu_file, "w") as wf:
                        wf.write(waktu_sekarang)
                    print(f"[WAKTU DICATAT] {waktu_file} = {waktu_sekarang}")

        except Exception as e:
            print(f"[ERROR] Saat menerima file: {e}")

        finally:
            client_socket.close()
            print("[DISCONNECTED] Client ditutup")

except KeyboardInterrupt:
    print("\n[SHUTDOWN] Server dimatikan oleh user.")

finally:
    server_socket.close()
