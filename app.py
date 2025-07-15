from flask import Flask, request, render_template ,jsonify,Response , send_file
import cv2
from ultralytics import YOLO 
import time
from threading import Thread
import io
from PIL import Image


app = Flask(__name__)
data_sensor = {
    "suhu": 0,
    "kelembaban": 0
}

cap = cv2.VideoCapture(0)
model = YOLO("/home/pi/nabila nadia/progam baru /Pemantauan-tempe/best.pt")

latest_frame = None  # Variabel global untuk menyimpan gambar terbaru

def capture_and_detect():
    global latest_frame
    while True:
        success, frame = cap.read()
        if not success:
            print("⚠️ Gagal membaca frame dari kamera.")
            time.sleep(0.5)
            continue

        # Jalankan YOLO
        results = model.predict(frame, verbose=False)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls_id = int(box.cls[0])
                label = model.names[cls_id]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Simpan frame sebagai image ke memori
        _, buffer = cv2.imencode('.jpg', frame)
        latest_frame = buffer.tobytes()

        time.sleep(0.5)  # Ambil foto setiap 500ms

# Jalankan thread terpisah untuk loop kamera
Thread(target=capture_and_detect, daemon=True).start()

@app.route('/')
def index():
    return render_template('image_view.html')

@app.route('/latest_image')
def latest_image():
    global latest_frame
    if latest_frame:
        return Response(latest_frame, mimetype='image/jpeg')
    else:
        return "Belum ada gambar", 503


@app.route('/sensor-data')
def sensor_data():
    return jsonify(data_sensor)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', data=data_sensor)

# 🟢 Tambahkan decorator ini agar bisa diakses dari ESP32
@app.route('/update')
def update_data():
    suhu = request.args.get('suhu')
    kelembaban = request.args.get('kelembaban')
    
    if suhu and kelembaban:
        data_sensor['suhu'] = suhu
        data_sensor['kelembaban'] = kelembaban
        print(f"DATA MASUK: Suhu = {suhu}, Kelembaban = {kelembaban}")
        return "Data diterima"
    return "Data tidak lengkap"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=False)
