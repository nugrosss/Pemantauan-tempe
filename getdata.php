<?php
require 'database.php';

$pdo = Database::connect();
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// Ambil data terbaru (ubah jika ada primary key lain)
$sql = "SELECT temperature, humidity FROM esp32_table_test ORDER BY id DESC LIMIT 1";
$q = $pdo->prepare($sql);
$q->execute();
$data = $q->fetch(PDO::FETCH_ASSOC);

Database::disconnect();

header('Content-Type: application/json');
echo json_encode($data);
?>
