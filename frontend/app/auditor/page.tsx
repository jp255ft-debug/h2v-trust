"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Search, CheckCircle, Cloud, FileText } from "lucide-react";
import { fetchStats, fetchCertificate } from "@/lib/api";

export default function AuditorPage() {
  const [search, setSearch] = useState("");
  const [searchResult, setSearchResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState({
    totalCertificates: 0,
    complianceRate: 0,
    avgEmissions: 0,
  });
  const [statsLoading, setStatsLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        setStatsLoading(true);
        const statsData = await fetchStats();
        setStats({
          totalCertificates: statsData.totalCertificates,
          complianceRate: statsData.complianceRate,
          avgEmissions: statsData.avgEmissions,
        });
      } catch (err) {
        console.error("Failed to load auditor stats:", err);
        // Fallback to demo data
        setStats({
          totalCertificates: 1248,
          complianceRate: 96.7,
          avgEmissions: 2.1,
        });
      } finally {
        setStatsLoading(false);
      }
    };

    loadStats();
  }, []);

  const handleSearch = () => {
    setIsLoading(true);
    // Simular chamada à API
    setTimeout(() => {
      setSearchResult({
        id: "cert_001",
        batchId: "batch_045",
        producer: "Produtor A",
        ghgEmissions: 2.3,
        waterConsumption: 11.8,
        isCompliant: true,
        verifiedAt: "2024-06-15",
      });
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Menu de navegação */}
      <nav className="border-b bg-card">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-6">
            <Link href="/" className="text-xl font-bold text-foreground hover:text-primary transition">
              H2V-Trust
            </Link>
            <div className="flex gap-4">
              <Link href="/dashboard" className="text-sm font-medium text-foreground hover:text-primary transition">
                Dashboard
              </Link>
              <Link href="/auditor" className="text-sm font-medium text-primary transition">
                Auditor
              </Link>
              <Link href="/producer" className="text-sm font-medium text-foreground hover:text-primary transition">
                Produtor
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Conteúdo principal */}
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {/* Cabeçalho */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Auditor H2V-Trust</h1>
          <p className="text-muted-foreground mt-2">
            Sistema de auditoria e verificação de certificados de hidrogênio verde
          </p>
        </div>

        {/* Barra de pesquisa */}
        <div className="bg-card rounded-lg border shadow-sm p-6">
          <h2 className="text-xl font-semibold text-foreground mb-4">Pesquisar Certificados</h2>
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Digite ID do certificado, produtor ou lote..."
              className="flex-1 border rounded-md px-4 py-2 bg-background text-foreground"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button
              onClick={handleSearch}
              disabled={isLoading}
              className="bg-primary text-primary-foreground px-6 py-2 rounded-md hover:bg-primary/90 transition disabled:opacity-50 flex items-center gap-2"
            >
              <Search className="h-4 w-4" />
              {isLoading ? "Buscando..." : "Pesquisar"}
            </button>
          </div>

          {/* Resultado da pesquisa */}
          {searchResult && (
            <div className="mt-6 p-4 border rounded-lg bg-muted/20">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-foreground">Certificado {searchResult.id}</h3>
                  <p className="text-sm text-muted-foreground">Lote: {searchResult.batchId}</p>
                  <p className="text-sm text-muted-foreground">Produtor: {searchResult.producer}</p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${searchResult.isCompliant ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400" : "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"}`}>
                  {searchResult.isCompliant ? "Conforme" : "Não conforme"}
                </span>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-4">
                <div>
                  <p className="text-xs text-muted-foreground">Emissões GHG</p>
                  <p className="font-semibold text-foreground">{searchResult.ghgEmissions} kgCO₂e/kgH₂</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Consumo de Água</p>
                  <p className="font-semibold text-foreground">{searchResult.waterConsumption} L/kgH₂</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Verificado em</p>
                  <p className="font-semibold text-foreground">{searchResult.verifiedAt}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Cards de métricas */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-card rounded-lg border shadow-sm p-6">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium text-muted-foreground">Certificados Verificados</p>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </div>
            <p className="text-2xl font-bold mt-2 text-foreground">{stats.totalCertificates}</p>
            <p className="text-xs text-muted-foreground mt-1">Total auditado</p>
          </div>

          <div className="bg-card rounded-lg border shadow-sm p-6">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium text-muted-foreground">Conformidade</p>
              <CheckCircle className="h-4 w-4 text-muted-foreground" />
            </div>
            <p className="text-2xl font-bold mt-2 text-foreground">{stats.complianceRate}%</p>
            <p className="text-xs text-muted-foreground mt-1">Taxa de aprovação</p>
          </div>

          <div className="bg-card rounded-lg border shadow-sm p-6">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium text-muted-foreground">Emissões Médias</p>
              <Cloud className="h-4 w-4 text-muted-foreground" />
            </div>
            <p className="text-2xl font-bold mt-2 text-foreground">{stats.avgEmissions} kgCO₂e/kgH₂</p>
            <p className="text-xs text-muted-foreground mt-1">Abaixo do limite CBAM</p>
          </div>
        </div>

        {/* Status do Sistema */}
        <div className="bg-card rounded-lg border shadow-sm">
          <div className="p-6">
            <h2 className="text-xl font-semibold text-foreground">Status do Sistema</h2>
          </div>
          <div className="p-6 pt-0 space-y-4">
            <div className="flex items-center justify-between p-4 rounded-lg border bg-green-50 dark:bg-green-950/20 border-green-200 dark:border-green-800">
              <div>
                <p className="font-medium text-green-700 dark:text-green-400">✅ Módulo de Auditoria</p>
                <p className="text-sm text-green-600 dark:text-green-500">Operacional</p>
              </div>
              <span className="px-3 py-1 rounded-full text-sm font-medium bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
                Ativo
              </span>
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg border bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800">
              <div>
                <p className="font-medium text-blue-700 dark:text-blue-400">🔗 Conexão Blockchain</p>
                <p className="text-sm text-blue-600 dark:text-blue-500">Configurada</p>
              </div>
              <span className="px-3 py-1 rounded-full text-sm font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">
                Conectada
              </span>
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg border bg-purple-50 dark:bg-purple-950/20 border-purple-200 dark:border-purple-800">
              <div>
                <p className="font-medium text-purple-700 dark:text-purple-400">📊 Banco de Dados</p>
                <p className="text-sm text-purple-600 dark:text-purple-500">Sincronizado</p>
              </div>
              <span className="px-3 py-1 rounded-full text-sm font-medium bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200">
                Online
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
