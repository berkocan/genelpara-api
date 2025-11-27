#!/usr/bin/env python3
"""
GenelPara API - Python Basit Kullanım Örneği

Bu örnek, GenelPara API'sini kullanarak döviz ve kripto para
fiyatlarını çekmeyi gösterir.
"""

import requests
import json
from typing import Optional, Dict, Any

API_URL = 'https://api.genelpara.com/json/'

def get_rates(list_type: str, symbols: str) -> Optional[Dict[Any, Any]]:
    """
    API'den veri çek
    
    Args:
        list_type: Kategori (doviz, kripto, altin, vb.)
        symbols: Sembol listesi (virgülle ayrılmış) veya 'all'
    
    Returns:
        API yanıtı veya None
    """
    try:
        params = {
            'list': list_type,
            'sembol': symbols
        }
        
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"❌ API isteği başarısız: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse hatası: {e}")
        return None

def display_rates(data: Dict[Any, Any]) -> None:
    """Verileri formatlı olarak göster"""
    
    if not data or not data.get('success'):
        print(f"❌ API hatası: {data.get('error', 'Bilinmeyen hata')}")
        return
    
    print("\n=== DÖVİZ KURLARI ===\n")
    
    for symbol, info in data['data'].items():
        arrow = '↗' if info['yon'] == 'moneyUp' else '↘' if info['yon'] == 'moneyDown' else '→'
        
        print(f"{symbol:6s}: {float(info['satis']):>10.4f} {info['sembol']} "
              f"{arrow} {info['degisim']:>8s} ({info['oran']:>6s}%)")
    
    print("\n=== RATE LIMIT ===")
    rate_limit = data['rate_limit']
    print(f"Kalan: {rate_limit['remaining']}/{rate_limit['limit']}")
    print(f"Sıfırlanma: {rate_limit['reset_at']}")

def main():
    """Ana fonksiyon"""
    print("GenelPara API'den veri çekiliyor...\n")
    
    # Döviz kurlarını çek
    data = get_rates('doviz', 'USD,EUR,GBP,JPY')
    
    if data:
        display_rates(data)

if __name__ == '__main__':
    main()
