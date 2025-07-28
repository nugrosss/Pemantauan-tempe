const users = [
  { username: "admin", password: "1234" },
  { username: "user", password: "abcd" }
];

function login() {
  const username = document.getElementById("username")?.value;
  const password = document.getElementById("password")?.value;
  const errorMessage = document.getElementById("error-message");

  console.log("Input Username:", username);
  console.log("Input Password:", password);

  const user = users.find(
    u => u.username === username && u.password === password
  );

  if (!user) {
    console.warn("Username tidak ditemukan");
    errorMessage.textContent = "Username tidak ditemukan.";
    return;
  }

  if (user) {
    localStorage.setItem("loggedIn", "true");
    window.location.href = "page.html";
  } else {
    errorMessage.textContent = "Username atau password salah.";
  }
}

function history() {
  localStorage.removeItem("loggedIn");
  window.location.href = "history.html";
}


function updateSensorData() {
  fetch('getdata.php')
    .then(response => response.json())
    .then(data => {
      document.getElementById("suhu").textContent = `${data.temperature} °C`;
      document.getElementById("kelembapan").textContent = `${data.humidity} %`;
      console.log(`✅ [${fetchCount}] Temperature & humidity updated:`, data);
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

// function updateTempeCount() {
//   fetch('/tempe-count')
//     .then(response => response.json())
//     .then(data => {
//       document.getElementById('bagus').textContent = data.bagus;
//       document.getElementById('jelek').textContent = data.jelek;
//     })
//     .catch(error => console.error('Gagal ambil data tempe:', error));
// }

  // function resetImages() {
  //   document.getElementById("imgBagus").src = "";
  //   document.getElementById("imgJelek").src = "";
  // }

function updateImages() {
  const timestamp = new Date().getTime();
  document.getElementById("imgBagus").src = `upload_gambar/terbaru/Tempe bagus.jpg?t=${timestamp}`;
  document.getElementById("imgJelek").src = `upload_gambar/terbaru/Tempe jelek.jpg?t=${timestamp}`;
}


function updateImagesDasboar() {
  const timestamp = new Date().getTime();
  document.getElementById("imgBagus1").src = `/upload_gambar/terbaru/Tempe bagus.jpg?t=${timestamp}`;
  document.getElementById("imgJelek1").src = `/upload_gambar/terbaru/Tempe jelek.jpg?t=${timestamp}`;
}


// Fungsi untuk membaca file txt
// Simpan ID interval global untuk bisa di-reset
let waktuInterval = null;

// Fungsi untuk memperbarui satu elemen waktu
function perbaruiWaktu(idElement, filePath) {
  fetch(filePath)
    .then(response => response.text())
    .then(data => {
      document.getElementById(idElement).textContent = "Terakhir diperbarui: " + data.trim();
    })
    .catch(error => {
      console.error("Gagal membaca waktu dari " + filePath, error);
    });
}

// Fungsi untuk memanggil semua update waktu
function updateWaktu() {
  perbaruiWaktu("waktuBagus", "upload_gambar/terbaru/waktu_bagus.txt");
  perbaruiWaktu("waktuJelek", "upload_gambar/terbaru/waktu_jelek.txt");
}

// Fungsi untuk memulai ulang interval update
function mulaiIntervalWaktu() {
  if (waktuInterval) clearInterval(waktuInterval); // Reset interval lama
  updateWaktu(); // Jalankan pertama kali
  waktuInterval = setInterval(updateWaktu, 1000); // Set ulang interval tiap 1 detik
}

// Jalankan saat DOM siap





  // Reset setiap 3 detik
  // setInterval(resetImages, 3000);

  // Update gambar setiap 10 detik
  // setInterval(updateImages, 3000);



document.addEventListener('DOMContentLoaded', () => {
  updateSensorData();
  setInterval(updateSensorData, 1000);

  mulaiIntervalWaktu()

  updateDetectionImage();
  setInterval(updateDetectionImage, 500);

  updateWaktu();
  setInterval(updateWaktu,1000)

  ///aahhahhahahahahahhahah

  // updateTempeCount();
  // setInterval(updateTempeCount, 1000);  // ← Tambahkan baris ini

  updateImagesDasboar()
  setInterval(updateImagesDasboar, 1000);
});
