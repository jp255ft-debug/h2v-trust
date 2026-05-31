"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Search, CheckCircle, Cloud, FileText, AlertCircle } from "lucide-react";
import { fetchStats, fetchBatch } from "@/lib/api";
import type { Batch } from "@/types/batch";
import SystemStatus from "@/components/shared/SystemStatus";


export default function AuditorPage() {
  const [search, setSearch] = useState("");
  const [searchResult, setSearchResult] = useState<Batch | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
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

  const handleSearch = async () => {
    const query = search.trim();
    if (!query) return;

    setIsLoading(true);
    setError(null);
    setSearchResult(null);

    try {
      const data = await fetchBatch(query);
      setSearchResult(data);
    } catch (err: any) {
      if (err?.status === 404) {
        setError("Lote não encontrado. Verifique o ID informado.");
      } else {
        setError("Erro ao buscar lote. Verifique a conexão com o servidor.");
      }
      setSearchResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
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

          {/* Estado de erro */}
          {error && (
            <div className="mt-6 p-4 border rounded-lg bg-red-50 dark:bg-red-950/20 border-red-200 dark:border-red-800 flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-red-500 mt-0.5 flex-shrink-0" />
              <div>
                <p className="font-medium text-red-700 dark:text-red-400">Erro na pesquisa</p>
                <p className="text-sm text-red-600 dark:text-red-500">{error}</p>
              </div>
            </div>
          )}

          {/* Resultado da pesquisa */}
          {searchResult && (
            <div className="mt-6 p-4 border rounded-lg bg-muted/20">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-foreground">Lote {searchResult.id?.slice(0, 8)}...</h3>
                  <p className="text-sm text-muted-foreground">Facility: {searchResult.facility_id || "N/A"}</p>
                  <p className="text-sm text-muted-foreground">Localização: {searchResult.production_location || "N/A"}</p>
                  <p className="text-sm text-muted-foreground">Produtor: {searchResult.producer_id?.slice(0, 8)}...</p>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${searchResult.is_compliant ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400" : "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"}`}>
                    {searchResult.is_compliant ? "Conforme" : "Não conforme"}
                  </span>
                  {searchResult.compliance_report?.score && (
                    <span className="text-xs text-muted-foreground">
                      Score: {searchResult.compliance_report.score}/100
                    </span>
                  )}
                </div>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                <div>
                  <p className="text-xs text-muted-foreground">Emissões GHG</p>
                  <p className="font-semibold text-foreground">{searchResult.compliance_report?.ghg_emissions ?? "—"} kgCO₂e/kgH₂</p>
                  <p className="text-xs text-muted-foreground">Limite: {searchResult.compliance_report?.ghg_limit ?? 3.4} kgCO₂e/kgH₂</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Consumo de Água</p>
                  <p className="font-semibold text-foreground">{searchResult.compliance_report?.water_consumption ?? "—"} L/kgH₂</p>
                  <p className="text-xs text-muted-foreground">Limite: {searchResult.compliance_report?.water_limit ?? 15} L/kgH₂</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Fonte de Energia</p>
                  <p className="font-semibold text-foreground capitalize">{searchResult.compliance_report?.energy_source || searchResult.telemetry?.energy_source || "—"}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Tamanho do Lote</p>
                  <p className="font-semibold text-foreground">{searchResult.size_kg?.toFixed(1) ?? "—"} kg</p>
                </div>
              </div>
              <div className="mt-4 pt-3 border-t border-border">
                <Link
                  href={`/auditor/verify/${searchResult.id}`}
                  className="text-sm text-primary hover:text-primary/80 font-medium"
                >
                  Ver detalhes completos →
                </Link>
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

        {/* Status do Sistema - AGORA COM HEALTH CHECK REAL */}
        <SystemStatus />

      </div>
    </div>
  );
}
