"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CheckCircle, XCircle, Cloud, Droplets, Zap, FileText, Shield, ExternalLink, Download, Award } from "lucide-react";
import { useBatchDetail, useBatchCompliance } from "@/hooks/useBatch";
import LoadingSpinner from "@/components/shared/LoadingSpinner";
import ErrorBoundary from "@/components/shared/ErrorBoundary";

const GHG_LIMIT = 3.4; // kgCO₂e/kgH₂ - Limite CBAM
const WATER_LIMIT = 15; // L/kgH₂ - Limite recomendado

function EmissionsGauge({ value, max, label, unit, good }: { value: number; max: number; label: string; unit: string; good: boolean }) {
  const pct = Math.min((value / max) * 100, 100);
  const color = good ? "bg-green-500" : value <= max * 1.2 ? "bg-yellow-500" : "bg-red-500";
  const textColor = good ? "text-green-600" : value <= max * 1.2 ? "text-yellow-600" : "text-red-600";

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium">{label}</span>
        <span className={`text-lg font-bold ${textColor}`}>
          {value.toFixed(2)} <span className="text-sm font-normal text-muted-foreground">{unit}</span>
        </span>
      </div>
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${Math.min(pct, 100)}%` }}
        />
      </div>
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>0</span>
        <span>Limite: {max} {unit}</span>
      </div>
    </div>
  );
}

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

  const ghgValue = batch.telemetry?.ghg_emissions ?? 0;
  const waterValue = batch.telemetry?.water_consumption_liters ?? 0;
  const ghgOk = ghgValue <= GHG_LIMIT;
  const waterOk = waterValue <= WATER_LIMIT;
  const complianceScore = batch.compliance_report?.score ?? (batch.is_compliant ? 95 : 45);

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
          <p className="text-muted-foreground font-mono text-sm">ID: {batch.id}</p>
        </div>
        <div className="ml-auto">
          {batch.is_compliant ? (
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 font-medium">
              <CheckCircle className="h-5 w-5" />
              Conforme CBAM
            </span>
          ) : (
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 font-medium">
              <XCircle className="h-5 w-5" />
              Não Conforme
            </span>
          )}
        </div>
      </div>

      {/* Score Card */}
      <div className="border rounded-lg p-6 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-muted-foreground">Score de Conformidade CBAM</p>
            <p className={`text-4xl font-bold ${complianceScore >= 80 ? 'text-green-600' : complianceScore >= 60 ? 'text-yellow-600' : 'text-red-600'}`}>
              {complianceScore.toFixed(0)}<span className="text-lg">%</span>
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-muted-foreground">Padrão</p>
            <p className="font-semibold flex items-center gap-1">
              <Award className="h-4 w-4" />
              CBAM (EU) 2023/956
            </p>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Batch Info */}
        <div className="border rounded-lg p-6 space-y-4">
          <h2 className="text-lg font-semibold">Informações do Lote</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Produtor</span>
              <span className="font-medium">{batch.producer_id || "N/A"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Instalação</span>
              <span className="font-medium">{batch.facility_id || "N/A"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Localização</span>
              <span className="font-medium">{batch.production_location || "N/A"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Tamanho</span>
              <span className="font-medium">{batch.size_kg.toLocaleString()} kg H₂</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Data de Criação</span>
              <span className="font-medium">
                {batch.created_at ? new Date(batch.created_at).toLocaleString() : "N/A"}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Status Blockchain</span>
              <span className={`font-medium capitalize ${
                batch.blockchain_status === "confirmed" ? "text-green-600" : "text-yellow-600"
              }`}>
                {batch.blockchain_status || "Não iniciado"}
              </span>
            </div>
          </div>
        </div>

        {/* Telemetry */}
        <div className="border rounded-lg p-6 space-y-4">
          <h2 className="text-lg font-semibold">Dados de Telemetria</h2>
          {batch.telemetry ? (
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <Cloud className={`h-5 w-5 ${ghgOk ? 'text-green-500' : 'text-red-500'}`} />
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground">Emissões GHG</p>
                  <p className={`font-semibold ${ghgOk ? 'text-green-600' : 'text-red-600'}`}>
                    {ghgValue.toFixed(2)} kgCO₂e/kgH₂
                    {ghgOk ? ' ✅ Abaixo do limite' : ' ⚠️ Acima do limite CBAM'}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Droplets className={`h-5 w-5 ${waterOk ? 'text-cyan-500' : 'text-red-500'}`} />
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground">Consumo de Água</p>
                  <p className={`font-semibold ${waterOk ? 'text-cyan-600' : 'text-red-600'}`}>
                    {waterValue.toFixed(1)} L/kgH₂
                    {waterOk ? ' ✅ Abaixo do limite' : ' ⚠️ Acima do limite recomendado'}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Zap className="h-5 w-5 text-yellow-500" />
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground">Fonte de Energia</p>
                  <p className="font-semibold capitalize">{batch.telemetry.energy_source}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <FileText className="h-5 w-5 text-purple-500" />
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground">Sensor / Potência</p>
                  <p className="font-semibold">{batch.telemetry.sensor_id} · {batch.telemetry.power_generated_mwh.toFixed(2)} MWh</p>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-muted-foreground">Nenhum dado de telemetria disponível</p>
          )}
        </div>
      </div>

      {/* Emissions Gauges */}
      <div className="border rounded-lg p-6 space-y-6">
        <h2 className="text-lg font-semibold">Indicadores de Conformidade CBAM</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <EmissionsGauge
            value={ghgValue}
            max={GHG_LIMIT}
            label="Emissões GHG"
            unit="kgCO₂e/kgH₂"
            good={ghgOk}
          />
          <EmissionsGauge
            value={waterValue}
            max={WATER_LIMIT}
            label="Consumo de Água"
            unit="L/kgH₂"
            good={waterOk}
          />
        </div>
      </div>

      {/* Compliance Report */}
      {compliance && (
        <div className="border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Relatório de Conformidade</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className={`p-4 rounded-lg border ${
              batch.is_compliant
                ? "bg-green-50 dark:bg-green-950/20 border-green-200 dark:border-green-800"
                : "bg-red-50 dark:bg-red-950/20 border-red-200 dark:border-red-800"
            }`}>
              <p className="text-sm text-muted-foreground">Status Geral</p>
              <p className={`text-lg font-bold ${
                batch.is_compliant ? "text-green-700 dark:text-green-300" : "text-red-700 dark:text-red-300"
              }`}>
                {batch.is_compliant ? "✅ Conforme" : "❌ Não Conforme"}
              </p>
            </div>
            <div className="p-4 bg-blue-50 dark:bg-blue-950/20 rounded-lg border border-blue-200 dark:border-blue-800">
              <p className="text-sm text-blue-600 dark:text-blue-400">Emissões GHG</p>
              <p className="text-lg font-bold text-blue-700 dark:text-blue-300">
                {compliance.ghg_emissions.toFixed(2)} kgCO₂e/kgH₂
              </p>
              <p className="text-xs text-blue-500 mt-1">Limite CBAM: 3.4</p>
            </div>
            <div className="p-4 bg-cyan-50 dark:bg-cyan-950/20 rounded-lg border border-cyan-200 dark:border-cyan-800">
              <p className="text-sm text-cyan-600 dark:text-cyan-400">Consumo Água</p>
              <p className="text-lg font-bold text-cyan-700 dark:text-cyan-300">
                {compliance.water_consumption.toFixed(1)} L/kgH₂
              </p>
              <p className="text-xs text-cyan-500 mt-1">Limite: 15 L/kgH₂</p>
            </div>
          </div>
          <p className="text-xs text-muted-foreground mt-4">
            Relatório gerado em: {compliance.generated_at ? new Date(compliance.generated_at).toLocaleString() : "N/A"}
          </p>
        </div>
      )}

      {/* Blockchain Proof */}
      <div className="border rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Shield className="h-5 w-5 text-purple-500" />
          Prova Blockchain
        </h2>
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-muted-foreground">Batch Hash</span>
            <span className="font-mono text-sm">{batch.batch_hash ? `${batch.batch_hash.substring(0, 20)}...` : "N/A"}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">Status</span>
            <span className={`font-medium capitalize ${
              batch.blockchain_status === "confirmed" ? "text-green-600" : "text-yellow-600"
            }`}>
              {batch.blockchain_status === "confirmed" ? "✅ Confirmado" : "⏳ Pendente"}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">Carteira do Produtor</span>
            <span className="font-mono text-sm">{batch.producer_wallet ? `${batch.producer_wallet.substring(0, 14)}...` : "N/A"}</span>
          </div>
          {batch.batch_hash && (
            <div className="pt-2">
              <a
                href={`https://sepolia.etherscan.io/tx/${batch.batch_hash}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 text-sm flex items-center gap-1"
              >
                <ExternalLink className="h-3 w-3" />
                Verificar no Etherscan
              </a>
            </div>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-4">
        <button
          onClick={async () => {
            if (!batch.is_compliant) return;
            try {
              const { certifyBatch } = await import("@/lib/api");
              const result = await certifyBatch(batch.id);
              alert(`✅ Certificado SBT emitido com sucesso!\nToken ID: ${result.token_id}\nTX: ${result.tx_hash?.slice(0, 20)}...`);
            } catch (err) {
              alert(`❌ Erro ao emitir certificado: ${err instanceof Error ? err.message : "Erro desconhecido"}`);
            }
          }}
          className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={!batch.is_compliant}
          title={!batch.is_compliant ? "Lote não conforme não pode receber certificado" : "Emitir certificado SBT"}
        >
          <Award className="h-4 w-4" />
          Emitir Certificado SBT
        </button>
        <button
          onClick={async () => {
            try {
              const year = new Date().getFullYear();
              const response = await fetch(`/api/v1/reports/cbam/${year}/download?format=pdf`, {
                method: 'GET'
              });
              if (!response.ok) throw new Error("Falha ao gerar o relatório");
              const blob = await response.blob();
              const url = window.URL.createObjectURL(blob);
              const link = document.createElement('a');
              link.href = url;
              link.download = `Relatorio_Verificacao_${batch.id.slice(0, 8)}_${year}.pdf`;
              document.body.appendChild(link);
              link.click();
              link.remove();
              window.URL.revokeObjectURL(url);
            } catch (error) {
              console.error("Erro ao exportar relatório:", error);
              alert("Erro ao exportar relatório PDF. Verifique se o backend está rodando.");
            }
          }}
          className="border px-6 py-2 rounded-md hover:bg-muted transition flex items-center gap-2"
        >
          <Download className="h-4 w-4" />
          Exportar Relatório PDF
        </button>
        <Link
          href={`/producer/certificates?batch_id=${batch.id}`}
          className="border px-6 py-2 rounded-md hover:bg-muted transition flex items-center gap-2"
        >
          Ver Certificados
        </Link>
      </div>
    </div>
  );
}

export default function BatchVerificationPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <ErrorBoundary>
          <BatchVerificationContent />
        </ErrorBoundary>
      </div>
    </div>
  );
}
