/**
 * GenelPara API - JavaScript Fetch API Örneği
 * 
 * Bu örnek, modern JavaScript ile API kullanımını gösterir.
 */

const API_URL = 'https://api.genelpara.com/json/';

/**
 * API'den veri çek
 */
async function getRates(list, symbols) {
    const params = new URLSearchParams({
        list: list,
        sembol: symbols
    });
    
    try {
        const response = await fetch(`${API_URL}?${params}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API isteği başarısız:', error);
        return null;
    }
}

/**
 * Verileri konsola yazdır
 */
function displayRates(data) {
    if (!data || !data.success) {
        console.error('❌ API hatası:', data?.error || 'Bilinmeyen hata');
        return;
    }
    
    console.log('=== DÖVİZ KURLARI ===\n');
    
    Object.entries(data.data).forEach(([symbol, info]) => {
        const arrow = info.yon === 'moneyUp' ? '↗' : 
                     info.yon === 'moneyDown' ? '↘' : '→';
        
        console.log(
            `${symbol}: ${info.satis} ${info.sembol} ${arrow} ${info.oran} (${info.degisim}%)`
        );
    });
    
    console.log('\n=== RATE LIMIT ===');
    console.log(`Kalan: ${data.rate_limit.remaining}/${data.rate_limit.limit}`);
    console.log(`Sıfırlanma: ${data.rate_limit.reset_at}`);
}

// Kullanım örneği
(async () => {
    console.log('API\'den veri çekiliyor...\n');
    
    const data = await getRates('doviz', 'USD,EUR,GBP');
    displayRates(data);
})();
