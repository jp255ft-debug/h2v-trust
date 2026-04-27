"use client";

import { useState } from "react";
import Link from "next/link";
import { PlusCircle, Search, Download, AlertTriangle, CheckCircle, Clock } from "lucide-react";
import Navbar from "@/components/layout/Navbar";
import { useBatches } from "@/hooks/useBatch";
import LoadingSpinner from "@/components/shared/LoadingSpinner";

export default function ProducerBatchesPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [showNewBatch, setShowNewBatch] = useState(false);
  const { batches, total, isLoading, error } = useBatches({ limit: 50 });

  const filteredBatches = batches.filter(
    (b: any) =>
      b.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      b.producer_id?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusBadge = (isCompliant: boolean) => {
    if (isCompliant) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
          <CheckCircle className="h-3 w-3" />
          Verificado
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400">
        <Clock className="h-3 w-3" />
        Pendente
      </span>
    );
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <LoadingSpinner message="Carregando lotes..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="container mx-auto p-6 space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Meus Lotes</h1>
            <p className="text-muted-foreground">
              Gerencie seus lotes de produção de hidrogênio verde
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowNewBatch(true)}
              className="bg-green-600 text-white rounded-md px-4 py-2 text-sm flex items-center gap-2 hover:bg-green-700"
            >
              <PlusCircle className="h-4 w-4" />
              Novo Lote
            </button>
          </div>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Pesquisar lotes por ID ou produtor..."
            className="w-full border rounded-md pl-10 pr-4 py-2 bg-background"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {/* Error */}
        {error && (
          <div className="p-4 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
          </div>
        )}

        {/* Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="border rounded-lg p-4">
            <p className="text-sm text-muted-foreground">Total de Lotes</p>
            <p className="text-2xl font-bold">{total}</p>
          </div>
          <div className="border rounded-lg p-4">
            <p className="text-sm text-muted-foreground">Conformes</p>
            <p className="text-2xl font-bold text-green-600">
              {batches.filter((b: any) => b.is_compliant).length}
            </p>
          </div>
          <div className="border rounded-lg p-4">
            <p className="text-sm text-muted-foreground">Pendentes</p>
            <p className="text-2xl font-bold text-yellow-600">
              {batches.filter((b: any) => !b.is_compliant).length}
            </p>
          </div>
        </div>

        {/* Batches Table */}
        <div className="border rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b bg-muted/50">
                  <th className="text-left py-3 px-4 font-medium text-sm">ID do Lote</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Tamanho</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Emissões GHG</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Consumo Água</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Data</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredBatches.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-8 text-center text-muted-foreground">
                      Nenhum lote encontrado
                    </td>
                  </tr>
                ) : (
                  filteredBatches.map((batch: any) => (
                    <tr key={batch.id} className="border-b hover:bg-muted/30">
                      <td className="py-3 px-4">
                        <div className="font-medium">{batch.id.substring(0, 12)}...</div>
                      </td>
                      <td className="py-3 px-4">{batch.size_kg.toLocaleString()} kg</td>
                      <td className="py-3 px-4">
                        {batch.telemetry?.ghg_emissions?.toFixed(2) || "N/A"} kgCO₂e/kgH₂
                      </td>
                      <td className="py-3 px-4">
                        {batch.telemetry?.water_consumption_liters?.toFixed(1) || "N/A"} L/kgH₂
                      </td>
                      <td className="py-3 px-4">{getStatusBadge(batch.is_compliant)}</td>
                      <td className="py-3 px-4 text-sm text-muted-foreground">
                        {batch.created_at ? new Date(batch.created_at).toLocaleDateString() : "N/A"}
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex gap-2">
                          <Link
                            href={`/auditor/verify/${batch.id}`}
                            className="text-blue-600 hover:text-blue-800 text-sm"
                          >
                            Verificar
                          </Link>
                          <button className="text-green-600 hover:text-green-800 text-sm">
                            <Download className="h-4 w-4 inline mr-1" />
                            Certificado
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
