// @ts-nocheck
"use client";

import React from "react";
import { useBatches, useCertificate, useComplianceCheck } from "@/hooks";

interface HookExampleProps {
  batchId?: string;
  certificateId?: string;
}

export default function HookExample({ batchId = "batch_001", certificateId = "cert_001" }: HookExampleProps) {
  // Exemplo de uso do hook useBatch
  const { batch, isLoading: batchLoading, error: batchError, refetch: refetchBatch } = useBatches(batchId, {
    enabled: true,
    refetchInterval: 0,
  });

  // Exemplo de uso do hook useCertificate
  const { 
    certificate, 
    onChainProof, 
    isLoading: certLoading, 
    error: certError, 
    refetch: refetchCert 
  } = useCertificate(certificateId, {
    enabled: true,
    includeProof: true,
  });

  // Exemplo de uso do hook useComplianceCheck
  const { 
    compliance, 
    isLoading: complianceLoading, 
    error: complianceError, 
    check: checkCompliance 
  } = useComplianceCheck(batchId, {
    enabled: true,
  });

  const handleRefreshAll = async () => {
    await Promise.all([
      refetchBatch(),
      refetchCert(),
      checkCompliance(),
    ]);
  };

  return (
    <div className="p-6 space-y-6 bg-card rounded-lg border shadow-sm">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Exemplo de Uso dos Hooks</h2>
        <button
          onClick={handleRefreshAll}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition"
        >
          Atualizar Todos
        </button>
      </div>

      {/* Seção Batch */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Hook: useBatch</h3>
        <div className="p-4 bg-muted rounded-md">
          {batchLoading ? (
            <p className="text-muted-foreground">Carregando batch...</p>
          ) : batchError ? (
            <p className="text-red-600">Erro: {batchError}</p>
          ) : batch ? (
            <div className="space-y-2">
              <p><strong>ID:</strong> {batch.id}</p>
              <p><strong>Tamanho:</strong> {batch.size_kg.toLocaleString()} kg</p>
              <p><strong>Produtor:</strong> {batch.producer_wallet || "Não especificado"}</p>
              <p><strong>Emissões:</strong> {batch.telemetry?.ghg_emissions?.toFixed(1)} kgCO₂e/kgH₂</p>
              <p><strong>Status:</strong> {batch.is_compliant ? "✅ Conforme" : "❌ Não Conforme"}</p>
            </div>
          ) : (
            <p className="text-muted-foreground">Nenhum batch encontrado</p>
          )}
        </div>
      </div>

      {/* Seção Certificate */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Hook: useCertificate</h3>
        <div className="p-4 bg-muted rounded-md">
          {certLoading ? (
            <p className="text-muted-foreground">Carregando certificado...</p>
          ) : certError ? (
            <p className="text-red-600">Erro: {certError}</p>
          ) : certificate ? (
            <div className="space-y-2">
              <p><strong>ID:</strong> {certificate.id}</p>
              <p><strong>Batch ID:</strong> {certificate.batch_id}</p>
              <p><strong>Emissões:</strong> {certificate.ghg_emissions?.toFixed(1)} kgCO₂e/kgH₂</p>
              <p><strong>Consumo de Água:</strong> {certificate.water_consumption?.toFixed(1)} L/kgH₂</p>
              <p><strong>Status:</strong> {certificate.is_compliant ? "✅ Conforme" : "❌ Não Conforme"}</p>
              {onChainProof && (
                <div className="mt-2 pt-2 border-t">
                  <p className="text-sm text-muted-foreground">
                    <strong>Prova On-Chain:</strong> Disponível
                  </p>
                </div>
              )}
            </div>
          ) : (
            <p className="text-muted-foreground">Nenhum certificado encontrado</p>
          )}
        </div>
      </div>

      {/* Seção Compliance */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Hook: useComplianceCheck</h3>
        <div className="p-4 bg-muted rounded-md">
          {complianceLoading ? (
            <p className="text-muted-foreground">Verificando conformidade...</p>
          ) : complianceError ? (
            <p className="text-red-600">Erro: {complianceError}</p>
          ) : compliance ? (
            <div className="space-y-2">
              <p><strong>Status:</strong> {compliance.is_compliant ? "✅ Conforme" : "❌ Não Conforme"}</p>
              {compliance.violations && compliance.violations.length > 0 && (
                <div className="mt-2">
                  <p className="font-medium text-red-600">Violações:</p>
                  <ul className="list-disc pl-5 text-sm text-red-600">
                    {compliance.violations.map((violation, index) => (
                      <li key={index}>{violation}</li>
                    ))}
                  </ul>
                </div>
              )}
              {compliance.checks && (
                <div className="mt-2 pt-2 border-t">
                  <p className="text-sm text-muted-foreground">
                    <strong>Checks realizados:</strong> {Object.keys(compliance.checks).length}
                  </p>
                </div>
              )}
            </div>
          ) : (
            <p className="text-muted-foreground">Nenhuma verificação de conformidade disponível</p>
          )}
        </div>
      </div>

      {/* Código de exemplo */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Como usar os hooks</h3>
        <div className="p-4 bg-muted rounded-md font-mono text-sm">
          <pre className="whitespace-pre-wrap">
{`// Importação dos hooks
import { useBatch, useCertificate, useComplianceCheck } from "@/hooks";

// Uso do hook useBatch
const { batch, isLoading, error, refetch } = useBatch("batch_id", {
  enabled: true,
  refetchInterval: 30000, // 30 segundos
});

// Uso do hook useCertificate
const { certificate, onChainProof, isLoading, error } = useCertificate("cert_id", {
  includeProof: true,
});

// Uso do hook useComplianceCheck
const { compliance, isLoading, error, check } = useComplianceCheck("batch_id");`}
          </pre>
        </div>
      </div>
    </div>
  );
}
