"use client";

import { Suspense, useEffect, useState, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CheckCircle, XCircle, FileText, Flame } from "lucide-react";
import LoadingSpinner from "@/components/shared/LoadingSpinner";
import { useAuth } from "@/hooks/useAuth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "";

function getAuthHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  // Prioridade: JWT Bearer > API Key
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("h2v_admin_token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
      return headers;
    }
  }
  if (API_KEY) {
    headers["X-API-Key"] = API_KEY;
  }
  return headers;
}

interface Certificate {
  id: string;
  token_id: number;
  batch_id: string;
  is_consumed: boolean;
  created_at: string;
  blockchain_tx_hash: string;
}

function CertificatesContent() {
  const searchParams = useSearchParams();
  const batchIdFilter = searchParams.get("batch_id");
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [consumingId, setConsumingId] = useState<string | null>(null);
  const [consumeError, setConsumeError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        setError(null);
        const url = batchIdFilter
          ? `${API_BASE_URL}/api/v1/certificates?batch_id=${encodeURIComponent(batchIdFilter)}`
          : `${API_BASE_URL}/api/v1/certificates`;
        const res = await fetch(url, {
          headers: getAuthHeaders(),
        });
        if (!res.ok) throw new Error(`Erro ${res.status}`);
        const data = await res.json();
        setCertificates(data.certificates || []);
      } catch (err) {
        console.error("Erro ao carregar certificados:", err);
        setError("Falha ao carregar certificados");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [batchIdFilter]);

  const handleConsume = useCallback(async (certId: string) => {
    if (!window.confirm("Tem certeza que deseja consumir este certificado? Esta ação não pode ser desfeita.")) {
      return;
    }
    setConsumingId(certId);
    setConsumeError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/certificates/${certId}/consume`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify({ consumer_wallet: "0x0000000000000000000000000000000000000000", purpose: "cbam_surrender" }),
      });
      if (!res.ok) {
        const errBody = await res.text().catch(() => "Erro desconhecido");
        throw new Error(`Erro ${res.status}: ${errBody}`);
      }
      const result = await res.json();
      // Atualizar a lista localmente
      setCertificates((prev) =>
        prev.map((c) =>
          c.id === certId ? { ...c, is_consumed: true } : c
        )
      );
      alert(`✅ Certificado consumido com sucesso!\nTX: ${result.tx_hash?.slice(0, 20)}...`);
    } catch (err) {
      console.error("Erro ao consumir certificado:", err);
      setConsumeError(err instanceof Error ? err.message : "Falha ao consumir certificado");
    } finally {
      setConsumingId(null);
    }
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <LoadingSpinner message="Carregando certificados..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <Link
            href="/producer/batches"
            className="p-2 rounded-md border hover:bg-muted transition"
          >
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Meus Certificados</h1>
            <p className="text-muted-foreground">
              Certificados de hidrogênio verde emitidos na blockchain
            </p>
          </div>
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
            <p className="text-sm text-muted-foreground">Total</p>
            <p className="text-2xl font-bold">{certificates.length}</p>
          </div>
          <div className="border rounded-lg p-4">
            <p className="text-sm text-muted-foreground">Ativos</p>
            <p className="text-2xl font-bold text-green-600">
              {certificates.filter((c) => !c.is_consumed).length}
            </p>
          </div>
          <div className="border rounded-lg p-4">
            <p className="text-sm text-muted-foreground">Consumidos</p>
            <p className="text-2xl font-bold text-yellow-600">
              {certificates.filter((c) => c.is_consumed).length}
            </p>
          </div>
        </div>

        {/* Consume Error */}
        {consumeError && (
          <div className="p-4 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-600 dark:text-red-400 text-sm">{consumeError}</p>
          </div>
        )}

        {/* Table */}
        <div className="border rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b bg-muted/50">
                  <th className="text-left py-3 px-4 font-medium text-sm">Token ID</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Lote</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Data</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">TX Hash</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Ações</th>
                </tr>
              </thead>
              <tbody>
                {certificates.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-muted-foreground">
                      <FileText className="h-8 w-8 mx-auto mb-2 opacity-50" />
                      <p>Nenhum certificado emitido ainda.</p>
                    </td>
                  </tr>
                ) : (
                  certificates.map((cert) => (
                    <tr key={cert.id} className="border-b hover:bg-muted/30">
                      <td className="py-3 px-4 font-medium">#{cert.token_id}</td>
                      <td className="py-3 px-4 font-mono text-xs">
                        {cert.batch_id?.slice(0, 12)}...
                      </td>
                      <td className="py-3 px-4">
                        {cert.is_consumed ? (
                          <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400">
                            <XCircle className="h-3 w-3" />
                            Consumido
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                            <CheckCircle className="h-3 w-3" />
                            Ativo
                          </span>
                        )}
                      </td>
                      <td className="py-3 px-4 text-sm text-muted-foreground">
                        {cert.created_at
                          ? new Date(cert.created_at).toLocaleDateString("pt-BR")
                          : "N/A"}
                      </td>
                      <td className="py-3 px-4 font-mono text-xs text-muted-foreground">
                        {cert.blockchain_tx_hash?.slice(0, 16)}...
                      </td>
                      <td className="py-3 px-4">
                        {!cert.is_consumed && (
                          <button
                            onClick={() => handleConsume(cert.id)}
                            disabled={consumingId === cert.id}
                            className="inline-flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium bg-orange-100 text-orange-800 hover:bg-orange-200 dark:bg-orange-900/30 dark:text-orange-400 dark:hover:bg-orange-900/50 transition disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <Flame className="h-3 w-3" />
                            {consumingId === cert.id ? "Consumindo..." : "Consumir"}
                          </button>
                        )}
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

export default function CertificatesPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-background flex items-center justify-center">
        <LoadingSpinner message="Carregando certificados..." />
      </div>
    }>
      <CertificatesContent />
    </Suspense>
  );
}
