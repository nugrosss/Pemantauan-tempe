from flask import Flask, render_template, Response, jsonify, request
import cv2
from ultralytics import YOLO
import time

app = Flask(__name__)

data_sensor = {
    "suhu": 0,
    "kelembaban": 0
}

tempe_count = {
    "bagus": 0,
    "jelek": 0
}

cap = cv2.VideoCapture(0)
model = YOLO("/home/pi/nabila nadia/progam baru /Pemantauan-tempe/best.pt")

def generate_frames():
    global tempe_count
    while True:
        success, frame = cap.read()
        if not success:
            print("❌ Gagal membaca kamera")
            break

        results = model.predict(frame, verbose=False)

        # Reset jumlah tempe
        tempe_count["bagus"] = 0
        tempe_count["jelek"] = 0

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id].lower()

                if "bagus" in label:
                    tempe_count["bagus"] += 1
                elif "jelek" in label:
                    tempe_count["jelek"] += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Encode ke JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Streaming ke browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', data=data_sensor)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/sensor-data')
def sensor_data():
    return jsonify(data_sensor)

@app.route('/tempe-count')
def get_tempe_count():
    return jsonify(tempe_count)

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
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
