<?php
// api.php - Backend API untuk Dashboard Tempe History
// Updated untuk XAMPP environment

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Konfigurasi untuk XAMPP
$history_folder = 'upload_gambar/history/';
$full_path = $_SERVER['DOCUMENT_ROOT'] . '/web/' . $history_folder;
$web_url_base = '/web/' . $history_folder;
$allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'];

// Fungsi untuk mengklasifikasi gambar berdasarkan nama file
function classifyTempeImage($filename) {
    $lowerName = strtolower($filename);
    
    // Pattern untuk tempe jelek (berdasarkan nama file)
    $jelek_patterns = [
        'jelek', 'bad', 'rusak', 'busuk', 'tidak_bagus', 'reject',
        'low_quality', 'poor', 'defect', 'damaged'
    ];
    
    // Pattern untuk tempe bagus
    $bagus_patterns = [
        'bagus', 'good', 'fresh', 'berkualitas', 'baik', 'accept',
        'high_quality', 'premium', 'excellent', 'perfect'
    ];
    
    // Cek pattern jelek
    foreach ($jelek_patterns as $pattern) {
        if (strpos($lowerName, $pattern) !== false) {
            return 'jelek';
        }
    }
    
    // Cek pattern bagus
    foreach ($bagus_patterns as $pattern) {
        if (strpos($lowerName, $pattern) !== false) {
            return 'bagus';
        }
    }
    
    // Klasifikasi berdasarkan pattern regex
    if (preg_match('/tempe[_\s]*jelek/i', $lowerName)) {
        return 'jelek';
    }
    
    if (preg_match('/tempe[_\s]*bagus/i', $lowerName)) {
        return 'bagus';
    }
    
    // Berdasarkan timestamp dalam filename
    if (preg_match('/(\d{6,})/', $filename, $matches)) {
        $number = intval($matches[1]);
        return ($number % 2 == 0) ? 'bagus' : 'jelek';
    }
    
    // Default: berdasarkan hash filename
    return (crc32($filename) % 2 == 0) ? 'bagus' : 'jelek';
}

// Fungsi untuk membaca semua gambar dari folder history
function getHistoryImages($folder_path, $web_url_base, $allowed_extensions) {
    $images = [];
    
    if (!is_dir($folder_path)) {
        return [
            'success' => false,
            'error' => 'Folder tidak ditemukan: ' . $folder_path,
            'folder_path' => $folder_path,
            'images' => []
        ];
    }
    
    $files = scandir($folder_path);
    
    if ($files === false) {
        return [
            'success' => false,
            'error' => 'Tidak dapat membaca folder',
            'folder_path' => $folder_path,
            'images' => []
        ];
    }
    
    foreach ($files as $file) {
        if ($file === '.' || $file === '..') continue;
        
        $file_path = $folder_path . $file;
        $file_extension = strtolower(pathinfo($file, PATHINFO_EXTENSION));
        
        if (is_file($file_path) && in_array($file_extension, $allowed_extensions)) {
            $classification = classifyTempeImage($file);
            $file_size = filesize($file_path);
            $file_date = date('Y-m-d H:i:s', filemtime($file_path));
            
            $images[] = [
                'filename' => $file,
                'path' => $file_path,
                'url' => $web_url_base . $file, // URL untuk akses via web
                'classification' => $classification,
                'size' => $file_size,
                'size_formatted' => formatFileSize($file_size),
                'date' => $file_date,
                'date_formatted' => date('d/m/Y H:i', strtotime($file_date)),
                'extension' => strtoupper($file_extension),
                'timestamp' => strtotime($file_date)
            ];
        }
    }
    
    // Urutkan berdasarkan tanggal terbaru
    usort($images, function($a, $b) {
        return $b['timestamp'] - $a['timestamp'];
    });
    
    return [
        'success' => true,
        'folder_path' => $folder_path,
        'folder_exists' => true,
        'total_files' => count($files) - 2, // exclude . dan ..
        'image_files' => count($images),
        'images' => $images
    ];
}

// Fungsi untuk format ukuran file
function formatFileSize($bytes) {
    if ($bytes >= 1048576) {
        return number_format($bytes / 1048576, 1) . ' MB';
    } elseif ($bytes >= 1024) {
        return number_format($bytes / 1024, 1) . ' KB';
    } else {
        return $bytes . ' B';
    }
}

