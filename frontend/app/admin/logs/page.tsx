"use client";

import { useState, useEffect, useCallback } from "react";
import { useAuth } from "@/hooks/useAuth";
import { API_BASE_URL } from "@/lib/constants";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface AuditLog {
  id: string;
  user_id: string;
  user_email: string;
  tenant_id: string | null;
  tenant_name: string | null;
  action: string;
  resource: string;
  resource_id: string | null;
  details: Record<string, unknown> | null;
  ip_address: string | null;
  created_at: string;
}

interface AuditLogResponse {
  logs: AuditLog[];
  total: number;
  page: number;
  page_size: number;
}

const ACTION_COLORS: Record<string, string> = {
  create: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  update: "bg-blue-500/10 text-blue-400 border-blue-500/20",
  delete: "bg-red-500/10 text-red-400 border-red-500/20",
  login: "bg-purple-500/10 text-purple-400 border-purple-500/20",
  invite: "bg-amber-500/10 text-amber-400 border-amber-500/20",
  remove: "bg-red-500/10 text-red-400 border-red-500/20",
};

export default function AdminLogsPage() {
  const { getToken } = useAuth();
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTenant, setSearchTenant] = useState("");
  const [searchAction, setSearchAction] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const pageSize = 20;

  const fetchLogs = useCallback(async () => {
    const token = getToken();
    if (!token) return;

    setLoading(true);
    try {
      const params = new URLSearchParams({
        page: String(page),
        page_size: String(pageSize),
      });
      if (searchTenant) params.set("tenant_id", searchTenant);
      if (searchAction) params.set("action", searchAction);
      if (dateFrom) params.set("date_from", dateFrom);
      if (dateTo) params.set("date_to", dateTo);

      const response = await fetch(
        `${API_BASE_URL}/api/v1/admin/audit-logs?${params.toString()}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (!response.ok) throw new Error(`Erro ${response.status}`);
      const data: AuditLogResponse = await response.json();
      setLogs(data.logs);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao carregar logs");
    } finally {
      setLoading(false);
    }
  }, [getToken, page, searchTenant, searchAction, dateFrom, dateTo]);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  const totalPages = Math.ceil(total / pageSize);

  const formatAction = (action: string) => {
    const labels: Record<string, string> = {
      create: "Criação",
      update: "Atualização",
      delete: "Exclusão",
      login: "Login",
      invite: "Convite",
      remove: "Remoção",
    };
    return labels[action] || action;
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Logs de Auditoria</h1>
        <p className="text-slate-400 text-sm mt-1">
          Registro de todas as ações administrativas na plataforma
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-[200px]">
          <Input
            placeholder="Filtrar por tenant ID..."
            value={searchTenant}
            onChange={(e) => {
              setSearchTenant(e.target.value);
              setPage(1);
            }}
            className="bg-slate-800 border-slate-700 text-white placeholder:text-slate-500"
          />
        </div>
        <div className="w-48">
          <select
            value={searchAction}
            onChange={(e) => {
              setSearchAction(e.target.value);
              setPage(1);
            }}
            className="w-full p-2 rounded-md bg-slate-800 border border-slate-700 text-white"
          >
            <option value="">Todas as ações</option>
            <option value="create">Criação</option>
            <option value="update">Atualização</option>
            <option value="delete">Exclusão</option>
            <option value="login">Login</option>
            <option value="invite">Convite</option>
            <option value="remove">Remoção</option>
          </select>
        </div>
        <div className="w-44">
          <Input
            type="date"
            value={dateFrom}
            onChange={(e) => {
              setDateFrom(e.target.value);
              setPage(1);
            }}
            className="bg-slate-800 border-slate-700 text-white"
            placeholder="Data início"
          />
        </div>
        <div className="w-44">
          <Input
            type="date"
            value={dateTo}
            onChange={(e) => {
              setDateTo(e.target.value);
              setPage(1);
            }}
            className="bg-slate-800 border-slate-700 text-white"
            placeholder="Data fim"
          />
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="p-3 rounded-md bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          {error}
          <button
            onClick={() => setError(null)}
            className="ml-2 text-red-300 hover:text-red-200"
          >
            ×
          </button>
        </div>
      )}

      {/* Logs Table */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm font-medium text-slate-400">
            {total} registro{total !== 1 ? "s" : ""} encontrado{total !== 1 ? "s" : ""}
          </CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin h-8 w-8 border-4 border-emerald-500 border-t-transparent rounded-full" />
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left p-4 text-sm font-medium text-slate-400">Data/Hora</th>
                    <th className="text-left p-4 text-sm font-medium text-slate-400">Usuário</th>
                    <th className="text-left p-4 text-sm font-medium text-slate-400">Tenant</th>
                    <th className="text-left p-4 text-sm font-medium text-slate-400">Ação</th>
                    <th className="text-left p-4 text-sm font-medium text-slate-400">Recurso</th>
                    <th className="text-left p-4 text-sm font-medium text-slate-400">IP</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="p-8 text-center text-slate-500">
                        Nenhum log encontrado
                      </td>
                    </tr>
                  ) : (
                    logs.map((log) => (
                      <tr
                        key={log.id}
                        className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors"
                      >
                        <td className="p-4 text-sm text-slate-300 whitespace-nowrap">
                          {formatTimestamp(log.created_at)}
                        </td>
                        <td className="p-4">
                          <div>
                            <p className="text-sm text-white">{log.user_email}</p>
                            <p className="text-xs text-slate-500">{log.user_id.slice(0, 8)}...</p>
                          </div>
                        </td>
                        <td className="p-4 text-sm text-slate-300">
                          {log.tenant_name || (
                            <span className="text-slate-500 italic">Sistema</span>
                          )}
                        </td>
                        <td className="p-4">
                          <Badge
                            variant="outline"
                            className={
                              ACTION_COLORS[log.action] ||
                              "bg-slate-500/10 text-slate-400 border-slate-500/20"
                            }
                          >
                            {formatAction(log.action)}
                          </Badge>
                        </td>
                        <td className="p-4">
                          <div>
                            <p className="text-sm text-slate-300">{log.resource}</p>
                            {log.resource_id && (
                              <p className="text-xs text-slate-500">
                                {log.resource_id.slice(0, 12)}...
                              </p>
                            )}
                          </div>
                        </td>
                        <td className="p-4 text-sm text-slate-500 font-mono">
                          {log.ip_address || "—"}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-slate-400">
            Página {page} de {totalPages}
          </p>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="border-slate-600 text-slate-300"
            >
              Anterior
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
              className="border-slate-600 text-slate-300"
            >
              Próxima
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
