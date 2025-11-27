#!/usr/bin/env python3
"""
GenelPara API - Flask Web Uygulaması

Bu örnek, Flask kullanarak bir web arayüzü oluşturmayı gösterir.

Kurulum:
    pip install flask requests

Çalıştırma:
    python flask_app.py
    
Tarayıcıda açın:
    http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

API_URL = 'https://api.genelpara.com/json/'

def get_api_data(category, symbols='all'):
    """API'den veri çek"""
    try:
        params = {
            'list': category,
            'sembol': symbols
        }
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'success': False, 'error': str(e)}

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenelPara API - Flask Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        .controls {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        select, button {
            padding: 12px 20px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            margin-right: 10px;
        }
        button {
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: 600;
        }
        button:hover { background: #1e40af; }
        .rates-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }
        .rate-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left: 5px solid #2563eb;
        }
        .rate-card.up { border-left-color: #10b981; }
        .rate-card.down { border-left-color: #ef4444; }
        .symbol {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 15px;
        }
        .price {
            font-size: 2rem;
            color: #2563eb;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .change {
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 600;
        }
        .change.up { background: #d1fae5; color: #065f46; }
        .change.down { background: #fee2e2; color: #991b1b; }
        .info-box {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            text-align: center;
        }
        .loading {
            text-align: center;
            color: white;
            font-size: 1.5rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💱 Flask + GenelPara API Demo</h1>
        
        <div class="controls">
            <select id="category" onchange="loadRates()">
                <option value="doviz">Döviz</option>
                <option value="kripto">Kripto</option>
                <option value="altin">Altın</option>
            </select>
            <button onclick="loadRates()">🔄 Yenile</button>
            <span id="lastUpdate"></span>
        </div>
        
        <div id="content" class="rates-grid"></div>
        <div id="rateLimit" class="info-box" style="display: none;"></div>
    </div>

    <script>
        async function loadRates() {
            const category = document.getElementById('category').value;
            const content = document.getElementById('content');
            const rateLimitBox = document.getElementById('rateLimit');
            
            content.innerHTML = '<div class="loading">Yükleniyor...</div>';
            
            try {
                const response = await fetch(`/api/rates?category=${category}`);
                const data = await response.json();
                
                if (data.success) {
                    displayRates(data);
                    displayRateLimit(data.rate_limit);
                    updateTimestamp();
                } else {
                    content.innerHTML = `<div style="color: white;">Hata: ${data.error}</div>`;
                }
            } catch (error) {
                content.innerHTML = `<div style="color: white;">Hata: ${error.message}</div>`;
            }
        }
        
        function displayRates(data) {
            const content = document.getElementById('content');
            let html = '';
            
            for (const [symbol, info] of Object.entries(data.data)) {
                const direction = info.yon === 'moneyUp' ? 'up' : 
                                info.yon === 'moneyDown' ? 'down' : '';
                const arrow = direction === 'up' ? '↗' : 
                            direction === 'down' ? '↘' : '→';
                
                html += `
                    <div class="rate-card ${direction}">
                        <div class="symbol">${symbol}</div>
                        <div class="price">${parseFloat(info.satis).toFixed(4)} ${info.sembol}</div>
                        <span class="change ${direction}">
                            ${arrow} ${info.degisim} (${info.oran}%)
                        </span>
                    </div>
                `;
            }
            
            content.innerHTML = html;
        }
        
        function displayRateLimit(rateLimit) {
            const box = document.getElementById('rateLimit');
            box.style.display = 'block';
            box.innerHTML = `
                <strong>ℹ️ Rate Limit:</strong> 
                ${rateLimit.remaining}/${rateLimit.limit} istek kaldı
                <br>
                <small>Sıfırlanma: ${rateLimit.reset_at}</small>
            `;
        }
        
        function updateTimestamp() {
            const now = new Date();
            document.getElementById('lastUpdate').textContent = 
                `Son güncelleme: ${now.toLocaleTimeString('tr-TR')}`;
        }
        
        // Sayfa yüklendiğinde veri çek
        window.addEventListener('DOMContentLoaded', loadRates);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/rates')
def api_rates():
    """API endpoint - Kurları getir"""
    category = request.args.get('category', 'doviz')
    symbols = request.args.get('symbols', 'all')
    
    data = get_api_data(category, symbols)
    return jsonify(data)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  GenelPara API - Flask Demo")
    print("="*50)
    print("\n  🌐 Sunucu başlatılıyor...")
    print("  📍 URL: http://localhost:5000")
    print("\n  Ctrl+C ile durdurun\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
