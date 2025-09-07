#!/usr/bin/env python3
"""
Setup Test Script

Bu script .env dosyasının doğru yapılandırılıp yapılandırılmadığını kontrol eder.
"""

import os
import sys
from dotenv import load_dotenv

def test_env_setup():
    """Test .env file setup."""
    print("🔧 Testing .env Setup...")
    print("=" * 50)
    
    # Load .env file
    load_dotenv()
    
    # Required variables
    required_vars = [
        'BINANCE_API_KEY',
        'BINANCE_API_SECRET', 
        'ODOS_API_KEY',
        'SMART_CONTRACT_RPC_URL',
        'WALLET_ADDRESS',
        'PRIVATE_KEY'
    ]
    
    # Optional variables
    optional_vars = [
        'SMART_CONTRACT_ADDRESS',
        'ETHERSCAN_API_KEY'
    ]
    
    print("📋 Required Variables:")
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            print(f"✅ {var}: {'*' * min(len(value), 10)}...")
        else:
            print(f"❌ {var}: Not set or using default value")
            all_good = False
    
    print("\n📋 Optional Variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            print(f"✅ {var}: {'*' * min(len(value), 10)}...")
        else:
            print(f"⚠️  {var}: Not set (optional)")
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All required variables are set!")
        print("✅ You can now run the trading system!")
    else:
        print("❌ Some required variables are missing!")
        print("📝 Please update your .env file with real values.")
    
    return all_good

def test_imports():
    """Test if all required modules can be imported."""
    print("\n🧪 Testing Imports...")
    print("=" * 50)
    
    try:
        from src.business_service import BusinessService
        print("✅ BusinessService imported successfully")
    except Exception as e:
        print(f"❌ BusinessService import failed: {e}")
        return False
    
    try:
        from src.odos_client import OdosClient
        print("✅ OdosClient imported successfully")
    except Exception as e:
        print(f"❌ OdosClient import failed: {e}")
        return False
    
    try:
        from src.contract_listener import SmartContractListener
        print("✅ SmartContractListener imported successfully")
    except Exception as e:
        print(f"❌ SmartContractListener import failed: {e}")
        return False
    
    print("✅ All imports successful!")
    return True

def main():
    """Main test function."""
    print("🚀 Trading System Setup Test")
    print("=" * 60)
    
    env_ok = test_env_setup()
    imports_ok = test_imports()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    if env_ok and imports_ok:
        print("🎉 Everything is ready!")
        print("✅ You can now run: python3 main.py")
    else:
        print("⚠️  Some issues found.")
        print("📝 Please fix the issues above before running the system.")
    
    return env_ok and imports_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
