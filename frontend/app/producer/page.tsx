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
import Navbar from "@/components/layout/Navbar";
import { fetchBatches, fetchStats } from "@/lib/api";

// Dados mock para demonstração
const mockLotesProdutor = [
  {
    id: "batch_045",
    tamanhoKg: 1800,
    emissoesGhg: 2.3,
    consumoAgua: 11.8,
    conforme: true,
    data: "2024-06-15",
    status: "Verificado",
    pontuacao: 94,
  },
  {
    id: "batch_044",
    tamanhoKg: 2200,
    emissoesGhg: 3.1,
    consumoAgua: 13.5,
    conforme: true,
    data: "2024-06-14",
    status: "Verificado",
    pontuacao: 82,
  },
  {
    id: "batch_043",
    tamanhoKg: 1500,
    emissoesGhg: 3.8,
    consumoAgua: 15.2,
    conforme: false,
    data: "2024-06-13",
    status: "Atenção Necessária",
    pontuacao: 58,
  },
  {
    id: "batch_042",
    tamanhoKg: 3000,
    emissoesGhg: 2.1,
    consumoAgua: 10.8,
    conforme: true,
    data: "2024-06-12",
    status: "Verificado",
    pontuacao: 97,
  },
  {
    id: "batch_041",
    tamanhoKg: 2500,
    emissoesGhg: 2.9,
    consumoAgua: 12.3,
    conforme: true,
    data: "2024-06-11",
    status: "Pendente",
    pontuacao: 88,
  },
];

const desempenhoMensal = [
  { mes: "Jan", ghg: 3.2, agua: 14.5, conforme: 85 },
  { mes: "Fev", ghg: 3.0, agua: 13.8, conforme: 88 },
  { mes: "Mar", ghg: 2.8, agua: 13.2, conforme: 90 },
  { mes: "Abr", ghg: 2.6, agua: 12.7, conforme: 92 },
  { mes: "Mai", ghg: 2.4, agua: 12.1, conforme: 94 },
  { mes: "Jun", ghg: 2.3, agua: 11.8, conforme: 96 },
];

const estatisticasProdutor = {
  producaoTotal: 125000, // kg
  percentualConformidade: 85,
  mediaEmissoesGhg: 2.5,
  mediaConsumoAgua: 12.2,
  totalLotes: 42,
  pendentesVerificacao: 3,
  certificadosEmitidos: 28,
  tendenciaConformidade: "+5.2%",
};

