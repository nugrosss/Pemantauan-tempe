from flask import Flask, render_template, Response, jsonify, request, send_file
import cv2
from ultralytics import YOLO
import time
import os
import datetime
from gpiozero import Buzzer



buzzer = Buzzer(3)
app = Flask(__name__)
model = YOLO("/home/pi/nabila nadia/progam baru /best (1).pt")

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

    # Deteksi YOLO
    results = model.predict(frame, verbose=False)
    boxes = results[0].boxes
    names = model.names

    # Inisialisasi frame hasil
    frame_with_box = frame.copy()

    # Reset jumlah tempe
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

    # Simpan 1 gambar hasil (dengan box)
    cv2.imwrite("static/tempe_bagus.jpg", frame_with_box)
    cv2.imwrite("static/tempe_jelek.jpg", frame_with_box)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"static/history/tempe_{timestamp}.jpg"
    cv2.imwrite(filename, frame_with_box)
    print(f"✅ Disimpan ke history: {filename}")



@app.route('/image_feed')
def image_feed():
    global last_capture_time
    current_time = time.time()
    if current_time - last_capture_time >= 10:
        process_single_frame()
        last_capture_time = current_time
    return send_file(last_frame_path, mimetype='image/jpeg')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


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

@app.route('/history')
def history():
    image_folder = 'static/history'
    images = []
    if os.path.exists(image_folder):
        images = os.listdir(image_folder)
        images.sort(reverse=True)  # Supaya terbaru tampil dulu
    return render_template('history.html', images=images)


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

    print("server on")
    buzzer.on()
    time.sleep(1)
    buzzer.off()
    app.run(host='0.0.0.0', port=5050, debug=True, use_reloader=False)
