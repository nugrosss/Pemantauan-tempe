from flask import Flask, render_template, Response, jsonify, request, send_file
import cv2
from ultralytics import YOLO
import time
import os

app = Flask(__name__)
model = YOLO("/home/pi/nabila nadia/progam baru /Pemantauan-tempe/best.pt")

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

def process_single_frame():
    global tempe_count

    cap = cv2.VideoCapture(0)
    time.sleep(2)

    success, frame = cap.read()
    cap.release()

    if not success:
        print("❌ Gagal membaca kamera")
        return

    results = model.predict(frame, verbose=False)

    tempe_count["Tempe bagus"] = 0
    tempe_count["Tempe jelek"] = 0

    frame_bagus = frame.copy()
    frame_jelek = frame.copy()

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id].lower()
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            warna = (0, 255, 0) if "bagus" in label else (0, 0, 255)

            if "tempe bagus" in label:
                tempe_count["Tempe bagus"] += 1
                cv2.rectangle(frame_bagus, (x1, y1), (x2, y2), warna, 2)
                cv2.putText(frame_bagus, f'{label} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, warna, 2)

            elif "tempe jelek" in label:
                tempe_count["Tempe jelek"] += 1
                cv2.rectangle(frame_jelek, (x1, y1), (x2, y2), warna, 2)
                cv2.putText(frame_jelek, f'{label} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, warna, 2)

    # Simpan hasil terpisah
    cv2.imwrite("static/tempe_bagus.jpg", frame_bagus)
    cv2.imwrite("static/tempe_jelek.jpg", frame_jelek)


@app.route('/image_feed')
def image_feed():
    global last_capture_time
    current_time = time.time()
    if current_time - last_capture_time >= 10:
        process_single_frame()
        last_capture_time = current_time
    return send_file(last_frame_path, mimetype='image/jpeg')

#tempe
@app.route('/tempe_bagus')
def tempe_bagus():
    global last_capture_time
    if time.time() - last_capture_time >= 10:
        process_single_frame()
        last_capture_time = time.time()
    return send_file("static/tempe_bagus.jpg", mimetype='image/jpeg')

@app.route('/tempe_jelek')
def tempe_jelek():
    global last_capture_time
    if time.time() - last_capture_time >= 10:
        process_single_frame()
        last_capture_time = time.time()
    return send_file("static/tempe_jelek.jpg", mimetype='image/jpeg')


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
