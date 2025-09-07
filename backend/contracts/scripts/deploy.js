// Deployment script for TradingSignalContract
// Run with: node deploy.js

const Web3 = require('web3');
const fs = require('fs');
const path = require('path');

// Configuration
const RPC_URL = process.env.SMART_CONTRACT_RPC_URL || 'https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID';
const PRIVATE_KEY = process.env.PRIVATE_KEY || 'your_private_key_here';

// Contract ABI (minimal for deployment)
const contractABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "string",
                "name": "exType",
                "type": "string"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "quantity",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "expectedPrice",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "string",
                "name": "pair",
                "type": "string"
            },
            {
                "indexed": false,
                "internalType": "string",
                "name": "side",
                "type": "string"
            }
        ],
        "name": "TradingSignal",
        "type": "event"
    }
];

// Contract bytecode (you'll need to compile the contract first)
const contractBytecode = '0x608060405234801561001057600080fd5b506...'; // Replace with actual bytecode

async function deployContract() {
    try {
        // Initialize Web3
        const web3 = new Web3(RPC_URL);
        
        // Create account from private key
        const account = web3.eth.accounts.privateKeyToAccount(PRIVATE_KEY);
        web3.eth.accounts.wallet.add(account);
        
        console.log('🚀 Deploying TradingSignalContract...');
        console.log('📍 Deployer address:', account.address);
        console.log('🌐 RPC URL:', RPC_URL);
        
        // Create contract instance
        const contract = new web3.eth.Contract(contractABI);
        
        // Deploy contract
        const deployTx = contract.deploy({
            data: contractBytecode,
            arguments: []
        });
        
        // Estimate gas
        const gasEstimate = await deployTx.estimateGas({ from: account.address });
        console.log('⛽ Estimated gas:', gasEstimate);
        
        // Send transaction
        const deployedContract = await deployTx.send({
            from: account.address,
            gas: gasEstimate,
            gasPrice: await web3.eth.getGasPrice()
        });
        
        console.log('✅ Contract deployed successfully!');
        console.log('📍 Contract address:', deployedContract.options.address);
        console.log('🔗 Transaction hash:', deployedContract.transactionHash);
        
        // Save contract info
        const contractInfo = {
            address: deployedContract.options.address,
            transactionHash: deployedContract.transactionHash,
            blockNumber: deployedContract.options.address,
            abi: contractABI,
            deployer: account.address,
            network: RPC_URL,
            deployedAt: new Date().toISOString()
        };
        
        fs.writeFileSync(
            path.join(__dirname, 'deployed-contract.json'),
            JSON.stringify(contractInfo, null, 2)
        );
        
        console.log('💾 Contract info saved to deployed-contract.json');
        
        return contractInfo;
        
    } catch (error) {
        console.error('❌ Deployment failed:', error.message);
        process.exit(1);
    }
}

// Run deployment
deployContract();
