const { ethers } = require('ethers');
require('dotenv').config();

async function main() {
  const provider = new ethers.JsonRpcProvider(process.env.POLYGON_RPC_URL || 'https://rpc-amoy.polygon.technology');
  const privateKey = process.env.PRIVATE_KEY || '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80';
  const wallet = new ethers.Wallet(privateKey, provider);

  console.log('Verificando conexão com Polygon Amoy Testnet...');
  console.log('Endereço da carteira:', wallet.address);
  
  try {
    const balance = await provider.getBalance(wallet.address);
    console.log('Saldo:', ethers.formatEther(balance), 'MATIC');
    
    const network = await provider.getNetwork();
    console.log('Rede:', network.name, 'Chain ID:', network.chainId);
    
    if (balance === 0n) {
      console.log('\n⚠️ ATENÇÃO: A carteira não tem MATIC na Polygon Amoy Testnet.');
      console.log('Para obter MATIC de teste, visite: https://faucet.polygon.technology/');
      console.log('Selecione "Polygon Amoy" e cole seu endereço:', wallet.address);
    } else {
      console.log('\n✅ Carteira tem fundos para implantação!');
    }
  } catch (error) {
    console.error('Erro:', error.message);
    console.log('Verifique sua conexão com a internet ou a URL do RPC.');
  }
}

main().catch(console.error);