# 🚀 Trading System Setup Guide

## 📋 Doldurulması Gereken Alanlar

### 1. .env Dosyasını Düzenle

```bash
# .env dosyasını açın ve şu alanları doldurun:
```

#### 🔑 Binance Testnet API
1. https://testnet.binance.vision/ adresine gidin
2. API Management > Create API
3. API Key ve Secret'i kopyalayın
4. .env dosyasında güncelleyin:
   ```bash
   BINANCE_API_KEY=gerçek_api_key
   BINANCE_API_SECRET=gerçek_api_secret
   ```

#### 🦄 ODOS API
1. https://odos.xyz/ adresine gidin
2. Sign up / Login yapın
3. API Keys bölümünden key alın
4. .env dosyasında güncelleyin:
   ```bash
   ODOS_API_KEY=gerçek_odos_key
   ```

#### �� Ethereum Testnet RPC
1. https://infura.io/ veya https://alchemy.com/ adresine gidin
2. Proje oluşturun
3. Sepolia testnet RPC URL'ini alın
4. .env dosyasında güncelleyin:
   ```bash
   SMART_CONTRACT_RPC_URL=https://sepolia.infura.io/v3/GERÇEK_PROJECT_ID
   ```

#### 💰 Wallet Bilgileri
1. MetaMask'tan testnet wallet oluşturun
2. Private key'i export edin (testnet için güvenli)
3. .env dosyasında güncelleyin:
   ```bash
   WALLET_ADDRESS=0x...
   PRIVATE_KEY=0x...
   ```

### 2. Smart Contract Deploy Et

```bash
# Contracts klasörüne gidin
cd contracts

# Dependencies yükleyin
npm install

# Contract'ı compile edin
npm run compile

# Sepolia testnet'e deploy edin
npm run deploy:sepolia

# Deploy edilen adresi .env dosyasına ekleyin
SMART_CONTRACT_ADDRESS=0x...
```

### 3. Sistemi Test Et

```bash
# Ana dizine dönün
cd ..

# Setup testini çalıştırın
python3 test_setup.py

# Eğer her şey OK ise, sistemi başlatın
python3 main.py
```

## 🎯 Test Senaryoları

### 1. Manual Event Test
```python
# examples/cex_transaction_example.py çalıştır
python3 examples/cex_transaction_example.py
```

### 2. Comprehensive Test
```python
# Kapsamlı testleri çalıştır
python3 tests/test_comprehensive.py
```

### 3. Contract Event Test
```javascript
// Contract'tan event emit et
await contract.emitCexSignal(
    web3.utils.toWei("0.1", "ether"),
    web3.utils.toWei("2000", "ether"),
    "ETH",
    "buy"
);
```

## 🔧 Troubleshooting

### API Key Hataları
- Binance testnet API key'inin doğru olduğundan emin olun
- API permissions'ları kontrol edin (Spot trading enabled)

### Contract Connection Hataları
- RPC URL'in doğru olduğundan emin olun
- Contract address'in doğru olduğundan emin olun
- Wallet'ın testnet'te olduğundan emin olun

### ODOS API Hataları
- API key'in doğru olduğundan emin olun
- Rate limit'leri kontrol edin

## 📊 Sistem Durumu

- ✅ Event Parsing: Çalışıyor
- ✅ Risk Management: Çalışıyor  
- ✅ CEX Execution: Çalışıyor
- ✅ DEX Execution: Çalışıyor
- ✅ Contract Events: Çalışıyor
- ✅ Test System: Çalışıyor

## 🚀 Production'a Geçiş

1. Testnet'te her şeyi test edin
2. Mainnet API key'lerini alın
3. Mainnet contract deploy edin
4. .env dosyasını mainnet için güncelleyin
5. Sistemi mainnet'te çalıştırın

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. `python3 test_setup.py` çalıştırın
2. Hata mesajlarını kontrol edin
3. .env dosyasını tekrar kontrol edin
4. Log dosyalarını inceleyin
