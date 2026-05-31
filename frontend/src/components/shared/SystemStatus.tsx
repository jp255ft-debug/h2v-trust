"use client";

import { useState, useEffect } from "react";

interface ServiceStatus {
  name: string;
  icon: string;
  description: string;
  status: "online" | "offline" | "checking";
  statusLabel: string;
}

export default function SystemStatus() {
  const [services, setServices] = useState<ServiceStatus[]>([
    { name: "Backend API", icon: "🔗", description: "FastAPI na porta 8000", status: "checking", statusLabel: "Verificando..." },
    { name: "Banco de Dados", icon: "📊", description: "TimescaleDB", status: "checking", statusLabel: "Verificando..." },
    { name: "Blockchain", icon: "⚙️", description: "Hardhat Local Node", status: "checking", statusLabel: "Verificando..." },
    { name: "Cache", icon: "⚡", description: "Redis", status: "checking", statusLabel: "Verificando..." },
  ]);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        // Usa caminho relativo para passar pelo proxy do Next.js
        // Em dev: /api/health → next.config.js rewrite → http://localhost:8000/health
        // Em prod: /api/health → next.config.js rewrite → http://backend:8000/health
        const res = await fetch(`/api/health`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          signal: AbortSignal.timeout(5000),
        });


        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const data = await res.json();

        setServices([
          {
            name: "Backend API",
            icon: "🔗",
            description: `FastAPI - ${data.status || "rodando"}`,
            status: data.status === "healthy" || data.status === "ok" ? "online" : "offline",
            statusLabel: data.status === "healthy" || data.status === "ok" ? "Operacional" : "Instável",
          },
          {
            name: "Banco de Dados",
            icon: "📊",
            description: "TimescaleDB",
            status: data.checks?.database?.details?.connected === true ? "online" : "offline",
            statusLabel: data.checks?.database?.details?.connected === true ? "Online" : "Offline",
          },
          {
            name: "Blockchain",
            icon: "⚙️",
            description: data.checks?.blockchain?.details?.chain_id ? `Chain ID: ${data.checks.blockchain.details.chain_id}` : "Hardhat Local Node",
            status: data.checks?.blockchain?.details?.connected === true ? "online" : "offline",
            statusLabel: data.checks?.blockchain?.details?.connected === true ? "Conectada" : "Desconectada",
          },
          {
            name: "Cache",
            icon: "⚡",
            description: "Redis",
            status: data.checks?.redis?.details?.connected === true ? "online" : "offline",
            statusLabel: data.checks?.redis?.details?.connected === true ? "Online" : "Offline",
          },
        ]);
      } catch (err) {
        // Se o health check falhar, marca tudo como offline
        setServices([
          { name: "Backend API", icon: "🔗", description: "FastAPI na porta 8000", status: "offline", statusLabel: "Offline" },
          { name: "Banco de Dados", icon: "📊", description: "TimescaleDB", status: "offline", statusLabel: "Offline" },
          { name: "Blockchain", icon: "⚙️", description: "Hardhat Local Node", status: "offline", statusLabel: "Offline" },
          { name: "Cache", icon: "⚡", description: "Redis", status: "offline", statusLabel: "Offline" },
        ]);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Re-check a cada 30s
    return () => clearInterval(interval);
  }, []);

  const getStatusColors = (status: "online" | "offline" | "checking") => {
    switch (status) {
      case "online":
        return {
          bg: "bg-green-50 dark:bg-green-950/20",
          border: "border-green-200 dark:border-green-800",
          text: "text-green-700 dark:text-green-400",
          subtext: "text-green-600 dark:text-green-500",
          badge: "bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200",
        };
      case "offline":
        return {
          bg: "bg-red-50 dark:bg-red-950/20",
          border: "border-red-200 dark:border-red-800",
          text: "text-red-700 dark:text-red-400",
          subtext: "text-red-600 dark:text-red-500",
          badge: "bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200",
        };
      default:
        return {
          bg: "bg-yellow-50 dark:bg-yellow-950/20",
          border: "border-yellow-200 dark:border-yellow-800",
          text: "text-yellow-700 dark:text-yellow-400",
          subtext: "text-yellow-600 dark:text-yellow-500",
          badge: "bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200",
        };
    }
  };

  return (
    <div className="bg-card rounded-lg border shadow-sm">
      <div className="p-6">
        <h2 className="text-xl font-semibold text-foreground">Status do Sistema</h2>
        <p className="text-sm text-muted-foreground mt-1">Health check em tempo real via API</p>
      </div>
      <div className="p-6 pt-0 space-y-4">
        {services.map((service) => {
          const colors = getStatusColors(service.status);
          return (
            <div
              key={service.name}
              className={`flex items-center justify-between p-4 rounded-lg border ${colors.bg} ${colors.border}`}
            >
              <div>
                <p className={`font-medium ${colors.text}`}>
                  {service.icon} {service.name}
                </p>
                <p className={`text-sm ${colors.subtext}`}>{service.description}</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${colors.badge}`}>
                {service.statusLabel}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
