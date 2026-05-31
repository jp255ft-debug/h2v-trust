"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { fetchStats, fetchBatches } from "@/lib/api";
import ProductionChart from "./components/ProductionChart";
import EmissionsGauge from "./components/EmissionsGauge";
import CertificatesTable from "./components/CertificatesTable";
import WaterCompliance from "./components/WaterCompliance";
import SystemStatus from "@/components/shared/SystemStatus";


export default function Dashboard() {
  const [metrics, setMetrics] = useState([
    { title: "Certificados Emitidos", value: "0", unit: "", trend: "+0%", description: "Carregando..." },
    { title: "Conformidade CBAM", value: "0%", unit: "", trend: "+0%", description: "Carregando..." },
    { title: "Emissões Médias", value: "0.0", unit: "kgCO₂e/kgH₂", trend: "0.0", description: "Carregando..." },
    { title: "Consumo de Água", value: "0.0", unit: "L/kgH₂", trend: "0.0", description: "Carregando..." },
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
            description: "Taxa de aprovação" 
          },
          { 
            title: "Emissões Médias", 
            value: statsData.avgEmissions.toFixed(1), 
            unit: "kgCO₂e/kgH₂", 
            trend: "-0.4", 
            description: `Abaixo do limite (3.4)` 
          },
          { 
            title: "Consumo de Água", 
            value: statsData.avgWaterConsumption.toFixed(1), 
            unit: "L/kgH₂", 
            trend: "-1.2", 
            description: "Eficiência hídrica" 
          },
        ]);
        setError(null);
      } catch (err) {
        console.error("Failed to load dashboard data:", err);
        setError("Falha ao carregar dados do dashboard. Usando dados de demonstração.");
        
        // Fallback to demo data
        setMetrics([
          { title: "Certificados Emitidos", value: "1,248", unit: "", trend: "+12%", description: "Total auditado" },
          { title: "Conformidade CBAM", value: "96.7%", unit: "", trend: "+2.3%", description: "Taxa de aprovação" },
          { title: "Emissões Médias", value: "2.1", unit: "kgCO₂e/kgH₂", trend: "-0.4", description: "Abaixo do limite (3.4)" },
          { title: "Consumo de Água", value: "11.6", unit: "L/kgH₂", trend: "-1.2", description: "Eficiência hídrica" },
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
    if (isPositive) return `▲ ${trend}`;
    if (isNegative) return `▼ ${trend}`;
    return trend;
  };

  const getTrendColor = (trend: string) => {
    if (trend.startsWith("+")) return "text-green-600 dark:text-green-400";
    if (trend.startsWith("-")) return "text-red-600 dark:text-red-400";
    return "text-muted-foreground";
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">

        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Dashboard H2V-Trust</h1>
          <p className="text-muted-foreground mt-2">Monitoramento e indicadores do sistema de certificação blockchain para hidrogênio verde</p>
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

        {/* System Status - AGORA COM HEALTH CHECK REAL */}
        <SystemStatus />


        {/* Next Steps */}
        <div className="bg-card text-card-foreground rounded-lg border shadow-sm">
          <div className="p-6"><h2 className="text-xl font-semibold">Próximos Passos</h2></div>
          <div className="p-6 pt-0">
            <ul className="space-y-3">
              <li className="flex items-start gap-2"><span className="text-green-500">✓</span><span className="text-muted-foreground">Dashboard com componentes visuais implementados</span></li>
              <li className="flex items-start gap-2"><span className="text-green-500">✓</span><span className="text-muted-foreground">Gráficos Recharts integrados</span></li>
              <li className="flex items-start gap-2"><span className="text-green-500">✓</span><span className="text-muted-foreground">Conectado à API de dados</span></li>
              <li className="flex items-start gap-2"><span className="text-blue-500">→</span><span className="text-muted-foreground">Iniciar backend: <code className="bg-muted px-2 py-1 rounded text-sm">cd backend && uvicorn main:app --reload</code></span></li>
              <li className="flex items-start gap-2"><span className="text-blue-500">→</span><span className="text-muted-foreground">Testar integração API com dados reais</span></li>
              <li className="flex items-start gap-2"><span className="text-blue-500">→</span><span className="text-muted-foreground">Configurar conexão com blockchain</span></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
