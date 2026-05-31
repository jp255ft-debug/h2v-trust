"use client";

import { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import {
  TrendingUp,
  TrendingDown,
  Droplets,
  Cloud,
  Factory,
  CheckCircle,
  XCircle,
  Upload,
  FileText,
  Download,
  PlusCircle,
  AlertTriangle,
} from "lucide-react";
import { fetchBatches, fetchStats } from "@/lib/api";
import type { Batch } from "@/types/batch";
import { useAuth } from "@/hooks/useAuth";

export default function PainelProdutor() {
  const { getToken } = useAuth();
  const [enviando, setEnviando] = useState(false);
  const [exibirFormNovoLote, setExibirFormNovoLote] = useState(false);
  const [novoLote, setNovoLote] = useState({
    tamanhoKg: "",
    emissoesGhg: "",
    consumoAgua: "",
  });
  const [estatisticas, setEstatisticas] = useState({
    producaoTotal: 0,
    percentualConformidade: 0,
    mediaEmissoesGhg: 0,
    mediaConsumoAgua: 0,
    totalLotes: 0,
    lotesConformes: 0,
    lotesNaoConformes: 0,
    pendentesVerificacao: 0,
    certificadosEmitidos: 0,
    tendenciaConformidade: "+0%",
  });
  const [lotes, setLotes] = useState<Batch[]>([]);
  const [desempenhoMensal, setDesempenhoMensal] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [erroApi, setErroApi] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        setErroApi(null);

        // Carrega todos os lotes (sem filtro de producer_id para pegar tudo)
        const { batches } = await fetchBatches({ limit: 1000 });

        if (!batches || batches.length === 0) {
          setEstatisticas({
            producaoTotal: 0,
            percentualConformidade: 0,
            mediaEmissoesGhg: 0,
            mediaConsumoAgua: 0,
            totalLotes: 0,
            lotesConformes: 0,
            lotesNaoConformes: 0,
            pendentesVerificacao: 0,
            certificadosEmitidos: 0,
            tendenciaConformidade: "+0%",
          });
          setLotes([]);
          setDesempenhoMensal([]);
          setIsLoading(false);
          return;
        }

        setLotes(batches);

        // --- Cálculo das estatísticas dos cards superiores ---
        const totalProduction = batches.reduce((sum: number, b: Batch) => sum + (b.size_kg || 0), 0);
        const compliantBatches = batches.filter((b: Batch) => b.is_compliant).length;
        const nonCompliantBatches = batches.length - compliantBatches;
        const complianceRate = (compliantBatches / batches.length) * 100;

        // Médias de telemetria
        const batchesWithTelemetry = batches.filter((b: Batch) => b.telemetry);
        const avgEmissions = batchesWithTelemetry.length > 0
          ? batchesWithTelemetry.reduce((sum: number, b: Batch) => sum + (b.telemetry?.ghg_emissions || 0), 0) / batchesWithTelemetry.length
          : 0;
        const avgWater = batchesWithTelemetry.length > 0
          ? batchesWithTelemetry.reduce((sum: number, b: Batch) => sum + (b.telemetry?.water_consumption_liters || 0), 0) / batchesWithTelemetry.length
          : 0;

        // Tendência: comparar últimos 30 dias com os 30 anteriores
        const now = new Date();
        const trintaDiasAtras = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        const sessentaDiasAtras = new Date(now.getTime() - 60 * 24 * 60 * 60 * 1000);

        const batchesRecentes = batches.filter((b: Batch) => {
          if (!b.created_at) return false;
          const d = new Date(b.created_at);
          return d >= trintaDiasAtras && d <= now;
        });
        const batchesAnteriores = batches.filter((b: Batch) => {
          if (!b.created_at) return false;
          const d = new Date(b.created_at);
          return d >= sessentaDiasAtras && d < trintaDiasAtras;
        });

        const taxaRecente = batchesRecentes.length > 0
          ? (batchesRecentes.filter((b: Batch) => b.is_compliant).length / batchesRecentes.length) * 100
          : 0;
        const taxaAnterior = batchesAnteriores.length > 0
          ? (batchesAnteriores.filter((b: Batch) => b.is_compliant).length / batchesAnteriores.length) * 100
          : 0;

        let tendencia = "+0%";
        if (taxaAnterior > 0) {
          const diff = ((taxaRecente - taxaAnterior) / taxaAnterior) * 100;
          tendencia = `${diff >= 0 ? "+" : ""}${diff.toFixed(1)}%`;
        }

        setEstatisticas({
          producaoTotal: totalProduction,
          percentualConformidade: complianceRate != null ? parseFloat(complianceRate.toFixed(1)) : 0,
          mediaEmissoesGhg: avgEmissions != null ? parseFloat(avgEmissions.toFixed(2)) : 0,
          mediaConsumoAgua: avgWater != null ? parseFloat(avgWater.toFixed(1)) : 0,
          totalLotes: batches.length,
          lotesConformes: compliantBatches,
          lotesNaoConformes: nonCompliantBatches,
          pendentesVerificacao: nonCompliantBatches,
          certificadosEmitidos: compliantBatches,
          tendenciaConformidade: tendencia,
        });

        // --- Dados para o gráfico de tendência mensal ---
        const meses: Record<string, { ghg: number[]; agua: number[]; conforme: number[]; count: number }> = {};
        const nomesMeses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

        batches.forEach((b: Batch) => {
          if (!b.created_at) return;
          const d = new Date(b.created_at);
          const mesKey = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
          const mesLabel = nomesMeses[d.getMonth()];

          if (!meses[mesKey]) {
            meses[mesKey] = { ghg: [], agua: [], conforme: [], count: 0 };
          }
          meses[mesKey].count++;
          if (b.telemetry) {
            meses[mesKey].ghg.push(b.telemetry.ghg_emissions || 0);
            meses[mesKey].agua.push(b.telemetry.water_consumption_liters || 0);
          }
          meses[mesKey].conforme.push(b.is_compliant ? 100 : 0);
        });

        const dadosMensais = Object.entries(meses)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([key, vals]) => {
            const mesNum = parseInt(key.split("-")[1]) - 1;
            return {
              mes: nomesMeses[mesNum] || key,
              ghg: vals.ghg.length > 0 ? parseFloat((vals.ghg.reduce((a: number, b: number) => a + b, 0) / vals.ghg.length).toFixed(2)) : 0,
              agua: vals.agua.length > 0 ? parseFloat((vals.agua.reduce((a: number, b: number) => a + b, 0) / vals.agua.length).toFixed(1)) : 0,
              conforme: parseFloat((vals.conforme.reduce((a: number, b: number) => a + b, 0) / vals.conforme.length).toFixed(0)),
            };
          });

        setDesempenhoMensal(dadosMensais.length > 0 ? dadosMensais : []);

      } catch (error: any) {
        console.error("Falha ao carregar dados do produtor:", error);
        setErroApi(error.message || "Erro ao conectar com a API");
        // Zera tudo em caso de erro
        setEstatisticas({
          producaoTotal: 0,
          percentualConformidade: 0,
          mediaEmissoesGhg: 0,
          mediaConsumoAgua: 0,
          totalLotes: 0,
          lotesConformes: 0,
          lotesNaoConformes: 0,
          pendentesVerificacao: 0,
          certificadosEmitidos: 0,
          tendenciaConformidade: "+0%",
        });
        setLotes([]);
        setDesempenhoMensal([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const handleUploadDados = async () => {
    setEnviando(true);
    try {
      const apiKey = process.env.NEXT_PUBLIC_API_KEY || "";
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || "";
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(apiKey ? { "X-API-Key": apiKey } : {}),
      };
      // Envia dados de telemetria simulados para o lote mais recente
      const payload = {
        sensor_id: "producer_dashboard_upload",
        timestamp: new Date().toISOString(),
        energy_source: "wind",
        power_generated_mwh: 1.5,
        ghg_emissions_kgCO2_per_kgH2: 2.8,
        water_consumption_liters: 12.5,
        water_source: "desalination",
      };
      const res = await fetch(`${apiBaseUrl}/api/v1/telemetry`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const errBody = await res.text().catch(() => "Erro desconhecido");
        throw new Error(`Erro ${res.status}: ${errBody}`);
      }
      const result = await res.json();
      alert(`✅ Dados enviados com sucesso!\nLote: ${result.batch_id?.slice(0, 12)}...\nConforme: ${result.is_compliant ? "Sim" : "Não"}`);
      window.location.reload();
    } catch (err) {
      console.error("Erro ao enviar dados:", err);
      alert(`❌ Erro ao enviar dados: ${err instanceof Error ? err.message : "Erro desconhecido"}`);
    } finally {
      setEnviando(false);
    }
  };


  const handleSubmitNovoLote = async (e: React.FormEvent) => {
    e.preventDefault();
    setEnviando(true);
    try {
      const apiKey = process.env.NEXT_PUBLIC_API_KEY || "";
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || "";
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(apiKey ? { "X-API-Key": apiKey } : {}),
      };
      const payload = {
        sensor_id: "producer_dashboard",
        timestamp: new Date().toISOString(),
        energy_source: "wind",
        power_generated_mwh: parseFloat(novoLote.tamanhoKg) / 100,
        ghg_emissions_kgCO2_per_kgH2: parseFloat(novoLote.emissoesGhg),
        water_consumption_liters: parseFloat(novoLote.consumoAgua),
        water_source: "desalination",
      };
      const res = await fetch(`${apiBaseUrl}/api/v1/telemetry`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const errBody = await res.text().catch(() => "Erro desconhecido");
        throw new Error(`Erro ${res.status}: ${errBody}`);
      }
      const result = await res.json();
      alert(`✅ Lote criado com sucesso!\nID: ${result.batch_id?.slice(0, 12)}...\nConforme: ${result.is_compliant ? "Sim" : "Não"}`);
      setExibirFormNovoLote(false);
      setNovoLote({ tamanhoKg: "", emissoesGhg: "", consumoAgua: "" });
      // Recarregar dados
      window.location.reload();
    } catch (err) {
      console.error("Erro ao criar lote:", err);
      alert(`❌ Erro ao criar lote: ${err instanceof Error ? err.message : "Erro desconhecido"}`);
    } finally {
      setEnviando(false);
    }
  };

  // Helper para headers de autenticação (JWT Bearer com fallback X-API-Key)
  function getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {};
    const token = getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    } else {
      const apiKey = process.env.NEXT_PUBLIC_API_KEY || "";
      if (apiKey) {
        headers["X-API-Key"] = apiKey;
      }
    }
    return headers;
  }

  // Função para baixar o PDF Oficial CBAM
  const handleGenerateReport = async () => {
    try {
      const year = new Date().getFullYear();
      const response = await fetch(`/api/v1/reports/cbam/${year}/download?format=pdf`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) throw new Error("Falha ao gerar o relatório");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Certificacao_CBAM_H2V_${year}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Erro ao baixar relatório:", error);
      alert("Erro ao gerar relatório oficial. Verifique se o backend está rodando.");
    }
  };

  // Função para baixar a planilha de dados (CSV)
  const handleExportData = async () => {
    try {
      const year = new Date().getFullYear();
      const response = await fetch(`/api/v1/reports/cbam/${year}/download?format=csv`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) throw new Error("Falha ao exportar dados");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Dados_Telemetria_H2V_${year}.csv`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Erro ao exportar CSV:", error);
      alert("Erro ao exportar dados. Verifique se o backend está rodando.");
    }
  };

  const handleBaixarCertificado = async (idLote: string, isCompliant: boolean) => {
    if (!isCompliant) {
      alert(`O lote ${idLote} possui não-conformidades e não pode ser certificado no padrão CBAM.`);
      return;
    }
    try {
      const { certifyBatch } = await import("@/lib/api");
      const result = await certifyBatch(idLote);
      alert(`✅ Certificado SBT emitido com sucesso!\nToken ID: ${result.token_id}\nTX: ${result.tx_hash?.slice(0, 20)}...`);
      window.location.reload();
    } catch (err) {
      console.error("Erro ao emitir certificado:", err);
      alert(`❌ Erro ao emitir certificado: ${err instanceof Error ? err.message : "Erro desconhecido"}`);
    }
  };


  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-muted-foreground">Carregando dados de produção...</p>
        </div>
      </div>
    );
  }

  // Erro state
  if (erroApi) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center max-w-md">
          <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-2">Erro de Conexão</h2>
          <p className="text-muted-foreground mb-4">
            Não foi possível carregar os dados do servidor. Verifique se o backend está rodando.
          </p>
          <p className="text-sm text-red-500 mb-4">{erroApi}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-green-600 text-white rounded-md px-6 py-2 hover:bg-green-700"
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-6 space-y-6">
      {/* Cabeçalho */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Painel do Produtor</h1>
          <p className="text-muted-foreground">
            Gerencie sua produção de hidrogênio verde e relatórios de conformidade
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setExibirFormNovoLote(true)}
            className="bg-green-600 text-white rounded-md px-4 py-2 text-sm flex items-center gap-2 hover:bg-green-700"
          >
            <PlusCircle className="h-4 w-4" />
            Novo Lote
          </button>
          <button
            onClick={handleUploadDados}
            disabled={enviando}
            className="border rounded-md px-4 py-2 text-sm flex items-center gap-2 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50"
          >
            <Upload className="h-4 w-4" />
            {enviando ? "Enviando..." : "Enviar Dados"}
          </button>
        </div>
      </div>

      {/* Modal Novo Lote */}
      {exibirFormNovoLote && (
        <div className="fixed inset-0 flex items-center justify-center z-50" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
          <div style={{backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '24px', maxWidth: '448px', width: '100%', margin: '0 16px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px'}}>
              <h2 style={{fontSize: '20px', fontWeight: '700', color: '#111827', margin: 0}}>Registrar Novo Lote</h2>
              <button
                onClick={() => setExibirFormNovoLote(false)}
                style={{color: '#6b7280', background: 'none', border: 'none', cursor: 'pointer', fontSize: '18px'}}
              >
                ✕
              </button>
            </div>
            <form onSubmit={handleSubmitNovoLote}>
              <div style={{marginBottom: '16px'}}>
                <label style={{display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '4px'}}>Tamanho do Lote (kg)</label>
                <input
                  type="number"
                  required
                  style={{width: '100%', border: '1px solid #d1d5db', borderRadius: '6px', padding: '8px 12px', backgroundColor: '#ffffff', color: '#000000', fontSize: '16px'}}
                  value={novoLote.tamanhoKg}
                  onChange={(e) => setNovoLote({ ...novoLote, tamanhoKg: e.target.value })}
                  placeholder="Ex: 1500"
                />
              </div>
              <div style={{marginBottom: '16px'}}>
                <label style={{display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '4px'}}>Emissões GHG (kgCO₂e/kgH₂)</label>
                <input
                  type="number"
                  step="0.1"
                  required
                  style={{width: '100%', border: '1px solid #d1d5db', borderRadius: '6px', padding: '8px 12px', backgroundColor: '#ffffff', color: '#000000', fontSize: '16px'}}
                  value={novoLote.emissoesGhg}
                  onChange={(e) => setNovoLote({ ...novoLote, emissoesGhg: e.target.value })}
                  placeholder="Ex: 2.8"
                />
                <p style={{fontSize: '12px', color: '#6b7280', marginTop: '4px', margin: '4px 0 0 0'}}>Limite CBAM: 3.4 kgCO₂e/kgH₂</p>
              </div>
              <div style={{marginBottom: '16px'}}>
                <label style={{display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '4px'}}>Consumo de Água (L/kgH₂)</label>
                <input
                  type="number"
                  step="0.1"
                  required
                  style={{width: '100%', border: '1px solid #d1d5db', borderRadius: '6px', padding: '8px 12px', backgroundColor: '#ffffff', color: '#000000', fontSize: '16px'}}
                  value={novoLote.consumoAgua}
                  onChange={(e) => setNovoLote({ ...novoLote, consumoAgua: e.target.value })}
                  placeholder="Ex: 12.5"
                />
                <p style={{fontSize: '12px', color: '#6b7280', marginTop: '4px', margin: '4px 0 0 0'}}>Limite recomendado: 15 L/kgH₂</p>
              </div>
              <div style={{display: 'flex', justifyContent: 'flex-end', gap: '8px', paddingTop: '16px'}}>
                <button
                  type="button"
                  onClick={() => setExibirFormNovoLote(false)}
                  style={{border: '1px solid #d1d5db', borderRadius: '6px', padding: '8px 16px', color: '#374151', backgroundColor: '#ffffff', cursor: 'pointer', fontSize: '14px'}}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  style={{backgroundColor: '#2563eb', color: '#ffffff', borderRadius: '6px', padding: '8px 16px', border: 'none', cursor: 'pointer', fontSize: '14px'}}
                >
                  Registrar Lote
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Métricas principais - AGORA USANDO DADOS REAIS DA API */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="border rounded-lg p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="text-sm font-medium">Produção Total</div>
            <Factory className="h-4 w-4 text-gray-400" />
          </div>
          <div className="pt-2">
            <div className="text-2xl font-bold">{estatisticas.producaoTotal.toLocaleString('pt-BR')} kg</div>
            <div className="flex items-center text-sm text-gray-500 mt-1">
              <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
              <span>Hidrogênio verde produzido</span>
            </div>
          </div>
        </div>

        <div className="border rounded-lg p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="text-sm font-medium">Taxa de Conformidade</div>
            <CheckCircle className="h-4 w-4 text-gray-400" />
          </div>
          <div className="pt-2">
            <div className="text-2xl font-bold">{estatisticas.percentualConformidade}%</div>
            <div className="flex items-center text-sm text-gray-500 mt-1">
              <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
              <span>{estatisticas.tendenciaConformidade} de melhoria</span>
            </div>
          </div>
        </div>

        <div className="border rounded-lg p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="text-sm font-medium">Média Emissões GHG</div>
            <Cloud className="h-4 w-4 text-gray-400" />
          </div>
          <div className="pt-2">
            <div className="text-2xl font-bold">{estatisticas.mediaEmissoesGhg} kgCO₂e/kgH₂</div>
            <div className="flex items-center text-sm text-gray-500 mt-1">
              <TrendingDown className="h-4 w-4 text-green-500 mr-1" />
              <span>Abaixo do limite CBAM</span>
            </div>
          </div>
        </div>

        <div className="border rounded-lg p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="text-sm font-medium">Certificados</div>
            <FileText className="h-4 w-4 text-gray-400" />
          </div>
          <div className="pt-2">
            <div className="text-2xl font-bold">{estatisticas.certificadosEmitidos}</div>
            <div className="flex items-center text-sm text-gray-500 mt-1">
              <span>Tokens Soulbound emitidos</span>
            </div>
          </div>
        </div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="border rounded-lg p-6">
          <div className="mb-4">
            <h2 className="text-xl font-bold">Tendência Mensal de Desempenho</h2>
            <p className="text-gray-500">Evolução das emissões GHG e consumo de água</p>
          </div>
          <div className="h-80">
            {desempenhoMensal.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={desempenhoMensal}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="mes" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Legend />
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="ghg"
                    name="Emissões GHG (kgCO₂e/kgH₂)"
                    stroke="#3b82f6"
                    strokeWidth={2}
                  />
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="agua"
                    name="Consumo Água (L/kgH₂)"
                    stroke="#06b6d4"
                    strokeWidth={2}
                  />
                  <Line
                    yAxisId="right"
                    type="monotone"
                    dataKey="conforme"
                    name="Taxa de Conformidade (%)"
                    stroke="#10b981"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-full text-gray-400">
                <p>Sem dados mensais disponíveis</p>
              </div>
            )}
          </div>
        </div>

        <div className="border rounded-lg p-6">
          <div className="mb-4">
            <h2 className="text-xl font-bold">Visão Geral dos Lotes</h2>
            <p className="text-gray-500">Distribuição dos seus lotes de produção</p>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span>Verificados & Conformes</span>
              </div>
              <span className="font-semibold">{estatisticas.lotesConformes} lotes</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <span>Verificação Pendente</span>
              </div>
              <span className="font-semibold">{estatisticas.pendentesVerificacao} lotes</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <span>Necessitam Atenção</span>
              </div>
              <span className="font-semibold">{estatisticas.lotesNaoConformes} lotes</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                <span>Certificados Emitidos</span>
              </div>
              <span className="font-semibold">{estatisticas.certificadosEmitidos} SBTs</span>
            </div>
          </div>

          <div className="mt-6 pt-6 border-t">
            <h3 className="font-medium mb-3">Ações Rápidas</h3>
            <div className="grid grid-cols-2 gap-2">
              <button onClick={handleGenerateReport} className="border rounded-md p-3 text-sm hover:bg-gray-100 dark:hover:bg-gray-800 flex flex-col items-center justify-center">
                <FileText className="h-5 w-5 mb-1 text-blue-500" />
                <span>Gerar Relatório</span>
              </button>
              <button onClick={handleExportData} className="border rounded-md p-3 text-sm hover:bg-gray-100 dark:hover:bg-gray-800 flex flex-col items-center justify-center">
                <Download className="h-5 w-5 mb-1 text-green-500" />
                <span>Exportar Dados</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Tabela de lotes recentes */}
      <div className="border rounded-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-xl font-bold">Lotes de Produção Recentes</h2>
            <p className="text-gray-500">Seus últimos lotes de hidrogênio verde</p>
          </div>
          <button className="border rounded-md px-3 py-1 text-sm">
            Ver Todos ({estatisticas.totalLotes})
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-4 font-medium">ID do Lote</th>
                <th className="text-left py-3 px-4 font-medium">Tamanho (kg)</th>
                <th className="text-left py-3 px-4 font-medium">Emissões GHG</th>
                <th className="text-left py-3 px-4 font-medium">Água</th>
                <th className="text-left py-3 px-4 font-medium">Status</th>
                <th className="text-left py-3 px-4 font-medium">Conforme</th>
                <th className="text-left py-3 px-4 font-medium">Ações</th>
              </tr>
            </thead>
            <tbody>
              {lotes.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-gray-400">
                    Nenhum lote encontrado
                  </td>
                </tr>
              ) : (
                lotes.slice(0, 10).map((lote: Batch) => {
                  const dataFormatada = lote.created_at
                    ? new Date(lote.created_at).toLocaleDateString('pt-BR')
                    : "-";
                  const statusLabel = lote.is_compliant ? "Verificado" : "Atenção Necessária";
                  const statusColor = lote.is_compliant
                    ? "bg-green-100 text-green-800"
                    : "bg-red-100 text-red-800";
                  const ghgValue = lote.telemetry?.ghg_emissions || 0;
                  const aguaValue = lote.telemetry?.water_consumption_liters || 0;

                  return (
                    <tr key={lote.id} className="border-b hover:bg-gray-100 dark:hover:bg-gray-800">
                      <td className="py-3 px-4">
                        <div className="font-medium">{lote.id}</div>
                        <div className="text-sm text-gray-500">{dataFormatada}</div>
                      </td>
                      <td className="py-3 px-4">
                        <div className="font-semibold">{(lote.size_kg || 0).toLocaleString('pt-BR')} kg</div>
                      </td>
                      <td className="py-3 px-4">
                        <div className="font-semibold">{ghgValue} kgCO₂e/kgH₂</div>
                        <div className={`text-xs ${ghgValue <= 3.4 ? "text-green-600" : "text-red-600"}`}>
                          {ghgValue <= 3.4 ? "✓ Dentro do limite" : "✗ Acima do limite"}
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <div className="font-semibold">{aguaValue} L/kgH₂</div>
                        <div className={`text-xs ${aguaValue <= 15 ? "text-blue-600" : "text-orange-600"}`}>
                          {aguaValue <= 15 ? "✓ Dentro do limite" : "✗ Acima do limite"}
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs ${statusColor}`}>
                          {statusLabel}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        {lote.is_compliant ? (
                          <CheckCircle className="h-5 w-5 text-green-500" />
                        ) : (
                          <XCircle className="h-5 w-5 text-red-500" />
                        )}
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleBaixarCertificado(lote.id, lote.is_compliant)}
                            className="text-blue-600 hover:text-blue-800 text-sm"
                          >
                            <Download className="h-4 w-4 inline mr-1" />
                            Cert
                          </button>
                          {!lote.is_compliant && (
                            <button className="text-red-600 hover:text-red-800 text-sm">
                              <AlertTriangle className="h-4 w-4 inline mr-1" />
                              Corrigir
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Dicas de conformidade */}
      <div className="border rounded-lg p-6">
        <div className="mb-4">
          <h2 className="text-xl font-bold">Dicas e Recomendações de Conformidade</h2>
          <p className="text-gray-500">Melhore seu desempenho ambiental</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Cloud className="h-5 w-5 text-blue-500" />
              <h3 className="font-semibold">Reduza as Emissões GHG</h3>
            </div>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Otimize a eficiência dos eletrolisadores</li>
              <li>• Use fontes de energia renovável</li>
              <li>• Implemente sistemas de captura de carbono</li>
              <li>• Manutenção regular dos equipamentos</li>
            </ul>
          </div>
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Droplets className="h-5 w-5 text-blue-500" />
              <h3 className="font-semibold">Melhore a Eficiência Hídrica</h3>
            </div>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Implemente sistemas de reciclagem de água</li>
              <li>• Use água de alimentação de alta qualidade</li>
              <li>• Monitore o consumo em tempo real</li>
              <li>• Calibração regular do sistema</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}
