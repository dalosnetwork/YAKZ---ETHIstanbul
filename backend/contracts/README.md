# Trading Signal Contract

Bu akıllı kontrat, trading sinyalleri emit etmek için kullanılır. Python trading bot'u bu kontratı dinleyerek otomatik trading yapar.

## 🚀 Kurulum

```bash
# Dependencies yükle
npm install

# Contract'ı compile et
npm run compile

# .env dosyasını düzenle
cp ../.env .env
```

## 📝 .env Dosyasını Düzenle

```bash
# Ethereum Testnet RPC
SMART_CONTRACT_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID

# Private key (testnet için)
PRIVATE_KEY=your_private_key_here

# Etherscan API key (verification için)
ETHERSCAN_API_KEY=your_etherscan_api_key
```

## 🚀 Deployment

```bash
# Sepolia testnet'e deploy et
npm run deploy:sepolia

# Goerli testnet'e deploy et  
npm run deploy:goerli

# Local network'e deploy et
npm run deploy:local
```

## 📋 Contract Fonksiyonları

### Trading Signal Emit Etme

```javascript
// CEX signal
await contract.emitCexSignal(
    web3.utils.toWei("0.1", "ether"), // 0.1 ETH
    web3.utils.toWei("2000", "ether"), // $2000
    "ETH",
    "buy"
);

// DEX signal
await contract.emitDexSignal(
    web3.utils.toWei("1.0", "ether"), // 1.0 SOL
    web3.utils.toWei("50", "ether"), // $50
    "SOL", 
    "sell"
);
```

### Admin Fonksiyonları

```javascript
// Authorized caller ekle
await contract.addAuthorizedCaller("0x...");

// Trading limits güncelle
await contract.updateTradingLimits(
    web3.utils.toWei("0.001", "ether"), // min
    web3.utils.toWei("1000", "ether")   // max
);
```

## 🔗 Python Bot ile Entegrasyon

Contract deploy edildikten sonra, Python bot'unda şu ayarları yapın:

```python
# config/settings.py
SMART_CONTRACT_ADDRESS = "0x..." # Deploy edilen adres
SMART_CONTRACT_RPC_URL = "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"
```

## 🧪 Test

```bash
# Testleri çalıştır
npm test

# Contract'ı verify et
npm run verify
```

## 📊 Event Monitoring

Contract'ı dinlemek için:

```javascript
// TradingSignal event'ini dinle
contract.events.TradingSignal({
    fromBlock: 'latest'
}, (error, event) => {
    console.log('Trading Signal:', event.returnValues);
});
```
