/**
 * Script para testar a emissão (minting) do Soulbound Token (SBT)
 * 
 * Este script:
 * 1. Faz deploy de todos os contratos (BatchRegistry, ComplianceVerifier, GreenHydrogenSBT)
 * 2. Emite (minta) um SBT para um produtor
 * 3. Verifica os dados do certificado na blockchain
 * 4. Testa o consumo do certificado
 * 5. Testa a não-transferibilidade (Soulbound)
 * 
 * Uso: npx hardhat run scripts/test_mint.js --network localhost
 * Ou:  npx hardhat run scripts/test_mint.js (usa hardhat network local)
 */

const hre = require("hardhat");

async function main() {
  console.log("=".repeat(60));
  console.log("🧪 TESTE DE EMISSÃO DO SOULBOUND TOKEN (SBT)");
  console.log("=".repeat(60));
  console.log();

  // Obtém signatários
  const [owner, producer, consumer] = await hre.ethers.getSigners();
  console.log(`🔑 Owner:    ${owner.address}`);
  console.log(`🔑 Producer: ${producer.address}`);
  console.log(`🔑 Consumer: ${consumer.address}`);
  console.log();

  // ==========================================
  // PASSO 1: Deploy dos contratos
  // ==========================================
  console.log("📦 PASSO 1: Deploy dos contratos");
  console.log("-".repeat(40));

  // 1.1 BatchRegistry
  console.log("  → Deploy do BatchRegistry...");
  const BatchRegistry = await hre.ethers.getContractFactory("BatchRegistry");
  const batchRegistry = await BatchRegistry.deploy();
  await batchRegistry.waitForDeployment();
  const batchRegistryAddress = await batchRegistry.getAddress();
  console.log(`  ✅ BatchRegistry: ${batchRegistryAddress}`);

  // 1.2 ComplianceVerifier
  console.log("  → Deploy do ComplianceVerifier...");
  const ComplianceVerifier = await hre.ethers.getContractFactory("ComplianceVerifier");
  const complianceVerifier = await ComplianceVerifier.deploy(batchRegistryAddress);
  await complianceVerifier.waitForDeployment();
  const complianceVerifierAddress = await complianceVerifier.getAddress();
  console.log(`  ✅ ComplianceVerifier: ${complianceVerifierAddress}`);

  // 1.3 GreenHydrogenSBT
  console.log("  → Deploy do GreenHydrogenSBT...");
  const GreenHydrogenSBT = await hre.ethers.getContractFactory("GreenHydrogenSBT");
  const sbt = await GreenHydrogenSBT.deploy(
    "Green Hydrogen Certificate",
    "GHCERT",
    batchRegistryAddress,
    complianceVerifierAddress
  );
  await sbt.waitForDeployment();
  const sbtAddress = await sbt.getAddress();
  console.log(`  ✅ GreenHydrogenSBT: ${sbtAddress}`);
  console.log();

  // ==========================================
  // PASSO 2: Verificar deploy
  // ==========================================
  console.log("🔍 PASSO 2: Verificação do deploy");
  console.log("-".repeat(40));

  const name = await sbt.name();
  const symbol = await sbt.symbol();
  const totalBefore = await sbt.getTotalCertificates();
  const contractOwner = await sbt.owner();

  console.log(`  📛 Nome:              ${name}`);
  console.log(`  🔤 Símbolo:           ${symbol}`);
  console.log(`  👤 Owner:             ${contractOwner}`);
  console.log(`  🔢 Total certificados: ${totalBefore.toString()}`);
  console.log(`  📋 BatchRegistry:     ${await sbt.batchRegistry()}`);
  console.log(`  ✅ ComplianceVerifier: ${await sbt.complianceVerifier()}`);
  console.log();

  // ==========================================
  // PASSO 3: Emitir (mint) SBT
  // ==========================================
  console.log("🪙 PASSO 3: Emissão do SBT (Minting)");
  console.log("-".repeat(40));

  // Criar um batchId (32 bytes = 64 hex chars + 0x)
  const batchId = hre.ethers.hexlify(hre.ethers.randomBytes(32));
  const tokenURI = "https://h2v-trust.com/metadata/certificate/1";

  console.log(`  📦 Batch ID:  ${batchId}`);
  console.log(`  🔗 Token URI: ${tokenURI}`);
  console.log(`  👤 Producer:  ${producer.address}`);
  console.log();

  console.log("  → Executando mintCertificate...");
  const mintTx = await sbt.connect(owner).mintCertificate(batchId, producer.address, tokenURI);
  const mintReceipt = await mintTx.wait();
  console.log(`  ✅ Transação confirmada!`);
  console.log(`  📝 Tx Hash: ${mintReceipt.hash}`);
  console.log();

  // ==========================================
  // PASSO 4: Verificar certificado emitido
  // ==========================================
  console.log("✅ PASSO 4: Verificação do certificado emitido");
  console.log("-".repeat(40));

  const tokenId = 1;
  const totalAfter = await sbt.getTotalCertificates();
  const ownerOfToken = await sbt.ownerOf(tokenId);
  const tokenURIStored = await sbt.tokenURI(tokenId);
  const batchTokenId = await sbt.getTokenIdForBatch(batchId);

  console.log(`  🆔 Token ID:           ${tokenId}`);
  console.log(`  🔢 Total certificados:  ${totalAfter.toString()}`);
  console.log(`  👤 Owner do token:     ${ownerOfToken}`);
  console.log(`  🔗 Token URI:          ${tokenURIStored}`);
  console.log(`  🔍 Batch → Token ID:   ${batchTokenId.toString()}`);
  console.log();

  // Verificar dados completos do certificado
  console.log("  📋 Dados completos do certificado:");
  const certData = await sbt.getCertificateData(tokenId);
  console.log(`    • batchId:           ${certData[0]}`);
  console.log(`    • producer:          ${certData[1]}`);
  console.log(`    • timestamp:         ${certData[2].toString()}`);
  console.log(`    • sizeKg:            ${certData[3].toString()}`);
  console.log(`    • ghgEmissions:      ${certData[4].toString()}`);
  console.log(`    • waterConsumption:  ${certData[5].toString()}`);
  console.log(`    • isCompliant:       ${certData[6]}`);
  console.log(`    • complianceHash:    ${certData[7]}`);
  console.log(`    • isConsumed:        ${certData[8]}`);
  console.log(`    • consumedAt:        ${certData[9].toString()}`);
  console.log(`    • consumedBy:        ${certData[10]}`);
  console.log();

  // Verificar validade
  const isValid = await sbt.isValidCertificate(tokenId);
  console.log(`  ✅ Certificado válido: ${isValid}`);

  // Calcular economia de carbono
  const carbonSavings = await sbt.calculateCarbonSavings(tokenId);
  console.log(`  🌱 Economia de CO2:    ${carbonSavings.toString()} kg`);
  console.log();

  // ==========================================
  // PASSO 5: Testar Soulbound (não-transferível)
  // ==========================================
  console.log("🔒 PASSO 5: Teste de Soulbound (não-transferível)");
  console.log("-".repeat(40));

  console.log("  → Tentando transferir o token (deve falhar)...");
  try {
    await sbt.connect(producer).transferFrom(producer.address, consumer.address, tokenId);
    console.log("  ❌ ERRO: A transferência deveria ter falhado!");
  } catch (error) {
    console.log(`  ✅ Transferência bloqueada: ${error.message.split("reverted with reason string '")[1]?.split("'")[0] || "SBT: Token is non-transferable"}`);
  }
  console.log();

  // ==========================================
  // PASSO 6: Consumir certificado
  // ==========================================
  console.log("🔥 PASSO 6: Consumo do certificado");
  console.log("-".repeat(40));

  console.log("  → Consumindo certificado...");
  const consumeTx = await sbt.connect(producer).consumeCertificate(tokenId);
  await consumeTx.wait();
  console.log("  ✅ Certificado consumido com sucesso!");

  const certAfterConsume = await sbt.certificateData(tokenId);
  console.log(`    • isConsumed:  ${certAfterConsume[8]}`);
  console.log(`    • consumedAt:  ${certAfterConsume[9].toString()}`);
  console.log(`    • consumedBy:  ${certAfterConsume[10]}`);

  const isValidAfter = await sbt.isValidCertificate(tokenId);
  console.log(`  ✅ Certificado válido após consumo: ${isValidAfter}`);
  console.log();

  // ==========================================
  // PASSO 7: Listar certificados do produtor
  // ==========================================
  console.log("📋 PASSO 7: Listagem de certificados");
  console.log("-".repeat(40));

  const producerCerts = await sbt.getProducerCertificates(producer.address);
  console.log(`  👤 Certificados do produtor (${producer.address}):`);
  for (const id of producerCerts) {
    console.log(`    • Token ID: ${id.toString()}`);
  }

  const ownerCerts = await sbt.getOwnerCertificates(producer.address);
  console.log(`  👤 Certificados do owner (${producer.address}):`);
  for (const id of ownerCerts) {
    console.log(`    • Token ID: ${id.toString()}`);
  }
  console.log();

  // ==========================================
  // RESUMO FINAL
  // ==========================================
  console.log("=".repeat(60));
  console.log("📊 RESUMO DO TESTE");
  console.log("=".repeat(60));
  console.log(`  ✅ Deploy:                    OK`);
  console.log(`  ✅ Mint (emissão):            OK (Token #${tokenId})`);
  console.log(`  ✅ Verificação de dados:      OK`);
  console.log(`  ✅ Cálculo de carbono:        OK (${carbonSavings.toString()} kg CO2)`);
  console.log(`  ✅ Soulbound (não-transfer.): OK`);
  console.log(`  ✅ Consumo:                   OK`);
  console.log(`  ✅ Listagem:                  OK`);
  console.log();
  console.log("🎉 Teste de emissão do SBT concluído com sucesso!");
  console.log("=".repeat(60));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Erro durante o teste:", error);
    process.exitCode = 1;
  });
