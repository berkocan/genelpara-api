/**
 * GenelPara API - React Component Örneği
 * 
 * Bu örnek, React ile API kullanımını gösterir.
 */

import React, { useState, useEffect } from 'react';

const API_URL = 'https://api.genelpara.com/json/';

function CurrencyRates() {
    const [rates, setRates] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        fetchRates();
        
        // Her 5 dakikada bir güncelle
        const interval = setInterval(fetchRates, 5 * 60 * 1000);
        
        return () => clearInterval(interval);
    }, []);
    
    const fetchRates = async () => {
        try {
            setLoading(true);
            const params = new URLSearchParams({
                list: 'doviz',
                sembol: 'USD,EUR,GBP,JPY'
            });
            
            const response = await fetch(`${API_URL}?${params}`);
            
            if (!response.ok) {
                throw new Error('API isteği başarısız');
            }
            
            const data = await response.json();
            
            if (data.success) {
                setRates(data);
                setError(null);
            } else {
                throw new Error(data.error || 'Bilinmeyen hata');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };
    
    if (loading && !rates) {
        return <div className="loading">Yükleniyor...</div>;
    }
    
    if (error) {
        return <div className="error">Hata: {error}</div>;
    }
    
    return (
        <div className="currency-rates">
            <h1>💱 Döviz Kurları</h1>
            
            <div className="rates-grid">
                {rates && Object.entries(rates.data).map(([symbol, info]) => (
                    <div 
                        key={symbol} 
                        className={`rate-card ${info.yon}`}
                    >
                        <div className="symbol">{symbol}</div>
                        <div className="price">
                            {parseFloat(info.satis).toFixed(4)} {info.sembol}
                        </div>
                        <div className={`change ${info.yon}`}>
                            {info.oran} ({info.degisim}%)
                        </div>
                    </div>
                ))}
            </div>
            
            {rates && (
                <div className="rate-limit">
                    ℹ️ Kalan istek: {rates.rate_limit.remaining}/{rates.rate_limit.limit}
                </div>
            )}
            
            <button onClick={fetchRates} disabled={loading}>
                {loading ? 'Güncelleniyor...' : '🔄 Yenile'}
            </button>
        </div>
    );
}

export default CurrencyRates;

// CSS (ayrı dosya olarak kaydedin: CurrencyRates.css)
const styles = `
.currency-rates {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.rates-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.rate-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-left: 4px solid #2563eb;
}

.rate-card.moneyUp { border-left-color: #10b981; }
.rate-card.moneyDown { border-left-color: #ef4444; }

.symbol {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.price {
    font-size: 2rem;
    color: #2563eb;
    font-weight: 700;
}

.change {
    font-size: 0.875rem;
    padding: 4px 12px;
    border-radius: 6px;
    display: inline-block;
    margin-top: 10px;
}

.change.moneyUp {
    background: #d1fae5;
    color: #065f46;
}

.change.moneyDown {
    background: #fee2e2;
    color: #991b1b;
}

.rate-limit {
    background: #dbeafe;
    padding: 15px;
    border-radius: 8px;
    margin: 20px 0;
}

button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
}

button:hover {
    background: #1e40af;
}

button:disabled {
    background: #94a3b8;
    cursor: not-allowed;
}
`;
