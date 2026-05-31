"use client";

import { useState, useEffect, useCallback } from "react";
import { useAuth } from "@/hooks/useAuth";
import { API_BASE_URL } from "@/lib/constants";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

interface Tenant {
  id: string;
  name: string;
  slug: string;
  status: string;
  contact_email: string;
  created_at: string;
  api_key: string | null;
}

interface TenantListResponse {
  tenants: Tenant[];
  total: number;
}

interface UserTenant {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_primary: boolean;
}

export default function AdminTenantsPage() {
  const { getToken } = useAuth();
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTenant, setSelectedTenant] = useState<Tenant | null>(null);
  const [tenantUsers, setTenantUsers] = useState<UserTenant[]>([]);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showUsersDialog, setShowUsersDialog] = useState(false);
  const [showInviteDialog, setShowInviteDialog] = useState(false);

  // Create tenant form
  const [newName, setNewName] = useState("");
  const [newSlug, setNewSlug] = useState("");
  const [newEmail, setNewEmail] = useState("");
  const [creating, setCreating] = useState(false);

  // Invite user form
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("operator");
  const [inviting, setInviting] = useState(false);

  const fetchTenants = useCallback(async () => {
    const token = getToken();
    if (!token) return;

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/admin/tenants`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error(`Erro ${response.status}`);
      const data: TenantListResponse = await response.json();
      setTenants(data.tenants);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao carregar tenants");
    } finally {
      setLoading(false);
    }
  }, [getToken]);

  const fetchTenantUsers = useCallback(async (tenantId: string) => {
    const token = getToken();
    if (!token) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/admin/tenants/${tenantId}/users`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (!response.ok) throw new Error(`Erro ${response.status}`);
      const data = await response.json();
      setTenantUsers(data.users || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao carregar usuários");
    }
  }, [getToken]);

  useEffect(() => {
    fetchTenants();
  }, [fetchTenants]);

  const handleCreateTenant = async () => {
    const token = getToken();
    if (!token || !newName || !newSlug || !newEmail) return;

    setCreating(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/admin/tenants`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: newName,
          slug: newSlug,
          contact_email: newEmail,
        }),
      });
      if (!response.ok) throw new Error(`Erro ${response.status}`);
      
      setShowCreateDialog(false);
      setNewName("");
      setNewSlug("");
      setNewEmail("");
      await fetchTenants();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao criar tenant");
    } finally {
      setCreating(false);
    }
  };

  const handleInviteUser = async () => {
    const token = getToken();
    if (!token || !selectedTenant || !inviteEmail) return;

    setInviting(true);
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/admin/tenants/${selectedTenant.id}/users`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: inviteEmail,
            role: inviteRole,
          }),
        }
      );
      if (!response.ok) throw new Error(`Erro ${response.status}`);
      
      setShowInviteDialog(false);
      setInviteEmail("");
      await fetchTenantUsers(selectedTenant.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao convidar usuário");
    } finally {
      setInviting(false);
    }
  };

  const handleRemoveUser = async (userId: string) => {
    const token = getToken();
    if (!token || !selectedTenant) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/admin/tenants/${selectedTenant.id}/users/${userId}`,
        {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (!response.ok) throw new Error(`Erro ${response.status}`);
      await fetchTenantUsers(selectedTenant.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao remover usuário");
    }
  };

  const openUsersDialog = async (tenant: Tenant) => {
    setSelectedTenant(tenant);
    setShowUsersDialog(true);
    await fetchTenantUsers(tenant.id);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin h-8 w-8 border-4 border-emerald-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Tenants</h1>
          <p className="text-slate-400 text-sm mt-1">
            Gerencie as organizações cadastradas na plataforma
          </p>
        </div>
        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
          <DialogTrigger asChild>
            <Button className="bg-emerald-600 hover:bg-emerald-500 text-white">
              + Novo Tenant
            </Button>
          </DialogTrigger>
          <DialogContent className="bg-slate-800 border-slate-700">
            <DialogHeader>
              <DialogTitle className="text-white">Criar Novo Tenant</DialogTitle>
              <DialogDescription className="text-slate-400">
                Adicione uma nova organização à plataforma
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name" className="text-slate-300">Nome</Label>
                <Input
                  id="name"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  placeholder="Produtor Gama Ltda"
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="slug" className="text-slate-300">Slug</Label>
                <Input
                  id="slug"
                  value={newSlug}
                  onChange={(e) => setNewSlug(e.target.value)}
                  placeholder="produtor-gama"
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email" className="text-slate-300">Email de Contato</Label>
                <Input
                  id="email"
                  type="email"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                  placeholder="admin@produtor-gama.com"
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
            </div>
            <DialogFooter>
              <Button
                variant="outline"
                onClick={() => setShowCreateDialog(false)}
                className="border-slate-600 text-slate-300"
              >
                Cancelar
              </Button>
              <Button
                onClick={handleCreateTenant}
                disabled={creating || !newName || !newSlug || !newEmail}
                className="bg-emerald-600 hover:bg-emerald-500 text-white"
              >
                {creating ? "Criando..." : "Criar Tenant"}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
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

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-400">
              Total de Tenants
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-white">{total}</p>
          </CardContent>
        </Card>
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-400">
              Ativos
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-emerald-400">
              {tenants.filter((t) => t.status === "active").length}
            </p>
          </CardContent>
        </Card>
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-400">
              Inativos
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-slate-400">
              {tenants.filter((t) => t.status !== "active").length}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tenants Table */}
      <Card className="bg-slate-800 border-slate-700">
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left p-4 text-sm font-medium text-slate-400">Nome</th>
                  <th className="text-left p-4 text-sm font-medium text-slate-400">Slug</th>
                  <th className="text-left p-4 text-sm font-medium text-slate-400">Status</th>
                  <th className="text-left p-4 text-sm font-medium text-slate-400">Contato</th>
                  <th className="text-left p-4 text-sm font-medium text-slate-400">Criado em</th>
                  <th className="text-right p-4 text-sm font-medium text-slate-400">Ações</th>
                </tr>
              </thead>
              <tbody>
                {tenants.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="p-8 text-center text-slate-500">
                      Nenhum tenant encontrado
                    </td>
                  </tr>
                ) : (
                  tenants.map((tenant) => (
                    <tr
                      key={tenant.id}
                      className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors"
                    >
                      <td className="p-4">
                        <span className="text-white font-medium">{tenant.name}</span>
                      </td>
                      <td className="p-4">
                        <code className="text-sm text-slate-400">{tenant.slug}</code>
                      </td>
                      <td className="p-4">
                        <Badge
                          variant={tenant.status === "active" ? "default" : "secondary"}
                          className={
                            tenant.status === "active"
                              ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                              : "bg-slate-500/10 text-slate-400 border-slate-500/20"
                          }
                        >
                          {tenant.status === "active" ? "Ativo" : "Inativo"}
                        </Badge>
                      </td>
                      <td className="p-4 text-sm text-slate-300">
                        {tenant.contact_email}
                      </td>
                      <td className="p-4 text-sm text-slate-400">
                        {new Date(tenant.created_at).toLocaleDateString("pt-BR")}
                      </td>
                      <td className="p-4 text-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => openUsersDialog(tenant)}
                          className="text-slate-400 hover:text-white"
                        >
                          Usuários
                        </Button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Users Dialog */}
      <Dialog open={showUsersDialog} onOpenChange={setShowUsersDialog}>
        <DialogContent className="bg-slate-800 border-slate-700 max-w-2xl">
          <DialogHeader>
            <DialogTitle className="text-white">
              Usuários - {selectedTenant?.name}
            </DialogTitle>
            <DialogDescription className="text-slate-400">
              Gerencie os usuários deste tenant
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            {tenantUsers.length === 0 ? (
              <p className="text-center text-slate-500 py-4">
                Nenhum usuário neste tenant
              </p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-slate-700">
                      <th className="text-left p-3 text-sm font-medium text-slate-400">Nome</th>
                      <th className="text-left p-3 text-sm font-medium text-slate-400">Email</th>
                      <th className="text-left p-3 text-sm font-medium text-slate-400">Perfil</th>
                      <th className="text-right p-3 text-sm font-medium text-slate-400">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tenantUsers.map((user) => (
                      <tr key={user.id} className="border-b border-slate-700/50">
                        <td className="p-3 text-white">{user.full_name}</td>
                        <td className="p-3 text-slate-300">{user.email}</td>
                        <td className="p-3">
                          <Badge
                            variant="outline"
                            className={
                              user.role === "admin"
                                ? "border-purple-500/30 text-purple-400"
                                : user.role === "operator"
                                ? "border-emerald-500/30 text-emerald-400"
                                : "border-blue-500/30 text-blue-400"
                            }
                          >
                            {user.role}
                          </Badge>
                        </td>
                        <td className="p-3 text-right">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleRemoveUser(user.id)}
                            className="text-red-400 hover:text-red-300 hover:bg-red-500/10"
                          >
                            Remover
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            <div className="flex justify-end">
              <Dialog open={showInviteDialog} onOpenChange={setShowInviteDialog}>
                <DialogTrigger asChild>
                  <Button
                    variant="outline"
                    className="border-emerald-600 text-emerald-400 hover:bg-emerald-500/10"
                  >
                    + Convidar Usuário
                  </Button>
                </DialogTrigger>
                <DialogContent className="bg-slate-800 border-slate-700">
                  <DialogHeader>
                    <DialogTitle className="text-white">Convidar Usuário</DialogTitle>
                    <DialogDescription className="text-slate-400">
                      Adicione um usuário ao tenant {selectedTenant?.name}
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="invite-email" className="text-slate-300">Email</Label>
                      <Input
                        id="invite-email"
                        type="email"
                        value={inviteEmail}
                        onChange={(e) => setInviteEmail(e.target.value)}
                        placeholder="usuario@exemplo.com"
                        className="bg-slate-700 border-slate-600 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="invite-role" className="text-slate-300">Perfil</Label>
                      <select
                        id="invite-role"
                        value={inviteRole}
                        onChange={(e) => setInviteRole(e.target.value)}
                        className="w-full p-2 rounded-md bg-slate-700 border border-slate-600 text-white"
                      >
                        <option value="operator">Operator</option>
                        <option value="auditor">Auditor</option>
                      </select>
                    </div>
                  </div>
                  <DialogFooter>
                    <Button
                      variant="outline"
                      onClick={() => setShowInviteDialog(false)}
                      className="border-slate-600 text-slate-300"
                    >
                      Cancelar
                    </Button>
                    <Button
                      onClick={handleInviteUser}
                      disabled={inviting || !inviteEmail}
                      className="bg-emerald-600 hover:bg-emerald-500 text-white"
                    >
                      {inviting ? "Convidando..." : "Convidar"}
                    </Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
