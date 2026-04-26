const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GreenHydrogenSBT", function () {
  let GreenHydrogenSBT;
  let BatchRegistry;
  let ComplianceVerifier;
  let sbt;
  let batchRegistry;
  let complianceVerifier;
  let owner;
  let producer;
  let consumer;
  let other;

  beforeEach(async function () {
    [owner, producer, consumer, other] = await ethers.getSigners();

    // Deploy BatchRegistry
    BatchRegistry = await ethers.getContractFactory("BatchRegistry");
    batchRegistry = await BatchRegistry.deploy();
    await batchRegistry.waitForDeployment();

    // Deploy ComplianceVerifier
    ComplianceVerifier = await ethers.getContractFactory("ComplianceVerifier");
    complianceVerifier = await ComplianceVerifier.deploy(await batchRegistry.getAddress());
    await complianceVerifier.waitForDeployment();

    // Deploy GreenHydrogenSBT with constructor params
    GreenHydrogenSBT = await ethers.getContractFactory("GreenHydrogenSBT");
    sbt = await GreenHydrogenSBT.deploy(
      "Green Hydrogen Certificate",
      "GHCERT",
      await batchRegistry.getAddress(),
      await complianceVerifier.getAddress()
    );
    await sbt.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should deploy with correct name and symbol", async function () {
      expect(await sbt.name()).to.equal("Green Hydrogen Certificate");
      expect(await sbt.symbol()).to.equal("GHCERT");
    });

    it("Should set the right owner", async function () {
      expect(await sbt.owner()).to.equal(owner.address);
    });

    it("Should initialize token counter at 0", async function () {
      expect(await sbt.getTotalCertificates()).to.equal(0);
    });

    it("Should set batch registry and compliance verifier", async function () {
      expect(await sbt.batchRegistry()).to.equal(await batchRegistry.getAddress());
      expect(await sbt.complianceVerifier()).to.equal(await complianceVerifier.getAddress());
    });
  });

  describe("Minting", function () {
    const batchIdHex = "0x" + "ab".repeat(32); // 32 bytes hex
    const tokenURI = "https://example.com/token/1";

    it("Should mint a new certificate", async function () {
      await expect(
        sbt.connect(owner).mintCertificate(batchIdHex, producer.address, tokenURI)
      ).to.emit(sbt, "CertificateMinted");

      const tokenId = 1;
      expect(await sbt.ownerOf(tokenId)).to.equal(producer.address);
      expect(await sbt.tokenURI(tokenId)).to.equal(tokenURI);
      expect(await sbt.batchToTokenId(batchIdHex)).to.equal(tokenId);

      const cert = await sbt.certificateData(tokenId);
      expect(cert.batchId).to.equal(batchIdHex);
      expect(cert.producer).to.equal(producer.address);
      expect(cert.isCompliant).to.equal(true);
      expect(cert.isConsumed).to.equal(false);
    });

    it("Should increment token counter after minting", async function () {
      await sbt.connect(owner).mintCertificate(batchIdHex, producer.address, tokenURI);
      expect(await sbt.getTotalCertificates()).to.equal(1);
    });

    it("Should fail if minting from non-owner", async function () {
      await expect(
        sbt.connect(producer).mintCertificate(batchIdHex, producer.address, tokenURI)
      ).to.be.revertedWithCustomError(sbt, "OwnableUnauthorizedAccount");
    });

    it("Should fail if batch already has a certificate", async function () {
      await sbt.connect(owner).mintCertificate(batchIdHex, producer.address, tokenURI);
      await expect(
        sbt.connect(owner).mintCertificate(batchIdHex, producer.address, tokenURI)
      ).to.be.revertedWith("Certificate already minted for this batch");
    });

    it("Should fail with invalid producer address", async function () {
      await expect(
        sbt.connect(owner).mintCertificate(batchIdHex, ethers.ZeroAddress, tokenURI)
      ).to.be.revertedWith("Invalid producer address");
    });

    it("Should mint multiple certificates for different batches", async function () {
      const batchId2 = "0x" + "cd".repeat(32);
      const batchId3 = "0x" + "ef".repeat(32);

      await sbt.connect(owner).mintCertificate(batchIdHex, producer.address, tokenURI);
      await sbt.connect(owner).mintCertificate(batchId2, producer.address, tokenURI + "2");
      await sbt.connect(owner).mintCertificate(batchId3, consumer.address, tokenURI + "3");

      expect(await sbt.getTotalCertificates()).to.equal(3);
      expect(await sbt.ownerOf(1)).to.equal(producer.address);
      expect(await sbt.ownerOf(2)).to.equal(producer.address);
      expect(await sbt.ownerOf(3)).to.equal(consumer.address);
    });
  });

  describe("Consumption", function () {
    const batchIdHex = "0x" + "ab".repeat(32);
    const tokenURI = "https://example.com/token/1";

    beforeEach(async function () {
      await sbt.connect(owner).mintCertificate(batchIdHex, producer.address, tokenURI);
    });

    it("Should consume a certificate", async function () {
      const tokenId = 1;
      await expect(
        sbt.connect(producer).consumeCertificate(tokenId)
      ).to.emit(sbt, "CertificateConsumed");

      const cert = await sbt.certificateData(tokenId);
      expect(cert.isConsumed).to.equal(true);
      expect(cert.consumedBy).to.equal(producer.address);
      expect(cert.consumedAt).to.be.gt(0);
    });

    it("Should fail if consuming from non-owner", async function () {
      const tokenId = 1;
      await expect(
        sbt.connect(consumer).consumeCertificate(tokenId)
      ).to.be.revertedWith("Not token owner");
    });

    it("Should fail if certificate already consumed", async function () {
      const tokenId = 1;
      await sbt.connect(producer).consumeCertificate(tokenId);
      await expect(
        sbt.connect(producer).consumeCertificate(tokenId)
      ).to.be.revertedWith("Certificate already consumed");
    });

    it("Should fail if token does not exist", async function () {
      await expect(
        sbt.connect(producer).consumeCertificate(999)
      ).to.be.revertedWith("Token does not exist");
    });
  });

  describe("Verification", function () {
    const batchIdHex = "0x" + "ab".repeat(32);
    const tokenURI = "https://example.com/token/1";

    beforeEach(async function () {
      await sbt.connect(owner).mintCertificate(batchIdHex, producer.address, tokenURI);
    });

    it("Should verify certificate exists via ownerOf", async function () {
      expect(await sbt.ownerOf(1)).to.equal(producer.address);
    });

    it("Should get certificate data", async function () {
      const data = await sbt.getCertificateData(1);
      expect(data[0]).to.equal(batchIdHex);      // batchId
      expect(data[1]).to.equal(producer.address); // producer
      expect(data[6]).to.equal(true);             // isCompliant
      expect(data[8]).to.equal(false);            // isConsumed
    });

    it("Should get token ID for batch", async function () {
      expect(await sbt.getTokenIdForBatch(batchIdHex)).to.equal(1);
    });

    it("Should return 0 for non-existent batch", async function () {
      const nonExistentBatch = "0x" + "ff".repeat(32);
      expect(await sbt.getTokenIdForBatch(nonExistentBatch)).to.equal(0);
    });

    it("Should verify certificate is valid", async function () {
      expect(await sbt.isValidCertificate(1)).to.equal(true);
    });

    it("Should verify certificate is not valid after consumption", async function () {
      await sbt.connect(producer).consumeCertificate(1);
      expect(await sbt.isValidCertificate(1)).to.equal(false);
    });

    it("Should calculate carbon savings", async function () {
      // sizeKg=1000, ghgEmissions=2500 (2.5 kgCO2e/kgH2)
      // grey hydrogen = 10000 (10 kgCO2e/kgH2)
      // savings = (10000 - 2500) * 1000 / 1000 = 7500
      const savings = await sbt.calculateCarbonSavings(1);
      expect(savings).to.equal(7500);
    });
  });

  describe("Batch operations", function () {
    const batchId1 = "0x" + "ab".repeat(32);
    const batchId2 = "0x" + "cd".repeat(32);
    const tokenURI = "https://example.com/token/";

    beforeEach(async function () {
      await sbt.connect(owner).mintCertificate(batchId1, producer.address, tokenURI + "1");
      await sbt.connect(owner).mintCertificate(batchId2, producer.address, tokenURI + "2");
    });

    it("Should get certificates by producer", async function () {
      const certs = await sbt.getProducerCertificates(producer.address);
      expect(certs.length).to.equal(2);
      expect(certs[0]).to.equal(1);
      expect(certs[1]).to.equal(2);
    });

    it("Should get certificates by owner", async function () {
      const certs = await sbt.getOwnerCertificates(producer.address);
      expect(certs.length).to.equal(2);
      expect(certs[0]).to.equal(1);
      expect(certs[1]).to.equal(2);
    });

    it("Should return empty array for producer with no certificates", async function () {
      const certs = await sbt.getProducerCertificates(consumer.address);
      expect(certs.length).to.equal(0);
    });
  });

  describe("Admin functions", function () {
    it("Should update batch registry", async function () {
      const newRegistry = ethers.Wallet.createRandom().address;
      await sbt.connect(owner).updateBatchRegistry(newRegistry);
      expect(await sbt.batchRegistry()).to.equal(newRegistry);
    });

    it("Should fail to update batch registry from non-owner", async function () {
      const newRegistry = ethers.Wallet.createRandom().address;
      await expect(
        sbt.connect(producer).updateBatchRegistry(newRegistry)
      ).to.be.revertedWithCustomError(sbt, "OwnableUnauthorizedAccount");
    });

    it("Should update compliance verifier", async function () {
      const newVerifier = ethers.Wallet.createRandom().address;
      await sbt.connect(owner).updateComplianceVerifier(newVerifier);
      expect(await sbt.complianceVerifier()).to.equal(newVerifier);
    });

    it("Should fail to update compliance verifier from non-owner", async function () {
      const newVerifier = ethers.Wallet.createRandom().address;
      await expect(
        sbt.connect(producer).updateComplianceVerifier(newVerifier)
      ).to.be.revertedWithCustomError(sbt, "OwnableUnauthorizedAccount");
    });

    it("Should fail to set invalid batch registry", async function () {
      await expect(
        sbt.connect(owner).updateBatchRegistry(ethers.ZeroAddress)
      ).to.be.revertedWith("Invalid registry address");
    });

    it("Should fail to set invalid compliance verifier", async function () {
      await expect(
        sbt.connect(owner).updateComplianceVerifier(ethers.ZeroAddress)
      ).to.be.revertedWith("Invalid verifier address");
    });
  });

  describe("SBT properties (non-transferable)", function () {
    const batchIdHex = "0x" + "ab".repeat(32);
    const tokenURI = "https://example.com/token/1";

    beforeEach(async function () {
      await sbt.connect(owner).mintCertificate(batchIdHex, producer.address, tokenURI);
    });

    it("Should not allow transfers from regular users", async function () {
      const tokenId = 1;
      await expect(
        sbt.connect(producer).transferFrom(producer.address, consumer.address, tokenId)
      ).to.be.revertedWith("SBT: Token is non-transferable");
    });

    it("Should not allow safeTransferFrom from regular users", async function () {
      const tokenId = 1;
      await expect(
        sbt.connect(producer)["safeTransferFrom(address,address,uint256)"](
          producer.address, consumer.address, tokenId
        )
      ).to.be.revertedWith("SBT: Token is non-transferable");
    });

    it("Should allow owner to transfer (migration)", async function () {
      const tokenId = 1;
      // Owner needs to approve themselves first for ERC721 transferFrom
      await sbt.connect(producer).approve(owner.address, tokenId);
      await sbt.connect(owner).transferFrom(producer.address, consumer.address, tokenId);
      expect(await sbt.ownerOf(tokenId)).to.equal(consumer.address);
    });

    it("Should update owner certificates mapping after owner transfer", async function () {
      const tokenId = 1;
      // Owner needs to approve themselves first for ERC721 transferFrom
      await sbt.connect(producer).approve(owner.address, tokenId);
      await sbt.connect(owner).transferFrom(producer.address, consumer.address, tokenId);
      
      const producerCerts = await sbt.getOwnerCertificates(producer.address);
      expect(producerCerts.length).to.equal(0);
      
      const consumerCerts = await sbt.getOwnerCertificates(consumer.address);
      expect(consumerCerts.length).to.equal(1);
      expect(consumerCerts[0]).to.equal(1);
    });
  });

  describe("Edge cases", function () {
    it("Should handle empty bytes32 batch ID", async function () {
      const emptyBatch = "0x" + "00".repeat(32);
      await sbt.connect(owner).mintCertificate(emptyBatch, producer.address, "uri");
      expect(await sbt.getTokenIdForBatch(emptyBatch)).to.equal(1);
    });

    it("Should handle very long token URI", async function () {
      const longURI = "https://example.com/" + "a".repeat(2000);
      await sbt.connect(owner).mintCertificate(
        "0x" + "ab".repeat(32),
        producer.address,
        longURI
      );
      expect(await sbt.tokenURI(1)).to.equal(longURI);
    });

    it("Should revert on non-existent token data query", async function () {
      await expect(
        sbt.getCertificateData(999)
      ).to.be.revertedWith("Token does not exist");
    });

    it("Should revert isValidCertificate for non-existent token", async function () {
      await expect(
        sbt.isValidCertificate(999)
      ).to.be.revertedWith("Token does not exist");
    });

    it("Should revert calculateCarbonSavings for non-existent token", async function () {
      await expect(
        sbt.calculateCarbonSavings(999)
      ).to.be.revertedWith("Token does not exist");
    });
  });
});
