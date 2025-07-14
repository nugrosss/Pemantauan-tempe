
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
    // Simpan status login di localStorage
    localStorage.setItem("loggedIn", "true");
    
    // Redirect ke route Flask, bukan file HTML langsung!
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

// Jalankan saat halaman selesai dimuat
document.addEventListener('DOMContentLoaded', () => {
  updateSensorData(); // Panggil langsung pertama kali
  setInterval(updateSensorData, 1000); // Update setiap 1 detik
});
