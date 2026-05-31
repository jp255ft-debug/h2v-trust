"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CheckCircle, XCircle, UserPlus, Trash2, RefreshCw } from "lucide-react";
import LoadingSpinner from "@/components/shared/LoadingSpinner";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "";
const headers: Record<string, string> = {
  "Content-Type": "application/json",
  ...(API_KEY ? { "X-API-Key": API_KEY } : {}),
};

interface Delegation {
  id: string;
  producer_id: string;
  declarant_address: string;
  status: string;
  created_at: string;
  valid_until: string;
}

function DelegationContent() {
  const searchParams = useSearchParams();
  const producerId = searchParams.get("producer_id") || "prod_001";

  const [declarantWallet, setDeclarantWallet] = useState("");
  const [delegations, setDelegations] = useState<Delegation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const fetchDelegations = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetch(`${API_BASE_URL}/api/v1/delegation/status/${producerId}`, {
        headers,
      });
      if (!res.ok) throw new Error(`Erro ${res.status}`);
      const data = await res.json();
      setDelegations(data.delegations || []);
    } catch (err) {
      console.error("Erro ao carregar delegações:", err);
      setError("Falha ao carregar delegações");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDelegations();
  }, [producerId]);

  const handleAuthorize = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!declarantWallet.trim()) return;

    setError(null);
    setActionLoading("authorize");
    try {
      const res = await fetch(
        `${API_BASE_URL}/api/v1/delegation/authorize?producer_id=${encodeURIComponent(producerId)}&declarant_wallet=${encodeURIComponent(declarantWallet.trim())}`,
        {
          method: "POST",
          headers,
        }
      );
      if (!res.ok) {
        const errBody = await res.text().catch(() => "Erro desconhecido");
        throw new Error(`Erro ${res.status}: ${errBody}`);
      }
      setDeclarantWallet("");
      await fetchDelegations();
    } catch (err) {
      console.error("Erro ao autorizar:", err);
      setError(err instanceof Error ? err.message : "Falha ao autorizar declaração");
    } finally {
      setActionLoading(null);
    }
  };

  const handleRevoke = async (wallet: string) => {
    if (!window.confirm(`Tem certeza que deseja revogar a autorização de ${wallet.slice(0, 10)}...?`)) {
      return;
    }

    setError(null);
    setActionLoading(wallet);
    try {
      const res = await fetch(
        `${API_BASE_URL}/api/v1/delegation/revoke?producer_id=${encodeURIComponent(producerId)}&declarant_wallet=${encodeURIComponent(wallet)}`,
        {
          method: "POST",
          headers,
        }
      );
      if (!res.ok) {
        const errBody = await res.text().catch(() => "Erro desconhecido");
        throw new Error(`Erro ${res.status}: ${errBody}`);
      }
      await fetchDelegations();
    } catch (err) {
      console.error("Erro ao revogar:", err);
      setError(err instanceof Error ? err.message : "Falha ao revogar autorização");
    } finally {
      setActionLoading(null);
    }
  };

  if (loading && delegations.length === 0) {
    return (
      <div className="min-h-screen bg-background">
        <LoadingSpinner message="Carregando delegações..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <Link
            href="/producer"
            className="p-2 rounded-md border hover:bg-muted transition"
          >
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <div className="flex-1">
            <h1 className="text-3xl font-bold tracking-tight">Delegação CBAM</h1>
            <p className="text-muted-foreground">
              Autorize declarantes a gerenciar certificados em seu nome
            </p>
          </div>
          <button
            onClick={fetchDelegations}
            disabled={loading}
            className="inline-flex items-center gap-2 px-3 py-2 rounded-md border hover:bg-muted transition disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
            Atualizar
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="p-4 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
          </div>
        )}

        {/* Authorize Form */}
        <div className="border rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <UserPlus className="h-5 w-5" />
            Autorizar Novo Declarante
          </h2>
          <form onSubmit={handleAuthorize} className="flex gap-3">
            <input
              type="text"
              placeholder="Carteira do Declarante (0x...)"
              value={declarantWallet}
              onChange={(e) => setDeclarantWallet(e.target.value)}
              required
              className="flex-1 px-3 py-2 rounded-md border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary font-mono text-sm"
            />
            <button
              type="submit"
              disabled={actionLoading === "authorize" || !declarantWallet.trim()}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {actionLoading === "authorize" ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  Autorizando...
                </>
              ) : (
                <>
                  <UserPlus className="h-4 w-4" />
                  Autorizar
                </>
              )}
            </button>
          </form>
        </div>

        {/* Delegations Table */}
        <div className="border rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b bg-muted/50">
                  <th className="text-left py-3 px-4 font-medium text-sm">Declarante (Wallet)</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Autorizado em</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Expira em</th>
                  <th className="text-left py-3 px-4 font-medium text-sm">Ações</th>
                </tr>
              </thead>
              <tbody>
                {delegations.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-12 text-center text-muted-foreground">
                      <UserPlus className="h-8 w-8 mx-auto mb-2 opacity-50" />
                      <p>Nenhuma autorização ativa.</p>
                      <p className="text-sm mt-1">
                        Use o formulário acima para autorizar um declarante.
                      </p>
                    </td>
                  </tr>
                ) : (
                  delegations.map((d) => (
                    <tr key={d.id || d.declarant_address} className="border-b hover:bg-muted/30">
                      <td className="py-3 px-4 font-mono text-xs">
                        {d.declarant_address}
                      </td>
                      <td className="py-3 px-4">
                        {d.status === "active" ? (
                          <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                            <CheckCircle className="h-3 w-3" />
                            Ativa
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400">
                            <XCircle className="h-3 w-3" />
                            Revogada
                          </span>
                        )}
                      </td>
                      <td className="py-3 px-4 text-sm text-muted-foreground">
                        {d.created_at
                          ? new Date(d.created_at).toLocaleDateString("pt-BR")
                          : "N/A"}
                      </td>
                      <td className="py-3 px-4 text-sm text-muted-foreground">
                        {d.valid_until
                          ? new Date(d.valid_until).toLocaleDateString("pt-BR")
                          : "N/A"}
                      </td>
                      <td className="py-3 px-4">
                        {d.status === "active" && (
                          <button
                            onClick={() => handleRevoke(d.declarant_address)}
                            disabled={actionLoading === d.declarant_address}
                            className="inline-flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium bg-red-100 text-red-800 hover:bg-red-200 dark:bg-red-900/30 dark:text-red-400 dark:hover:bg-red-900/50 transition disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <Trash2 className="h-3 w-3" />
                            {actionLoading === d.declarant_address ? "Revogando..." : "Revogar"}
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

        {/* Info Card */}
        <div className="border rounded-lg p-4 bg-muted/30">
          <h3 className="text-sm font-semibold mb-2">Sobre Delegação CBAM</h3>
          <p className="text-sm text-muted-foreground">
            A delegação permite que um declarante (exportador) realize ações em nome do produtor
            de hidrogênio verde. Isso é essencial para o processo de conformidade CBAM, onde o
            exportador precisa acessar certificados para submissão às autoridades europeias.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function DelegationPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-background flex items-center justify-center">
        <LoadingSpinner message="Carregando..." />
      </div>
    }>
      <DelegationContent />
    </Suspense>
  );
}
