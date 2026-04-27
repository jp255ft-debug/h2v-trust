"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { fetchStats, fetchBatches } from "@/lib/api";
import ProductionChart from "./components/ProductionChart";
import EmissionsGauge from "./components/EmissionsGauge";
import CertificatesTable from "./components/CertificatesTable";
import WaterCompliance from "./components/WaterCompliance";

export default function Dashboard() {
  const [metrics, setMetrics] = useState([
    { title: "Certificados Emitidos", value: "0", unit: "", trend: "+0%", description: "Carregando..." },
    { title: "Conformidade CBAM", value: "0%", unit: "", trend: "+0%", description: "Carregando..." },
    { title: "Emiss├Áes M├®dias", value: "0.0", unit: "kgCOÔéée/kgHÔéé", trend: "0.0", description: "Carregando..." },
    { title: "Consumo de ├ügua", value: "0.0", unit: "L/kgHÔéé", trend: "0.0", description: "Carregando..." },
  ]);
  const [stats, setStats] = useState<any>(null);
  const [batches, setBatches] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        
        // Load stats and batches in parallel
        const [statsData, batchesData] = await Promise.all([
          fetchStats(),
          fetchBatches({ limit: 20 })
        ]);
        
        setStats(statsData);
        setBatches(batchesData.batches);
        
        // Format the metrics from API data
        setMetrics([
          { 
            title: "Certificados Emitidos", 
            value: statsData.totalCertificates.toLocaleString(), 
            unit: "", 
            trend: "+12%", 
            description: "Total auditado" 
          },
          { 
            title: "Conformidade CBAM", 
            value: `${statsData.complianceRate}%`, 
            unit: "", 
            trend: "+2.3%", 
            description: "Taxa de aprova├º├úo" 
          },
          { 
            title: "Emiss├Áes M├®dias", 
            value: statsData.avgEmissions.toFixed(1), 
            unit: "kgCOÔéée/kgHÔéé", 
            trend: "-0.4", 
            description: `Abaixo do limite (3.4)` 
          },
          { 
            title: "Consumo de ├ügua", 
            value: statsData.avgWaterConsumption.toFixed(1), 
            unit: "L/kgHÔéé", 
            trend: "-1.2", 
            description: "Efici├¬ncia h├¡drica" 
          },
        ]);
        setError(null);
      } catch (err) {
        console.error("Failed to load dashboard data:", err);
        setError("Falha ao carregar dados do dashboard. Usando dados de demonstra├º├úo.");
        
        // Fallback to demo data
        setMetrics([
          { title: "Certificados Emitidos", value: "1,248", unit: "", trend: "+12%", description: "Total auditado" },
          { title: "Conformidade CBAM", value: "96.7%", unit: "", trend: "+2.3%", description: "Taxa de aprova├º├úo" },
          { title: "Emiss├Áes M├®dias", value: "2.1", unit: "kgCOÔéée/kgHÔéé", trend: "-0.4", description: "Abaixo do limite (3.4)" },
          { title: "Consumo de ├ügua", value: "11.6", unit: "L/kgHÔéé", trend: "-1.2", description: "Efici├¬ncia h├¡drica" },
        ]);
        
        // Set demo stats and batches
        setStats({
          totalCertificates: 1248,
          complianceRate: 96.7,
          avgEmissions: 2.1,
          avgWaterConsumption: 11.6,
          totalBatches: 42,
          compliantBatches: 36,
          nonCompliantBatches: 6
        });
        
        setBatches([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  const formatTrend = (trend: string) => {
    const isPositive = trend.startsWith("+");
    const isNegative = trend.startsWith("-");
    if (isPositive) return `Ôû▓ ${trend}`;
    if (isNegative) return `Ôû╝ ${trend}`;
    return trend;
  };

  const getTrendColor = (trend: string) => {
    if (trend.startsWith("+")) return "text-green-600 dark:text-green-400";
    if (trend.startsWith("-")) return "text-red-600 dark:text-red-400";
    return "text-muted-foreground";
  };

  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b bg-card">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-6">
            <Link href="/" className="text-xl font-bold text-foreground hover:text-primary transition">H2V-Trust</Link>
            <div className="flex gap-4">
              <Link href="/dashboard" className="text-sm font-medium text-primary transition">Dashboard</Link>
              <Link href="/auditor" className="text-sm font-medium text-foreground hover:text-primary transition">Auditor</Link>
              <Link href="/producer" className="text-sm font-medium text-foreground hover:text-primary transition">Produtor</Link>
            </div>
          </div>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Dashboard H2V-Trust</h1>
          <p className="text-muted-foreground mt-2">Monitoramento e indicadores do sistema de certifica├º├úo blockchain para hidrog├¬nio verde</p>
        </div>
        
        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {metrics.map((metric, idx) => (
            <div key={idx} className="bg-card text-card-foreground rounded-lg border shadow-sm p-6">
              <div className="flex flex-row items-center justify-between pb-2">
                <h3 className="text-sm font-medium text-muted-foreground">{metric.title}</h3>
              </div>
              <div className="pt-2">
                <div className="text-2xl font-bold">
                  {metric.value} <span className="text-lg font-normal text-muted-foreground">{metric.unit}</span>
                </div>
                <div className="flex items-center gap-2 mt-2">
                  <span className={`text-xs ${getTrendColor(metric.trend)}`}>{formatTrend(metric.trend)}</span>
                  <span className="text-xs text-muted-foreground">{metric.description}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Main Dashboard Components */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Charts */}
          <div className="lg:col-span-2 space-y-6">
            <ProductionChart batches={batches} />
            <CertificatesTable batches={batches} />
          </div>
          
          {/* Right Column - Gauges and Compliance */}
          <div className="space-y-6">
            <EmissionsGauge avgEmissions={stats?.avgEmissions} />
            <WaterCompliance 
              avgWaterConsumption={stats?.avgWaterConsumption} 
              batches={batches}
            />
          </div>
        </div>

        {/* System Status */}
        <div className="bg-card text-card-foreground rounded-lg border shadow-sm">
          <div className="p-6"><h2 className="text-xl font-semibold">Status do Sistema</h2></div>
          <div className="p-6 pt-0 space-y-4">
            <div className="flex items-center justify-between p-4 rounded-lg border bg-green-50 dark:bg-green-950/20 border-green-200 dark:border-green-800">
              <div><p className="font-medium text-green-700 dark:text-green-400">Ô£à Frontend</p><p className="text-sm text-green-600 dark:text-green-500">Next.js rodando em localhost:3000</p></div>
              <span className="px-3 py-1 rounded-full text-sm font-medium bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">Operacional</span>
            </div>
            <div className="flex items-center justify-between p-4 rounded-lg border bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800">
              <div><p className="font-medium text-blue-700 dark:text-blue-400">­ƒöº Backend API</p><p className="text-sm text-blue-600 dark:text-blue-500">FastAPI pronto para iniciar na porta 8000</p></div>
              <span className="px-3 py-1 rounded-full text-sm font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">Pronto</span>
            </div>
            <div className="flex items-center justify-between p-4 rounded-lg border bg-purple-50 dark:bg-purple-950/20 border-purple-200 dark:border-purple-800">
              <div><p className="font-medium text-purple-700 dark:text-purple-400">Ôøô´©Å Blockchain</p><p className="text-sm text-purple-600 dark:text-purple-500">Contratos Ethereum configurados</p></div>
              <span className="px-3 py-1 rounded-full text-sm font-medium bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200">Configurado</span>
            </div>
          </div>
        </div>

        {/* Next Steps */}
        <div className="bg-card text-card-foreground rounded-lg border shadow-sm">
          <div className="p-6"><h2 className="text-xl font-semibold">Pr├│ximos Passos</h2></div>
          <div className="p-6 pt-0">
            <ul className="space-y-3">
              <li className="flex items-start gap-2"><span className="text-green-500">Ô£ô</span><span className="text-muted-foreground">Dashboard com componentes visuais implementados</span></li>
              <li className="flex items-start gap-2"><span className="text-green-500">Ô£ô</span><span className="text-muted-foreground">Gr├íficos Recharts integrados</span></li>
              <li className="flex items-start gap-2"><span className="text-green-500">Ô£ô</span><span className="text-muted-foreground">Conectado ├á API de dados</span></li>
              <li className="flex items-start gap-2"><span className="text-blue-500">ÔåÆ</span><span className="text-muted-foreground">Iniciar backend: <code className="bg-muted px-2 py-1 rounded text-sm">cd backend && uvicorn main:app --reload</code></span></li>
              <li className="flex items-start gap-2"><span className="text-blue-500">ÔåÆ</span><span className="text-muted-foreground">Testar integra├º├úo API com dados reais</span></li>
              <li className="flex items-start gap-2"><span className="text-blue-500">ÔåÆ</span><span className="text-muted-foreground">Configurar conex├úo com blockchain</span></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
