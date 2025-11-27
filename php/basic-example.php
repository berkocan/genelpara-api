<?php
/**
 * GenelPara API - Basit Kullanım Örneği
 * 
 * Bu örnek, GenelPara API'sini kullanarak döviz ve kripto para
 * fiyatlarını çekmeyi gösterir.
 */

// API endpoint
$apiUrl = 'https://api.genelpara.com/json/';

// İstek parametreleri
$params = http_build_query([
    'list' => 'doviz',
    'sembol' => 'USD,EUR,GBP'
]);

// cURL ile istek gönder
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $apiUrl . '?' . $params);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if (curl_errno($ch)) {
    die('cURL Hatası: ' . curl_error($ch));
}

curl_close($ch);

// Yanıtı işle
if ($httpCode == 200) {
    $data = json_decode($response, true);
    
    if ($data['success']) {
        echo "=== DÖVİZ FİYATLARI ===\n\n";
        
        foreach ($data['data'] as $symbol => $info) {
            echo sprintf(
                "%s: Alış: %s %s | Satış: %s %s | Değişim: %s%%\n",
                $symbol,
                $info['alis'],
                $info['sembol'],
                $info['satis'],
                $info['sembol'],
                $info['degisim']
            );
        }
        
        echo "\n=== RATE LIMIT BİLGİSİ ===\n";
        echo sprintf(
            "Kalan İstek: %d/%d\n",
            $data['rate_limit']['remaining'],
            $data['rate_limit']['limit']
        );
        echo "Sıfırlanma Zamanı: " . $data['rate_limit']['reset_at'] . "\n";
    } else {
        echo "API Hatası: " . ($data['error'] ?? 'Bilinmeyen hata') . "\n";
    }
} else {
    echo "HTTP Hatası: " . $httpCode . "\n";
}
