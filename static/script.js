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

function history() {
  // localStorage.removeItem("loggedIn");
  window.location.href = "/history";
}


function updateSensorData() {
  fetch('/sensor-data')
    .then(response => response.json())
    .then(data => {
      document.getElementById('suhu').textContent = data.suhu;
      document.getElementById('kelembaban').textContent = data.kelembaban;
    })
    .catch(error => console.error('Gagal ambil data sensor:', error));
}

function updateDetectionImage() {
  const img = document.getElementById('deteksi');
  if (img) {
    const timestamp = new Date().getTime();
    img.src = `/latest_image?t=${timestamp}`;
  }
}

function updateTempeCount() {
  fetch('/tempe-count')
    .then(response => response.json())
    .then(data => {
      document.getElementById('bagus').textContent = data.bagus;
      document.getElementById('jelek').textContent = data.jelek;
    })
    .catch(error => console.error('Gagal ambil data tempe:', error));
}

  function resetImages() {
    document.getElementById("imgBagus").src = "";
    document.getElementById("imgJelek").src = "";
  }

function updateImages() {
  const timestamp = new Date().getTime();
  document.getElementById("imgBagus").src = `/static/tempe_bagus.jpg?t=${timestamp}`;
  document.getElementById("imgJelek").src = `/static/tempe_jelek.jpg?t=${timestamp}`;
}

function updateImagesDasboar() {
  const timestamp = new Date().getTime();
  document.getElementById("imgBagus1").src = `/static/tempe_bagus.jpg?t=${timestamp}`;
  document.getElementById("imgJelek1").src = `/static/tempe_jelek.jpg?t=${timestamp}`;
}


  // Reset setiap 3 detik
  // setInterval(resetImages, 3000);

  // Update gambar setiap 10 detik
  setInterval(updateImages, 3000);



document.addEventListener('DOMContentLoaded', () => {
  updateSensorData();
  setInterval(updateSensorData, 1000);

  updateDetectionImage();
  setInterval(updateDetectionImage, 500);

  updateTempeCount();
  setInterval(updateTempeCount, 1000);  // ← Tambahkan baris ini

  updateImagesDasboar()
  setInterval(updateImagesDasboar, 1000);
});
