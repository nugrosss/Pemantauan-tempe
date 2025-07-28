<?php
$folder = 'upload_gambar/history';
$files = scandir($folder);
foreach ($files as $file) {
    if (strpos($file, 'Tempe jelek') !== false && preg_match('/\.jpg$/', $file)) {
        echo "<img src='$folder$file' alt='$file'><br>";
    }
}
?>
