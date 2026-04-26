"use client";

import { useState } from "react";
import { CheckCircle, XCircle, Cloud, Droplets, Zap, Search, FileText } from "lucide-react";
import { useBatchDetail, useBatchCompliance } from "@/hooks/useBatch";
import LoadingSpinner from "@/components/shared/LoadingSpinner";

interface BatchVerificationProps {
  batchId?: string;
  onVerify?: (batchId: string, isCompliant: boolean) => void;
}

export default function BatchVerification({ batchId: initialBatchId, onVerify }: BatchVerificationProps) {
  const [batchId, setBatchId] = useState(initialBatchId || "");
  const [searchId, setSearchId] = useState(initialBatchId || "");
  
  const { batch, isLoading: batchLoading, error: batchError } = useBatchDetail(searchId);
  const { compliance, isLoading: complianceLoading } = useBatchCompliance(searchId);

  const handleSearch = () => {
    setSearchId(batchId);
  };

  const handleVerify = () => {
    if (batch && onVerify) {
      onVerify(batch.id, batch.is_compliant);
    }
  };

  return (
    <div className="space-y-6">
      {/* Search */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Digite o ID do lote para verificar..."
          className="flex-1 border rounded-md px-4 py-2 bg-background"
          value={batchId}
          onChange={(e) => setBatchId(e.target.value)}
        />
        <button
          onClick={handleSearch}
          disabled={!batchId || batchLoading}
          className="bg-primary text-primary-foreground px-6 py-2 rounded-md hover:bg-primary/90 transition disabled:opacity-50 flex items-center gap-2"
        >
          <Search className="h-4 w-4" />
          {batchLoading ? "Buscando..." : "Buscar"}
        </button>
      </div>

      {/* Loading */}
      {batchLoading && <LoadingSpinner message="Verificando lote..." />}

      {/* Error */}
      {batchError && (
        <div className="p-4 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-red-600 dark:text-red-400">{batchError}</p>
        </div>
      )}

      {/* Batch Details */}
      {batch && !batchLoading && (
        <div className="border rounded-lg p-6 space-y-6">
          {/* Status Header */}
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold">Lote: {batch.id}</h3>
              <p className="text-sm text-muted-foreground">
                Produtor: {batch.producer_id || "N/A"}
              </p>
            </div>
            <div>
              {batch.is_compliant ? (
                <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 font-medium text-sm">
                  <CheckCircle className="h-4 w-4" />
                  Conforme
                </span>
              ) : (
                <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 font-medium text-sm">
                  <XCircle className="h-4 w-4" />
                  Pendente
                </span>
              )}
            </div>
          </div>

          {/* Telemetry Data */}
          {batch.telemetry && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center gap-3 p-3 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
                <Cloud className="h-5 w-5 text-blue-500" />
                <div>
                  <p className="text-xs text-muted-foreground">Emissões GHG</p>
                  <p className="font-semibold">{batch.telemetry.ghg_emissions.toFixed(2)} kgCO₂e/kgH₂</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-cyan-50 dark:bg-cyan-950/20 rounded-lg">
                <Droplets className="h-5 w-5 text-cyan-500" />
                <div>
                  <p className="text-xs text-muted-foreground">Consumo Água</p>
                  <p className="font-semibold">{batch.telemetry.water_consumption_liters.toFixed(1)} L/kgH₂</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-yellow-50 dark:bg-yellow-950/20 rounded-lg">
                <Zap className="h-5 w-5 text-yellow-500" />
                <div>
                  <p className="text-xs text-muted-foreground">Fonte de Energia</p>
                  <p className="font-semibold capitalize">{batch.telemetry.energy_source}</p>
                </div>
              </div>
            </div>
          )}

          {/* Compliance Report */}
          {compliance && (
            <div className="border-t pt-4">
              <h4 className="font-medium mb-3 flex items-center gap-2">
                <FileText className="h-4 w-4" />
                Relatório de Conformidade
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-xs text-muted-foreground">Status</p>
                  <p className="font-semibold">{compliance.is_compliant ? "Aprovado" : "Reprovado"}</p>
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-xs text-muted-foreground">Emissões</p>
                  <p className="font-semibold">{compliance.ghg_emissions.toFixed(2)}</p>
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-xs text-muted-foreground">Água</p>
                  <p className="font-semibold">{compliance.water_consumption.toFixed(1)} L/kgH₂</p>
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-xs text-muted-foreground">Energia</p>
                  <p className="font-semibold capitalize">{compliance.energy_source}</p>
                </div>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-2">
            <button
              onClick={handleVerify}
              className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition"
            >
              {batch.is_compliant ? "Emitir Certificado" : "Solicitar Revisão"}
            </button>
            <button className="border px-4 py-2 rounded-md text-sm hover:bg-muted transition">
              Exportar
            </button>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!batch && !batchLoading && !batchError && (
        <div className="text-center py-12 text-muted-foreground">
          <Search className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>Digite o ID de um lote para iniciar a verificação</p>
        </div>
      )}
    </div>
  );
}