export default function PainelProdutor() {
  const [enviando, setEnviando] = useState(false);
  const [exibirFormNovoLote, setExibirFormNovoLote] = useState(false);
  const [novoLote, setNovoLote] = useState({
    tamanhoKg: "",
    emissoesGhg: "",
    consumoAgua: "",
  });
  const [estatisticasProdutor, setEstatisticasProdutor] = useState({
    producaoTotal: 0,
    percentualConformidade: 0,
    mediaEmissoesGhg: 0,
    mediaConsumoAgua: 0,
    totalLotes: 0,
    pendentesVerificacao: 0,
    certificadosEmitidos: 0,
    tendenciaConformidade: "+0%",
  });
  const [lotesProdutor, setLotesProdutor] = useState(mockLotesProdutor);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        
        // Load stats
        const stats = await fetchStats();
        
        // Load batches for this producer (assuming producer_id = "prod_001" for demo)
        const { batches } = await fetchBatches({ producer_id: "prod_001", limit: 10 });
        
        // Transform batches to match the table format
        const transformedBatches = batches.map(batch => ({
          id: batch.id,
          tamanhoKg: batch.size_kg,
          emissoesGhg: batch.telemetry?.ghg_emissions || 0,
          consumoAgua: batch.telemetry?.water_consumption_liters || 0,
          conforme: batch.is_compliant,
          data: batch.created_at ? new Date(batch.created_at).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
          status: batch.is_compliant ? "Verificado" : "Atenção Necessária",
          pontuacao: batch.is_compliant ? Math.floor(Math.random() * 20) + 80 : Math.floor(Math.random() * 40) + 40,
        }));
        
        setLotesProdutor(transformedBatches);
        
        // Calculate producer statistics from batches
        const totalProduction = batches.reduce((sum, batch) => sum + batch.size_kg, 0);
        const compliantBatches = batches.filter(b => b.is_compliant).length;
        const complianceRate = batches.length > 0 ? (compliantBatches / batches.length) * 100 : 0;
        
        // Calculate averages from telemetry data
        const batchesWithTelemetry = batches.filter(b => b.telemetry);
        const avgEmissions = batchesWithTelemetry.length > 0 ? 
          batchesWithTelemetry.reduce((sum, batch) => sum + (batch.telemetry?.ghg_emissions || 0), 0) / batchesWithTelemetry.length : 0;
        const avgWater = batchesWithTelemetry.length > 0 ? 
          batchesWithTelemetry.reduce((sum, batch) => sum + (batch.telemetry?.water_consumption_liters || 0), 0) / batchesWithTelemetry.length : 0;
        
        setEstatisticasProdutor({
          producaoTotal: totalProduction,
          percentualConformidade: parseFloat(complianceRate.toFixed(1)),
          mediaEmissoesGhg: parseFloat(avgEmissions.toFixed(1)),
          mediaConsumoAgua: parseFloat(avgWater.toFixed(1)),
          totalLotes: batches.length,
          pendentesVerificacao: batches.filter(b => !b.is_compliant).length,
          certificadosEmitidos: Math.floor(compliantBatches * 0.8), // Estimate
          tendenciaConformidade: "+5.2%",
        });
        
      } catch (error) {
        console.error("Failed to load producer data:", error);
        // Keep default mock data if API fails
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const handleUploadDados = () => {
    setEnviando(true);
    setTimeout(() => {
      alert("Dados do lote enviados com sucesso!");
      setEnviando(false);
    }, 1500);
  };

  const handleSubmitNovoLote = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Novo lote submetido: ${JSON.stringify(novoLote)}`);
    setExibirFormNovoLote(false);
    setNovoLote({ tamanhoKg: "", emissoesGhg: "", consumoAgua: "" });
  };

  // Função para baixar o PDF Oficial CBAM
  const handleGenerateReport = async () => {
    try {
      const year = new Date().getFullYear();
      const response = await fetch(`http://localhost:8000/api/v1/reports/cbam/${year}/download?format=pdf`, {
        method: 'GET',
        headers: {
          "X-API-Key": "test-secret-key-for-local-development-12345"
        }
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
      const response = await fetch(`http://localhost:8000/api/v1/reports/cbam/${year}/download?format=csv`, {
        method: 'GET',
        headers: {
          "X-API-Key": "test-secret-key-for-local-development-12345"
        }
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

  const handleBaixarCertificado = (idLote: string, status: string) => {
    if (status === "Atenção Necessária") {
      alert(`O lote ${idLote} possui não-conformidades e não pode ser certificado no padrão CBAM.`);
      return;
    }
    alert(`Redirecionando para a prova criptográfica (SBT) do lote ${idLote} na Polygon Explorer...`);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
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
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100">Registrar Novo Lote</h2>
              <button
                onClick={() => setExibirFormNovoLote(false)}
                className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
              >
                ✕
              </button>
            </div>
            <form onSubmit={handleSubmitNovoLote} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Tamanho do Lote (kg)</label>
                <input
                  type="number"
                  required
                  className="w-full border rounded-md px-3 py-2"
                  value={novoLote.tamanhoKg}
                  onChange={(e) => setNovoLote({ ...novoLote, tamanhoKg: e.target.value })}
                  placeholder="Ex: 1500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Emissões GHG (kgCO₂e/kgH₂)</label>
                <input
                  type="number"
                  step="0.1"
                  required
                  className="w-full border rounded-md px-3 py-2"
                  value={novoLote.emissoesGhg}
                  onChange={(e) => setNovoLote({ ...novoLote, emissoesGhg: e.target.value })}
                  placeholder="Ex: 2.8"
                />
                <p className="text-xs text-gray-500 mt-1">Limite CBAM: 3.4 kgCO₂e/kgH₂</p>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Consumo de Água (L/kgH₂)</label>
                <input
                  type="number"
                  step="0.1"
                  required
                  className="w-full border rounded-md px-3 py-2"
                  value={novoLote.consumoAgua}
                  onChange={(e) => setNovoLote({ ...novoLote, consumoAgua: e.target.value })}
                  placeholder="Ex: 12.5"
                />
                <p className="text-xs text-gray-500 mt-1">Limite recomendado: 15 L/kgH₂</p>
              </div>
              <div className="flex justify-end gap-2 pt-4">
                <button
                  type="button"
                  onClick={() => setExibirFormNovoLote(false)}
                  className="border rounded-md px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="bg-blue-600 text-white rounded-md px-4 py-2 text-sm hover:bg-blue-700"
                >
                  Registrar Lote
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Métricas principais */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="border rounded-lg p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="text-sm font-medium">Produção Total</div>
            <Factory className="h-4 w-4 text-gray-400" />
          </div>
          <div className="pt-2">
            <div className="text-2xl font-bold">{estatisticasProdutor.producaoTotal.toLocaleString('pt-BR')} kg</div>
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
            <div className="text-2xl font-bold">{estatisticasProdutor.percentualConformidade}%</div>
            <div className="flex items-center text-sm text-gray-500 mt-1">
              <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
              <span>{estatisticasProdutor.tendenciaConformidade} de melhoria</span>
            </div>
          </div>
        </div>

        <div className="border rounded-lg p-6">
          <div className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="text-sm font-medium">Média Emissões GHG</div>
            <Cloud className="h-4 w-4 text-gray-400" />
          </div>
          <div className="pt-2">
            <div className="text-2xl font-bold">{estatisticasProdutor.mediaEmissoesGhg} kgCO₂e/kgH₂</div>
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
            <div className="text-2xl font-bold">{estatisticasProdutor.certificadosEmitidos}</div>
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
              <span className="font-semibold">32 lotes</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <span>Verificação Pendente</span>
              </div>
              <span className="font-semibold">{estatisticasProdutor.pendentesVerificacao} lotes</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <span>Necessitam Atenção</span>
              </div>
              <span className="font-semibold">3 lotes</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                <span>Certificados Emitidos</span>
              </div>
              <span className="font-semibold">{estatisticasProdutor.certificadosEmitidos} SBTs</span>
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
            Ver Todos ({estatisticasProdutor.totalLotes})
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
                <th className="text-left py-3 px-4 font-medium">Pontuação</th>
                <th className="text-left py-3 px-4 font-medium">Ações</th>
              </tr>
            </thead>
            <tbody>
              {lotesProdutor.map((lote: any) => (
                <tr key={lote.id} className="border-b hover:bg-gray-100 dark:hover:bg-gray-800">
                  <td className="py-3 px-4">
                    <div className="font-medium">{lote.id}</div>
                    <div className="text-sm text-gray-500">{lote.data}</div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="font-semibold">{lote.tamanhoKg.toLocaleString('pt-BR')} kg</div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="font-semibold">{lote.emissoesGhg} kgCO₂e/kgH₂</div>
                    <div className={`text-xs ${lote.emissoesGhg <= 3.4 ? "text-green-600" : "text-red-600"}`}>
                      {lote.emissoesGhg <= 3.4 ? "✓ Dentro do limite" : "✗ Acima do limite"}
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="font-semibold">{lote.consumoAgua} L/kgH₂</div>
                    <div className={`text-xs ${lote.consumoAgua <= 15 ? "text-blue-600" : "text-orange-600"}`}>
                      {lote.consumoAgua <= 15 ? "✓ Dentro do limite" : "✗ Acima do limite"}
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-2 py-1 rounded-full text-xs ${
                        lote.status === "Verificado"
                          ? "bg-green-100 text-green-800"
                          : lote.status === "Pendente"
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {lote.status}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="font-semibold">{lote.pontuacao}/100</div>
                    <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden mt-1">
                      <div
                        className={`h-full ${
                          lote.pontuacao >= 80
                            ? "bg-green-500"
                            : lote.pontuacao >= 60
                            ? "bg-yellow-500"
                            : "bg-red-500"
                        }`}
                        style={{ width: `${lote.pontuacao}%` }}
                      />
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleBaixarCertificado(lote.id, lote.status)}
                        className="text-blue-600 hover:text-blue-800 text-sm"
                      >
                        <Download className="h-4 w-4 inline mr-1" />
                        Cert
                      </button>
                      {lote.status === "Atenção Necessária" && (
                        <button className="text-red-600 hover:text-red-800 text-sm">
                          <AlertTriangle className="h-4 w-4 inline mr-1" />
                          Corrigir
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
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
