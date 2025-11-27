<?php
/**
 * GenelPara API - Çoklu Kategori Örneği
 * 
 * Bu örnek, birden fazla kategoriden (döviz, kripto, altın) 
 * veri çekmeyi gösterir.
 */

class GenelParaAPI {
    private $apiUrl = 'https://api.genelpara.com/json/';
    private $timeout = 10;
    
    /**
     * API'den veri çek
     * 
     * @param string|array $list Kategori listesi
     * @param string|array $sembol Sembol listesi veya 'all'
     * @return array|false API yanıtı veya false
     */
    public function getData($list, $sembol = 'all') {
        // Array ise string'e çevir
        if (is_array($list)) {
            $list = implode(',', $list);
        }
        if (is_array($sembol)) {
            $sembol = implode(',', $sembol);
        }
        
        $params = http_build_query([
            'list' => $list,
            'sembol' => $sembol
        ]);
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->apiUrl . '?' . $params);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, $this->timeout);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        
        if (curl_errno($ch)) {
            error_log('cURL Hatası: ' . curl_error($ch));
            curl_close($ch);
            return false;
        }
        
        curl_close($ch);
        
        if ($httpCode != 200) {
            error_log('HTTP Hatası: ' . $httpCode);
            return false;
        }
        
        return json_decode($response, true);
    }
    
    /**
     * Rate limit bilgisini al
     */
    public function getRateLimit($data) {
        return $data['rate_limit'] ?? null;
    }
    
    /**
     * Belirli bir sembolün verisini al
     */
    public function getSymbolData($data, $symbol) {
        return $data['data'][$symbol] ?? null;
    }
}

// Kullanım örneği
$api = new GenelParaAPI();

// Çoklu kategori ve sembol
$result = $api->getData(
    ['doviz', 'kripto', 'altin'],
    ['USD', 'EUR', 'BTC', 'ETH', 'GA']
);

if ($result && $result['success']) {
    echo "=== ÇOKLU KATEGORİ VERİLERİ ===\n\n";
    
    // Kategorilere göre grupla
    $grouped = [];
    foreach ($result['data'] as $symbol => $info) {
        $source = $info['_source'] ?? 'unknown';
        $grouped[$source][$symbol] = $info;
    }
    
    // Her kategoriyi göster
    foreach ($grouped as $category => $symbols) {
        echo strtoupper($category) . ":\n";
        echo str_repeat('-', 50) . "\n";
        
        foreach ($symbols as $symbol => $info) {
            echo sprintf(
                "  %s: %s %s (Değişim: %s%%)\n",
                str_pad($symbol, 6),
                number_format((float)$info['satis'], 2),
                $info['sembol'],
                $info['degisim']
            );
        }
        echo "\n";
    }
    
    // Rate limit bilgisi
    $rateLimit = $api->getRateLimit($result);
    if ($rateLimit) {
        echo "=== RATE LIMIT ===\n";
        echo sprintf(
            "Kalan: %d/%d | Sıfırlanma: %s\n",
            $rateLimit['remaining'],
            $rateLimit['limit'],
            $rateLimit['reset_at']
        );
    }
    
} else {
    echo "API'den veri alınamadı!\n";
    if (isset($result['error'])) {
        echo "Hata: " . $result['error'] . "\n";
    }
}
