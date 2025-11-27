# 💰 GenelPara API - Kod Örnekleri

> 🇹🇷 GenelPara API'sini farklı programlama dillerinde kullanım örnekleri

[![API Status](https://img.shields.io/badge/API-Online-success)](https://api.genelpara.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📚 İçerik

Bu repository, GenelPara API'sini çeşitli programlama dillerinde nasıl kullanacağınızı gösteren örnek kodlar içerir.

- 🐘 **PHP** - Web uygulamaları için
- 🟨 **JavaScript** - Frontend ve Node.js için
- 🐍 **Python** - Data analysis ve backend için
- 💻 **cURL** - Komut satırı kullanımı için

## 🚀 Hızlı Başlangıç

### API Endpoint

```
https://api.genelpara.com/json/
```

### Parametreler

| Parametre | Açıklama | Örnek |
|-----------|----------|-------|
| `list` | Kategori (doviz, kripto, altin, emtia, hisse, endeks) | `doviz` |
| `sembol` | Sembol kodları (virgülle ayrılmış) veya "all" | `USD,EUR,BTC` |

### Basit Örnek

```bash
curl "https://api.genelpara.com/json/?list=doviz&sembol=USD,EUR"
```

## 📂 Klasör Yapısı

```
genelpara-api/
├── php/
│   ├── basic-example.php        # Basit kullanım
│   ├── multi-category.php       # Çoklu kategori
│   └── web-display.php          # Web sayfası örneği
├── javascript/
│   ├── basic-fetch.js           # Fetch API
│   ├── react-component.jsx      # React component
│   └── interactive-page.html    # İnteraktif sayfa
├── python/
│   ├── basic_example.py         # Basit kullanım
│   ├── api_wrapper.py           # Class wrapper
│   └── flask_app.py             # Flask web app
├── curl/
│   ├── examples.sh              # Örnek komutlar (script)
│   └── COMMANDS.md              # Komut referansı
└── README.md                     # Bu dosya
```

## 🐘 PHP Örnekleri

### Basit Kullanım

```php
<?php
$apiUrl = 'https://api.genelpara.com/json/';
$params = http_build_query([
    'list' => 'doviz',
    'sembol' => 'USD,EUR'
]);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $apiUrl . '?' . $params);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response, true);
print_r($data);
```

**Daha fazla örnek:** [`php/`](php/) klasörüne bakın

## 🟨 JavaScript Örnekleri

### Fetch API

```javascript
const API_URL = 'https://api.genelpara.com/json/';

async function getRates() {
    const params = new URLSearchParams({
        list: 'doviz',
        sembol: 'USD,EUR'
    });
    
    const response = await fetch(`${API_URL}?${params}`);
    const data = await response.json();
    
    console.log(data);
}

getRates();
```

**Daha fazla örnek:** [`javascript/`](javascript/) klasörüne bakın

## 🐍 Python Örnekleri

### Requests ile Kullanım

```python
import requests

API_URL = 'https://api.genelpara.com/json/'

params = {
    'list': 'doviz',
    'sembol': 'USD,EUR'
}

response = requests.get(API_URL, params=params)
data = response.json()

print(data)
```

**Daha fazla örnek:** [`python/`](python/) klasörüne bakın

## 💻 cURL Örnekleri

### Basit İstek

```bash
curl "https://api.genelpara.com/json/?list=doviz&sembol=USD,EUR"
```

### JSON Formatında (jq ile)

```bash
curl "https://api.genelpara.com/json/?list=doviz&sembol=USD" | jq .
```

**Daha fazla örnek:** [`curl/COMMANDS.md`](curl/COMMANDS.md) dosyasına bakın

## 🎯 Kullanım Senaryoları

### 1. Web Sitesinde Döviz Göstergesi

**Dil:** PHP, JavaScript  
**Dosyalar:** `php/web-display.php`, `javascript/interactive-page.html`

Canlı döviz kurlarını web sitenizde gösterin.

### 2. Mobil Uygulama Backend

**Dil:** Python (Flask)  
**Dosya:** `python/flask_app.py`

Mobile API endpoint oluşturun.

### 3. Otomatik Fiyat Takibi

**Dil:** Python  
**Dosya:** `python/api_wrapper.py`

Belirli aralıklarla fiyatları takip edin.

### 4. Komut Satırı Aracı

**Dil:** cURL + Bash  
**Dosya:** `curl/examples.sh`

Terminal'den hızlı fiyat kontrolü.

## 📊 Rate Limiting

| Limit | Değer |
|-------|-------|
| Günlük İstek | 1.000 / IP |
| Sıfırlanma | Her gün 00:00 |
| IP Ban Eşiği | 10.000+ istek/gün |

**⚠️ Önemli:** 10.000'den fazla istek gönderen IP'ler Cloudflare tarafından süresiz engellenecektir.

## 🔧 Gereksinimler

### PHP
- PHP 7.4+
- cURL extension

### JavaScript
- Modern browser (ES6+)
- Node.js 14+ (backend için)

### Python
- Python 3.7+
- `requests` library
- `flask` (web app için)

### cURL
- cURL 7.0+
- `jq` (JSON parsing için, opsiyonel)

## 📥 Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/berkocan/genelpara-api.git
cd genelpara-api

# PHP örneği çalıştır
php php/basic-example.php

# Python örneği çalıştır
python3 python/basic_example.py

# Flask uygulaması çalıştır
pip install flask requests
python3 python/flask_app.py

# cURL örnekleri çalıştır
chmod +x curl/examples.sh
./curl/examples.sh
```

## 📖 API Dokümantasyonu

Detaylı API dokümantasyonu için: **https://api.genelpara.com**

### Kategoriler

- **doviz** - Döviz kurları (USD, EUR, GBP, vb.)
- **kripto** - Kripto paralar (BTC, ETH, XRP, vb.)
- **altin** - Altın fiyatları (GA, C, vb.)
- **emtia** - Emtia fiyatları (BRENT, GOLD, vb.)
- **hisse** - Hisse senetleri (THYAO, GARAN, vb.)
- **endeks** - Endeksler (XU100, XU030, vb.)

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'feat: Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje [MIT lisansı](LICENSE) altında lisanslanmıştır.

## 💬 Destek

- **API Dokümantasyonu:** [api.genelpara.com](https://api.genelpara.com)
- **GitHub Issues:** [Yeni issue aç](https://github.com/berkocan/genelpara-api/issues)

## 🙏 Teşekkürler

GenelPara API'yi kullandığınız için teşekkür ederiz!

---

**⭐ Bu projeyi faydalı bulduysanız yıldızlamayı unutmayın!**

## 📚 İlgili Projeler

- [GenelPara API Dokümantasyon](https://api.genelpara.com)
- [GenelPara Website](https://genelpara.com)
