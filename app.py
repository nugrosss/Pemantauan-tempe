from flask import Flask, render_template, Response, jsonify, request, send_file
import cv2
from ultralytics import YOLO
import time
import os
from datetime import datetime

app = Flask(__name__)
model = YOLO("/home/pi/nabila nadia/progam baru /best (1).pt")

# Data Sensor
data_sensor = {
    "suhu": 0,
    "kelembaban": 0
}

tempe_count = {
    "Tempe bagus": 0,
    "Tempe jelek": 0
}

last_capture_time = 0
last_frame_path = "static/last_result.jpg"

# Direktori untuk history
HISTORY_DIR = "static/history"
os.makedirs(HISTORY_DIR, exist_ok=True)

def save_to_history(image):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(HISTORY_DIR, f"tempe_{timestamp}.jpg")
    cv2.imwrite(path, image)

def process_single_frame():
    global tempe_count, last_frame_path

    cap = cv2.VideoCapture(0)
    time.sleep(2)
    success, frame = cap.read()
    cap.release()

    if not success:
        print("❌ Gagal membaca kamera")
        return

    results = model.predict(frame, verbose=False)
    boxes = results[0].boxes
    names = model.names

    frame_with_box = frame.copy()

    tempe_count["Tempe bagus"] = 0
    tempe_count["Tempe jelek"] = 0

    for box in boxes:
        cls_id = int(box.cls[0])
        label = names[cls_id].lower()
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        warna = (0, 255, 0) if "bagus" in label else (0, 0, 255)
        cv2.rectangle(frame_with_box, (x1, y1), (x2, y2), warna, 2)
        cv2.putText(frame_with_box, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, warna, 2)

        if "bagus" in label:
            tempe_count["Tempe bagus"] += 1
        elif "jelek" in label:
            tempe_count["Tempe jelek"] += 1

    cv2.imwrite("static/tempe_bagus.jpg", frame_with_box)
    cv2.imwrite("static/tempe_jelek.jpg", frame_with_box)
    cv2.imwrite(last_frame_path, frame_with_box)

    save_to_history(frame_with_box)  # Simpan ke folder history

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', data=data_sensor)

@app.route('/image_feed')
def image_feed():
    global last_capture_time
    current_time = time.time()
    if current_time - last_capture_time >= 20:
        process_single_frame()
        last_capture_time = current_time
    return send_file(last_frame_path, mimetype='image/jpeg')

@app.route('/tempe_bagus')
def tempe_bagus():
    return send_file("static/tempe_bagus.jpg", mimetype='image/jpeg')

@app.route('/tempe_jelek')
def tempe_jelek():
    return send_file("static/tempe_jelek.jpg", mimetype='image/jpeg')

@app.route('/tempe-count')
def get_tempe_count():
    return jsonify(tempe_count)

@app.route('/sensor-data')
def sensor_data():
    return jsonify(data_sensor)

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

@app.route('/history')
def show_history():
    files = sorted(os.listdir(HISTORY_DIR), reverse=True)
    image_urls = [f"/{HISTORY_DIR}/{f}" for f in files if f.endswith(".jpg")]
    return render_template("history.html", images=image_urls)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
