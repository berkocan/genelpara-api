<?php
/**
 * GenelPara API - Web Sayfası Örneği
 * 
 * Bu örnek, API verilerini bir web sayfasında göstermeyi gösterir.
 */

// API'den veri çek
function fetchRates($list = 'doviz', $symbols = 'USD,EUR,GBP') {
    $apiUrl = 'https://api.genelpara.com/json/';
    $params = http_build_query([
        'list' => $list,
        'sembol' => $symbols
    ]);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $apiUrl . '?' . $params);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($response, true);
}

$data = fetchRates('doviz', 'USD,EUR,GBP,JPY');
?>
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Döviz Kurları - GenelPara API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2563eb;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #64748b;
            margin-bottom: 30px;
        }
        .rate-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .rate-card {
            background: #f8fafc;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #2563eb;
        }
        .rate-card.up { border-left-color: #10b981; }
        .rate-card.down { border-left-color: #ef4444; }
        .symbol {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 10px;
        }
        .price {
            font-size: 2rem;
            font-weight: 700;
            color: #2563eb;
            margin-bottom: 5px;
        }
        .change {
            font-size: 0.875rem;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 4px;
            display: inline-block;
        }
        .change.up {
            background: #d1fae5;
            color: #065f46;
        }
        .change.down {
            background: #fee2e2;
            color: #991b1b;
        }
        .change.neutral {
            background: #e2e8f0;
            color: #475569;
        }
        .info {
            background: #dbeafe;
            border-left: 4px solid #2563eb;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .info strong { color: #1e40af; }
        .timestamp {
            text-align: center;
            color: #94a3b8;
            font-size: 0.875rem;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💱 Canlı Döviz Kurları</h1>
        <p class="subtitle">GenelPara API ile güncellenen anlık kurlar</p>

        <?php if ($data && $data['success']): ?>
            <div class="rate-grid">
                <?php foreach ($data['data'] as $symbol => $info): ?>
                    <?php
                        $direction = 'neutral';
                        if ($info['yon'] == 'moneyUp') $direction = 'up';
                        if ($info['yon'] == 'moneyDown') $direction = 'down';
                    ?>
                    <div class="rate-card <?php echo $direction; ?>">
                        <div class="symbol"><?php echo $symbol; ?></div>
                        <div class="price">
                            <?php echo number_format((float)$info['satis'], 4); ?> 
                            <?php echo $info['sembol']; ?>
                        </div>
                        <span class="change <?php echo $direction; ?>">
                            <?php echo $info['oran']; ?> 
                            (<?php echo $info['degisim']; ?>%)
                        </span>
                    </div>
                <?php endforeach; ?>
            </div>

            <div class="info">
                <strong>ℹ️ Rate Limit:</strong> 
                <?php echo $data['rate_limit']['remaining']; ?>/<?php echo $data['rate_limit']['limit']; ?> 
                istek kaldı. 
                Sıfırlanma: <?php echo $data['rate_limit']['reset_at']; ?>
            </div>

            <div class="timestamp">
                Son güncelleme: <?php echo date('d.m.Y H:i:s'); ?>
            </div>
        <?php else: ?>
            <div style="background: #fee2e2; color: #991b1b; padding: 20px; border-radius: 8px;">
                <strong>❌ Hata:</strong> API'den veri alınamadı!
            </div>
        <?php endif; ?>
    </div>
</body>
</html>
