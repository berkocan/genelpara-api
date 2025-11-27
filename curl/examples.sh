#!/bin/bash
# GenelPara API - cURL Kullanım Örnekleri
# 
# Bu dosya, GenelPara API'sini cURL ile kullanmanın
# çeşitli yollarını gösterir.

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="https://api.genelpara.com/json/"

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   GenelPara API - cURL Kullanım Örnekleri     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}\n"

# Örnek 1: Basit istek
echo -e "${GREEN}📌 Örnek 1: Basit döviz kurları${NC}\n"
echo -e "${YELLOW}Komut:${NC}"
echo "curl \"${API_URL}?list=doviz&sembol=USD,EUR\""
echo -e "\n${YELLOW}Sonuç:${NC}"
curl -s "${API_URL}?list=doviz&sembol=USD,EUR" | python3 -m json.tool
echo -e "\n${BLUE}─────────────────────────────────────────────────${NC}\n"

# Örnek 2: Kripto paralar
echo -e "${GREEN}📌 Örnek 2: Kripto para fiyatları${NC}\n"
echo -e "${YELLOW}Komut:${NC}"
echo "curl \"${API_URL}?list=kripto&sembol=BTC,ETH,XRP\""
echo -e "\n${YELLOW}Sonuç:${NC}"
curl -s "${API_URL}?list=kripto&sembol=BTC,ETH,XRP" | python3 -m json.tool
echo -e "\n${BLUE}─────────────────────────────────────────────────${NC}\n"

# Örnek 3: Çoklu kategori
echo -e "${GREEN}📌 Örnek 3: Çoklu kategori sorgusu${NC}\n"
echo -e "${YELLOW}Komut:${NC}"
echo "curl \"${API_URL}?list=doviz,kripto,altin&sembol=USD,BTC,GA\""
echo -e "\n${YELLOW}Sonuç:${NC}"
curl -s "${API_URL}?list=doviz,kripto,altin&sembol=USD,BTC,GA" | python3 -m json.tool
echo -e "\n${BLUE}─────────────────────────────────────────────────${NC}\n"

# Örnek 4: Sadece belirli alanları göster (jq ile)
if command -v jq &> /dev/null; then
    echo -e "${GREEN}📌 Örnek 4: jq ile filtreleme${NC}\n"
    echo -e "${YELLOW}Komut:${NC}"
    echo "curl -s \"${API_URL}?list=doviz&sembol=USD\" | jq '.data.USD'"
    echo -e "\n${YELLOW}Sonuç:${NC}"
    curl -s "${API_URL}?list=doviz&sembol=USD" | jq '.data.USD'
    echo -e "\n${BLUE}─────────────────────────────────────────────────${NC}\n"
else
    echo -e "${RED}⚠️  jq yüklü değil, Örnek 4 atlandı${NC}\n"
fi

# Örnek 5: Headers göster
echo -e "${GREEN}📌 Örnek 5: HTTP headers${NC}\n"
echo -e "${YELLOW}Komut:${NC}"
echo "curl -I \"${API_URL}?list=doviz&sembol=USD\""
echo -e "\n${YELLOW}Sonuç:${NC}"
curl -sI "${API_URL}?list=doviz&sembol=USD"
echo -e "\n${BLUE}─────────────────────────────────────────────────${NC}\n"

# Örnek 6: Rate limit bilgisi
echo -e "${GREEN}📌 Örnek 6: Sadece rate limit bilgisi${NC}\n"
if command -v jq &> /dev/null; then
    echo -e "${YELLOW}Komut:${NC}"
    echo "curl -s \"${API_URL}?list=doviz&sembol=USD\" | jq '.rate_limit'"
    echo -e "\n${YELLOW}Sonuç:${NC}"
    curl -s "${API_URL}?list=doviz&sembol=USD" | jq '.rate_limit'
else
    echo -e "${YELLOW}Komut (jq olmadan):${NC}"
    echo "curl -s \"${API_URL}?list=doviz&sembol=USD\" | grep -o '\"rate_limit\":{[^}]*}'"
fi
echo -e "\n${BLUE}─────────────────────────────────────────────────${NC}\n"

# Örnek 7: Dosyaya kaydet
echo -e "${GREEN}📌 Örnek 7: Sonucu dosyaya kaydet${NC}\n"
echo -e "${YELLOW}Komut:${NC}"
echo "curl -s \"${API_URL}?list=doviz&sembol=all\" -o rates.json"
curl -s "${API_URL}?list=doviz&sembol=all" -o rates.json
echo -e "${GREEN}✅ Veriler rates.json dosyasına kaydedildi${NC}"
echo -e "\n${BLUE}─────────────────────────────────────────────────${NC}\n"

# Örnek 8: Timeout ayarı
echo -e "${GREEN}📌 Örnek 8: Timeout ayarlı istek${NC}\n"
echo -e "${YELLOW}Komut:${NC}"
echo "curl --max-time 10 \"${API_URL}?list=doviz&sembol=USD\""
echo -e "\n${YELLOW}Sonuç:${NC}"
curl -s --max-time 10 "${API_URL}?list=doviz&sembol=USD" | python3 -m json.tool
echo -e "\n${BLUE}─────────────────────────────────────────────────${NC}\n"

echo -e "${GREEN}✨ Tüm örnekler tamamlandı!${NC}\n"
