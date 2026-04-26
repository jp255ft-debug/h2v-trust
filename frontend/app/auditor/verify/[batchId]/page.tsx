"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CheckCircle, XCircle, Cloud, Droplets, Zap, FileText } from "lucide-react";
import { useBatchDetail, useBatchCompliance } from "@/hooks/useBatch";
import LoadingSpinner from "@/components/shared/LoadingSpinner";
import ErrorBoundary from "@/components/shared/ErrorBoundary";

function BatchVerificationContent() {
  const params = useParams();
  const batchId = (params?.batchId as string) || "";
  
  const { batch, isLoading: batchLoading, error: batchError } = useBatchDetail(batchId);
  const { compliance, isLoading: complianceLoading } = useBatchCompliance(batchId);

  if (batchLoading) {
    return <LoadingSpinner message="Carregando dados do lote..." />;
  }

  if (batchError) {
    return (
      <div className="p-8 text-center">
        <XCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-xl font-bold mb-2">Erro ao carregar lote</h2>
        <p className="text-muted-foreground mb-4">{batchError}</p>
        <Link href="/auditor" className="text-blue-600 hover:underline">
          Voltar para o painel do auditor
        </Link>
      </div>
    );
  }

  if (!batch) {
    return (
      <div className="p-8 text-center">
        <h2 className="text-xl font-bold mb-2">Lote não encontrado</h2>
        <p className="text-muted-foreground mb-4">O lote solicitado não foi encontrado.</p>
        <Link href="/auditor" className="text-blue-600 hover:underline">
          Voltar para o painel do auditor
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link
          href="/auditor"
          className="p-2 rounded-md border hover:bg-muted transition"
        >
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold">Verificação de Lote</h1>
          <p className="text-muted-foreground">ID: {batch.id}</p>
        </div>
        <div className="ml-auto">
          {batch.is_compliant ? (
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 font-medium">
              <CheckCircle className="h-5 w-5" />
              Conforme
            </span>
          ) : (
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 font-medium">
              <XCircle className="h-5 w-5" />
              Pendente
            </span>
          )}
        </div>
      </div>

      {/* Batch Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="border rounded-lg p-6 space-y-4">
          <h2 className="text-lg font-semibold">Informações do Lote</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-muted-foreground">ID do Lote</span>
              <span className="font-medium">{batch.id}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Produtor</span>
              <span className="font-medium">{batch.producer_id || "N/A"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Tamanho</span>
              <span className="font-medium">{batch.size_kg.toLocaleString()} kg</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Localização</span>
              <span className="font-medium">{batch.production_location || "N/A"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Data de Criação</span>
              <span className="font-medium">
                {batch.created_at ? new Date(batch.created_at).toLocaleString() : "N/A"}
              </span>
            </div>
          </div>
        </div>

        <div className="border rounded-lg p-6 space-y-4">
          <h2 className="text-lg font-semibold">Dados de Telemetria</h2>
          {batch.telemetry ? (
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <Cloud className="h-5 w-5 text-blue-500" />
                <div>
                  <p className="text-sm text-muted-foreground">Emissões GHG</p>
                  <p className="font-semibold">{batch.telemetry.ghg_emissions.toFixed(2)} kgCO₂e/kgH₂</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Droplets className="h-5 w-5 text-cyan-500" />
                <div>
                  <p className="text-sm text-muted-foreground">Consumo de Água</p>
                  <p className="font-semibold">{batch.telemetry.water_consumption_liters.toFixed(1)} L/kgH₂</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Zap className="h-5 w-5 text-yellow-500" />
                <div>
                  <p className="text-sm text-muted-foreground">Fonte de Energia</p>
                  <p className="font-semibold capitalize">{batch.telemetry.energy_source}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <FileText className="h-5 w-5 text-purple-500" />
                <div>
                  <p className="text-sm text-muted-foreground">Sensor</p>
                  <p className="font-semibold">{batch.telemetry.sensor_id}</p>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-muted-foreground">Nenhum dado de telemetria disponível</p>
          )}
        </div>
      </div>

      {/* Compliance Report */}
      {compliance && (
        <div className="border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Relatório de Conformidade</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-green-50 dark:bg-green-950/20 rounded-lg border border-green-200 dark:border-green-800">
              <p className="text-sm text-green-600 dark:text-green-400">Status</p>
              <p className="text-lg font-bold text-green-700 dark:text-green-300">
                {compliance.is_compliant ? "Conforme" : "Não Conforme"}
              </p>
            </div>
            <div className="p-4 bg-blue-50 dark:bg-blue-950/20 rounded-lg border border-blue-200 dark:border-blue-800">
              <p className="text-sm text-blue-600 dark:text-blue-400">Emissões GHG</p>
              <p className="text-lg font-bold text-blue-700 dark:text-blue-300">
                {compliance.ghg_emissions.toFixed(2)} kgCO₂e/kgH₂
              </p>
            </div>
            <div className="p-4 bg-cyan-50 dark:bg-cyan-950/20 rounded-lg border border-cyan-200 dark:border-cyan-800">
              <p className="text-sm text-cyan-600 dark:text-cyan-400">Consumo Água</p>
              <p className="text-lg font-bold text-cyan-700 dark:text-cyan-300">
                {compliance.water_consumption.toFixed(1)} L/kgH₂
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-4">
        <button className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition">
          Emitir Certificado
        </button>
        <button className="border px-6 py-2 rounded-md hover:bg-muted transition">
          Exportar Relatório
        </button>
      </div>
    </div>
  );
}

export default function BatchVerificationPage() {
  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b bg-card">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <Link href="/" className="text-xl font-bold text-foreground hover:text-primary transition">
            H2V-Trust
          </Link>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <ErrorBoundary>
          <BatchVerificationContent />
        </ErrorBoundary>
      </div>
    </div>
  );
}
