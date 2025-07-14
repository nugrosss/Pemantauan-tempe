from flask import Flask, request, render_template ,jsonify,Response
import cv2
from ultralytics import YOLO 


app = Flask(__name__)
data_sensor = {
    "suhu": 0,
    "kelembaban": 0
}

cap = cv2.VideoCapture(0)  # Ganti ke 1 jika pakai kamera USB eksternal
model = YOLO("/home/pi/nabila nadia/progam baru /Pemantauan-tempe/best.pt")

if not cap.isOpened():
    print("Kamera tidak terdeteksi.")
else:
    print("Kamera berhasil dibuka.")

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            print("⚠️ Gagal membaca frame dari kamera.")
            break
        else:
            # Jalankan deteksi dengan YOLO
            results = model.predict(frame, verbose=False)

            # Ambil hasil deteksi dari frame
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Koordinat bounding box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Skor dan label
                    conf = box.conf[0]
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]

                    # Gambar bounding box dan label di frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Encode frame ke JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Kirim frame sebagai stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


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
