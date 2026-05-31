"use client";

import { useState } from "react";
import Link from "next/link";
import { PlusCircle, Search, Download, AlertTriangle, CheckCircle, Clock, Award } from "lucide-react";
import { useBatches } from "@/hooks/useBatch";
import { certifyBatch } from "@/lib/api";
import LoadingSpinner from "@/components/shared/LoadingSpinner";

export default function ProducerBatchesPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [showNewBatch, setShowNewBatch] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [certifyingBatchId, setCertifyingBatchId] = useState<string | null>(null);
  const [certifyError, setCertifyError] = useState<string | null>(null);
  const [newBatchForm, setNewBatchForm] = useState({
    tamanhoKg: "",
    emissoesGhg: "",
    consumoAgua: "",
  });
  const { batches, total, isLoading, error, refetch } = useBatches({ limit: 50 });

  const handleCertify = async (batchId: string) => {
    setCertifyingBatchId(batchId);
    setCertifyError(null);
    try {
      await certifyBatch(batchId);
      await refetch();
    } catch (err) {
      setCertifyError(err instanceof Error ? err.message : "Erro ao certificar lote");
    } finally {
      setCertifyingBatchId(null);
    }
  };


  const handleSubmitNewBatch = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
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
        power_generated_mwh: parseFloat(newBatchForm.tamanhoKg) / 100,
        ghg_emissions_kgCO2_per_kgH2: parseFloat(newBatchForm.emissoesGhg),
        water_consumption_liters: parseFloat(newBatchForm.consumoAgua),
        water_source: "desalination",
        producer_wallet: "0x1234567890abcdef1234567890abcdef12345678",
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
      setShowNewBatch(false);
      setNewBatchForm({ tamanhoKg: "", emissoesGhg: "", consumoAgua: "" });
      refetch();
    } catch (err) {
      console.error("Erro ao criar lote:", err);
      alert(`❌ Erro ao criar lote: ${err instanceof Error ? err.message : "Erro desconhecido"}`);
    } finally {
      setSubmitting(false);
    }
  };

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
        <LoadingSpinner message="Carregando lotes..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
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

        {/* Certify Error */}
        {certifyError && (
          <div className="p-4 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-600 dark:text-red-400 text-sm flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              {certifyError}
            </p>
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

        {/* Modal Novo Lote */}
        {showNewBatch && (
          <div className="fixed inset-0 flex items-center justify-center z-50" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
            <div style={{backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '24px', maxWidth: '448px', width: '100%', margin: '0 16px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)'}}>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px'}}>
                <h2 style={{fontSize: '20px', fontWeight: '700', color: '#111827', margin: 0}}>Registrar Novo Lote</h2>
                <button
                  onClick={() => setShowNewBatch(false)}
                  style={{color: '#6b7280', background: 'none', border: 'none', cursor: 'pointer', fontSize: '18px'}}
                >
                  ✕
                </button>
              </div>
              <form onSubmit={handleSubmitNewBatch}>
                <div style={{marginBottom: '16px'}}>
                  <label style={{display: 'block', fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '4px'}}>Tamanho do Lote (kg)</label>
                  <input
                    type="number"
                    required
                    style={{width: '100%', border: '1px solid #d1d5db', borderRadius: '6px', padding: '8px 12px', backgroundColor: '#ffffff', color: '#000000', fontSize: '16px'}}
                    value={newBatchForm.tamanhoKg}
                    onChange={(e) => setNewBatchForm({ ...newBatchForm, tamanhoKg: e.target.value })}
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
                    value={newBatchForm.emissoesGhg}
                    onChange={(e) => setNewBatchForm({ ...newBatchForm, emissoesGhg: e.target.value })}
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
                    value={newBatchForm.consumoAgua}
                    onChange={(e) => setNewBatchForm({ ...newBatchForm, consumoAgua: e.target.value })}
                    placeholder="Ex: 12.5"
                  />
                  <p style={{fontSize: '12px', color: '#6b7280', marginTop: '4px', margin: '4px 0 0 0'}}>Limite recomendado: 15 L/kgH₂</p>
                </div>
                <div style={{display: 'flex', justifyContent: 'flex-end', gap: '8px', paddingTop: '16px'}}>
                  <button
                    type="button"
                    onClick={() => setShowNewBatch(false)}
                    style={{border: '1px solid #d1d5db', borderRadius: '6px', padding: '8px 16px', color: '#374151', backgroundColor: '#ffffff', cursor: 'pointer', fontSize: '14px'}}
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    style={{backgroundColor: '#2563eb', color: '#ffffff', borderRadius: '6px', padding: '8px 16px', border: 'none', cursor: 'pointer', fontSize: '14px'}}
                  >
                    {submitting ? "Registrando..." : "Registrar Lote"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

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
                          {batch.is_compliant && (
                            <button
                              onClick={() => handleCertify(batch.id)}
                              disabled={certifyingBatchId === batch.id}
                              className="text-purple-600 hover:text-purple-800 text-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
                            >
                              <Award className="h-4 w-4" />
                              {certifyingBatchId === batch.id ? "Certificando..." : "Certificar"}
                            </button>
                          )}
                          <Link
                            href={`/producer/certificates?batch_id=${batch.id}`}
                            className="text-green-600 hover:text-green-800 text-sm"
                          >
                            <Download className="h-4 w-4 inline mr-1" />
                            Certificado
                          </Link>
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