// Fungsi untuk memisahkan gambar berdasarkan klasifikasi
function separateImagesByClassification($images_data) {
    if (!$images_data['success'] || empty($images_data['images'])) {
        return [
            'success' => $images_data['success'] ?? false,
            'error' => $images_data['error'] ?? 'No images found',
            'folder_info' => [
                'path' => $images_data['folder_path'] ?? '',
                'exists' => $images_data['folder_exists'] ?? false,
                'total_files' => $images_data['total_files'] ?? 0,
                'image_files' => $images_data['image_files'] ?? 0
            ],
            'bagus' => [],
            'jelek' => [],
            'statistics' => [
                'total' => 0,
                'bagus_count' => 0,
                'jelek_count' => 0,
                'percentage_bagus' => 0,
                'percentage_jelek' => 0
            ]
        ];
    }
    
    $all_images = $images_data['images'];
    
    // Pisahkan berdasarkan klasifikasi
    $bagus_images = array_filter($all_images, function($img) {
        return $img['classification'] === 'bagus';
    });
    
    $jelek_images = array_filter($all_images, function($img) {
        return $img['classification'] === 'jelek';
    });
    
    // Reset array indices
    $bagus_images = array_values($bagus_images);
    $jelek_images = array_values($jelek_images);
    
    $total_count = count($all_images);
    $bagus_count = count($bagus_images);
    $jelek_count = count($jelek_images);
    
    return [
        'success' => true,
        'folder_info' => [
            'path' => $images_data['folder_path'],
            'exists' => $images_data['folder_exists'],
            'total_files' => $images_data['total_files'],
            'image_files' => $images_data['image_files']
        ],
        'bagus' => $bagus_images,
        'jelek' => $jelek_images,
        'statistics' => [
            'total' => $total_count,
            'bagus_count' => $bagus_count,
            'jelek_count' => $jelek_count,
            'percentage_bagus' => $total_count > 0 ? round(($bagus_count / $total_count) * 100, 1) : 0,
            'percentage_jelek' => $total_count > 0 ? round(($jelek_count / $total_count) * 100, 1) : 0
        ],
        'last_updated' => date('Y-m-d H:i:s'),
        'server_info' => [
            'php_version' => PHP_VERSION,
            'server_time' => date('Y-m-d H:i:s'),
            'document_root' => $_SERVER['DOCUMENT_ROOT']
        ]
    ];
}

if ($_GET['action'] === 'hapus_semua') {
    $folder = 'upload_gambar/history';
    $deleted = 0;

    foreach (glob($folder . '/*.{jpg,jpeg,png,gif}', GLOB_BRACE) as $file) {
        if (is_file($file)) {
            unlink($file);
            $deleted++;
        }
    }

    echo json_encode([
        'success' => true,
        'deleted_files' => $deleted
    ]);
    exit;
}



// Handle different API endpoints
$action = $_GET['action'] ?? 'get_images';

switch ($action) {
    case 'get_images':
        // Ambil semua gambar dan pisahkan berdasarkan klasifikasi
        $images_data = getHistoryImages($full_path, $web_url_base, $allowed_extensions);
        $result = separateImagesByClassification($images_data);
        echo json_encode($result, JSON_PRETTY_PRINT);
        break;
        
    case 'get_stats':
        // Hanya ambil statistik
        $images_data = getHistoryImages($full_path, $web_url_base, $allowed_extensions);
        $result = separateImagesByClassification($images_data);
        echo json_encode([
            'success' => $result['success'],
            'statistics' => $result['statistics'],
            'folder_info' => $result['folder_info'],
            'last_updated' => $result['last_updated'] ?? date('Y-m-d H:i:s')
        ], JSON_PRETTY_PRINT);
        break;
        
    case 'get_folder_info':
        // Info folder saja
        $folder_exists = is_dir($full_path);
        $total_files = 0;
        $image_files = 0;
        
        if ($folder_exists) {
            $files = scandir($full_path);
            $total_files = count($files) - 2; // exclude . dan ..
            
            foreach ($files as $file) {
                if ($file === '.' || $file === '..') continue;
                $file_extension = strtolower(pathinfo($file, PATHINFO_EXTENSION));
                if (in_array($file_extension, $allowed_extensions)) {
                    $image_files++;
                }
            }
        }
        
        echo json_encode([
            'success' => true,
            'folder_path' => $full_path,
            'web_path' => $web_url_base,
            'folder_exists' => $folder_exists,
            'total_files' => $total_files,
            'image_files' => $image_files,
            'allowed_extensions' => $allowed_extensions,
            'server_time' => date('Y-m-d H:i:s'),
            'php_version' => PHP_VERSION
        ], JSON_PRETTY_PRINT);
        break;
        
    case 'classify_single':
        // Klasifikasi single file (untuk testing)
        $filename = $_GET['filename'] ?? '';
        if (empty($filename)) {
            echo json_encode([
                'success' => false,
                'error' => 'Parameter filename diperlukan'
            ]);
            break;
        }
        
        $classification = classifyTempeImage($filename);
        echo json_encode([
            'success' => true,
            'filename' => $filename,
            'classification' => $classification,
            'timestamp' => date('Y-m-d H:i:s')
        ], JSON_PRETTY_PRINT);
        break;
        
    case 'test_connection':
        // Test koneksi dan environment
        echo json_encode([
            'success' => true,
            'message' => 'API berfungsi dengan baik',
            'environment' => [
                'php_version' => PHP_VERSION,
                'server_time' => date('Y-m-d H:i:s'),
                'document_root' => $_SERVER['DOCUMENT_ROOT'],
                'script_name' => $_SERVER['SCRIPT_NAME'],
                'full_folder_path' => $full_path,
                'web_url_base' => $web_url_base,
                'folder_exists' => is_dir($full_path),
                'folder_readable' => is_readable($full_path)
            ]
        ], JSON_PRETTY_PRINT);
        break;
        
    default:
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'error' => 'Action tidak valid: ' . $action,
            'available_actions' => [
                'get_images' => 'Ambil semua gambar dengan klasifikasi',
                'get_stats' => 'Ambil statistik saja', 
                'get_folder_info' => 'Ambil informasi folder',
                'classify_single' => 'Klasifikasi single file (parameter: filename)',
                'test_connection' => 'Test koneksi dan environment'
            ]
        ], JSON_PRETTY_PRINT);
        break;
}
?>