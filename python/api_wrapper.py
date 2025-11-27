#!/usr/bin/env python3
"""
GenelPara API - Python Class Wrapper

Bu örnek, API kullanımını kolaylaştıran bir Python class'ı gösterir.
"""

import requests
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
import time

class GenelParaAPI:
    """GenelPara API için Python wrapper"""
    
    def __init__(self, api_url: str = 'https://api.genelpara.com/json/'):
        self.api_url = api_url
        self.timeout = 10
        self.last_request_time = 0
        self.min_request_interval = 1  # Saniye cinsinden minimum istek aralığı
    
    def _wait_for_rate_limit(self):
        """Rate limit için bekleme"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def get_data(self, 
                 categories: str | List[str], 
                 symbols: str | List[str] = 'all') -> Optional[Dict[Any, Any]]:
        """
        API'den veri çek
        
        Args:
            categories: Kategori veya kategori listesi
            symbols: Sembol veya sembol listesi, ya da 'all'
        
        Returns:
            API yanıtı veya None
        """
        # Rate limit bekleme
        self._wait_for_rate_limit()
        
        # Liste ise string'e çevir
        if isinstance(categories, list):
            categories = ','.join(categories)
        if isinstance(symbols, list):
            symbols = ','.join(symbols)
        
        try:
            params = {
                'list': categories,
                'sembol': symbols
            }
            
            response = requests.get(
                self.api_url, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('success'):
                raise ValueError(f"API hatası: {data.get('error', 'Bilinmeyen')}")
            
            return data
        
        except requests.exceptions.RequestException as e:
            print(f"❌ İstek hatası: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse hatası: {e}")
            return None
        except ValueError as e:
            print(f"❌ {e}")
            return None
    
    def get_symbol(self, category: str, symbol: str) -> Optional[Dict[str, Any]]:
        """Tek bir sembolün verisini çek"""
        data = self.get_data(category, symbol)
        if data and symbol in data['data']:
            return data['data'][symbol]
        return None
    
    def get_all_symbols(self, category: str) -> Optional[Dict[str, Any]]:
        """Bir kategorideki tüm sembolleri çek"""
        return self.get_data(category, 'all')
    
    def get_rate_limit_info(self, data: Dict[Any, Any]) -> Dict[str, Any]:
        """Rate limit bilgisini al"""
        return data.get('rate_limit', {})
    
    def compare_symbols(self, category: str, symbols: List[str]) -> None:
        """Sembolleri karşılaştır ve göster"""
        data = self.get_data(category, symbols)
        
        if not data:
            print("Veri alınamadı!")
            return
        
        print(f"\n{'='*70}")
        print(f"  {category.upper()} KARŞILAŞTIRMASI")
        print(f"{'='*70}")
        print(f"{'Sembol':<10} {'Alış':>12} {'Satış':>12} {'Değişim':>12} {'Oran':>10}")
        print(f"{'-'*70}")
        
        for symbol in symbols:
            if symbol in data['data']:
                info = data['data'][symbol]
                print(f"{symbol:<10} "
                      f"{float(info['alis']):>12.4f} "
                      f"{float(info['satis']):>12.4f} "
                      f"{info['degisim']:>12s} "
                      f"{info['oran']:>10s}%")
        
        print(f"{'='*70}\n")
        
        # Rate limit bilgisi
        rl = self.get_rate_limit_info(data)
        print(f"⚡ Rate Limit: {rl.get('remaining', '?')}/{rl.get('limit', '?')} kaldı")

def main():
    """Kullanım örnekleri"""
    api = GenelParaAPI()
    
    # Örnek 1: Basit kullanım
    print("📊 Örnek 1: Döviz kurları\n")
    data = api.get_data('doviz', ['USD', 'EUR', 'GBP'])
    if data:
        for symbol, info in data['data'].items():
            print(f"{symbol}: {info['satis']} {info['sembol']}")
    
    print("\n" + "="*50 + "\n")
    
    # Örnek 2: Tek sembol
    print("📊 Örnek 2: Tek sembol sorgusu\n")
    btc = api.get_symbol('kripto', 'BTC')
    if btc:
        print(f"Bitcoin: ${btc['satis']}")
    
    print("\n" + "="*50 + "\n")
    
    # Örnek 3: Karşılaştırma
    print("📊 Örnek 3: Döviz karşılaştırma\n")
    api.compare_symbols('doviz', ['USD', 'EUR', 'GBP', 'JPY'])
    
    print("\n" + "="*50 + "\n")
    
    # Örnek 4: Çoklu kategori
    print("📊 Örnek 4: Çoklu kategori sorgusu\n")
    data = api.get_data(['doviz', 'kripto'], ['USD', 'EUR', 'BTC', 'ETH'])
    if data:
        # Kategorilere göre grupla
        by_category = {}
        for symbol, info in data['data'].items():
            category = info.get('_source', 'unknown')
            if category not in by_category:
                by_category[category] = {}
            by_category[category][symbol] = info
        
        for category, symbols in by_category.items():
            print(f"\n{category.upper()}:")
            for symbol, info in symbols.items():
                print(f"  {symbol}: {info['satis']} {info['sembol']}")

if __name__ == '__main__':
    main()
