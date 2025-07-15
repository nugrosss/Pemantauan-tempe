const users = [
  { username: "admin", password: "1234" },
  { username: "user", password: "abcd" }
];

function login() {
  const username = document.getElementById("username")?.value;
  const password = document.getElementById("password")?.value;
  const errorMessage = document.getElementById("error-message");

  const user = users.find(
    u => u.username === username && u.password === password
  );

  if (user) {
    localStorage.setItem("loggedIn", "true");
    window.location.href = "/dashboard";
  } else {
    errorMessage.textContent = "Username atau password salah.";
  }
}

function logout() {
  localStorage.removeItem("loggedIn");
  window.location.href = "/";
}

function updateSensorData() {
  fetch('/sensor-data')
    .then(response => response.json())
    .then(data => {
      document.getElementById('suhu').textContent = data.suhu;
      document.getElementById('kelembaban').textContent = data.kelembaban;
    })
    .catch(error => console.error('Gagal ambil data:', error));
}

function updateDetectionImage() {
  const img = document.getElementById('deteksi');
  if (img) {
    const timestamp = new Date().getTime();
    img.src = `/latest_image?t=${timestamp}`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateSensorData();
  setInterval(updateSensorData, 1000);
  setInterval(updateDetectionImage, 500);
});
