# GenelPara API - cURL Hızlı Referans

## Temel Kullanım

### Döviz Kurları
```bash
curl "https://api.genelpara.com/json/?list=doviz&sembol=USD,EUR"
```

### Kripto Paralar
```bash
curl "https://api.genelpara.com/json/?list=kripto&sembol=BTC,ETH"
```

### Altın Fiyatları
```bash
curl "https://api.genelpara.com/json/?list=altin&sembol=GA"
```

## Gelişmiş Kullanım

### Çoklu Kategori
```bash
curl "https://api.genelpara.com/json/?list=doviz,kripto,altin&sembol=USD,BTC,GA"
```

### Tüm Sembolleri Getir
```bash
curl "https://api.genelpara.com/json/?list=doviz&sembol=all"
```

### JSON Formatında (jq ile)
```bash
curl "https://api.genelpara.com/json/?list=doviz&sembol=USD" | jq .
```

### Sadece Fiyatı Göster
```bash
curl -s "https://api.genelpara.com/json/?list=doviz&sembol=USD" | jq '.data.USD.satis'
```

### Rate Limit Bilgisi
```bash
curl -s "https://api.genelpara.com/json/?list=doviz&sembol=USD" | jq '.rate_limit'
```

## HTTP Headers

### Headers'ı Göster
```bash
curl -I "https://api.genelpara.com/json/?list=doviz&sembol=USD"
```

### Rate Limit Headers
```bash
curl -s -D - "https://api.genelpara.com/json/?list=doviz&sembol=USD" | grep "X-RateLimit"
```

## Dosya İşlemleri

### Sonucu Dosyaya Kaydet
```bash
curl "https://api.genelpara.com/json/?list=doviz&sembol=all" -o rates.json
```

### Dosyadan Oku ve İşle
```bash
cat rates.json | jq '.data'
```

## Hata Yönetimi

### Timeout Ayarı
```bash
curl --max-time 10 "https://api.genelpara.com/json/?list=doviz&sembol=USD"
```

### Retry Mekanizması
```bash
curl --retry 3 --retry-delay 2 "https://api.genelpara.com/json/?list=doviz&sembol=USD"
```

### HTTP Status Kontrolü
```bash
curl -w "\n%{http_code}\n" "https://api.genelpara.com/json/?list=doviz&sembol=USD"
```

## Otomatik Güncelleme

### Her 5 Dakikada Güncelle (Linux/Mac)
```bash
watch -n 300 'curl -s "https://api.genelpara.com/json/?list=doviz&sembol=USD,EUR" | jq .'
```

### Cron ile Günlük Güncelleme
```bash
# Crontab'a ekle: Her gün 09:00'da çalıştır
0 9 * * * curl "https://api.genelpara.com/json/?list=doviz&sembol=all" -o /path/to/rates.json
```

## Örnekler

### 1. USD ve EUR Fiyatlarını Göster
```bash
curl -s "https://api.genelpara.com/json/?list=doviz&sembol=USD,EUR" | \
  jq '.data | to_entries | .[] | "\(.key): \(.value.satis) \(.value.sembol)"'
```

### 2. En Çok Yükselen Dövizi Bul
```bash
curl -s "https://api.genelpara.com/json/?list=doviz&sembol=all" | \
  jq '.data | to_entries | max_by(.value.oran | tonumber)'
```

### 3. CSV Formatına Çevir
```bash
curl -s "https://api.genelpara.com/json/?list=doviz&sembol=USD,EUR,GBP" | \
  jq -r '.data | to_entries | .[] | "\(.key),\(.value.satis),\(.value.degisim)"'
```

### 4. Rate Limit Kontrolü
```bash
REMAINING=$(curl -s "https://api.genelpara.com/json/?list=doviz&sembol=USD" | \
  jq '.rate_limit.remaining')
echo "Kalan istek: $REMAINING"
```

## PowerShell (Windows)

### Basit İstek
```powershell
Invoke-RestMethod -Uri "https://api.genelpara.com/json/?list=doviz&sembol=USD,EUR"
```

### Formatlanmış Çıktı
```powershell
$response = Invoke-RestMethod -Uri "https://api.genelpara.com/json/?list=doviz&sembol=USD"
$response.data.USD | Format-List
```

## İpuçları

1. **Rate Limit:** Günde 1000 istek limiti var, dikkatli kullanın
2. **Cache:** Mümkünse sonuçları cache'leyin (15 dakika)
3. **Error Handling:** HTTP status kodlarını kontrol edin
4. **Timeout:** 10 saniye timeout ayarlayın
5. **jq:** JSON işleme için jq kurun (https://stedolan.github.io/jq/)

## Kaynaklar

- API Dokümantasyonu: https://api.genelpara.com
- jq Tutorial: https://stedolan.github.io/jq/tutorial/
- cURL Dokümantasyonu: https://curl.se/docs/
