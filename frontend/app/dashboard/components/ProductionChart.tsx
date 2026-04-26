"use client";

import { useState, useEffect } from "react";
import { fetchBatches } from "@/lib/api";
import type { Batch } from "@/types/batch";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

interface ProductionChartProps {
  batches?: Batch[];
}

interface ChartData {
  name: string;
  producao: number;
  emissoes: number;
}

export default function ProductionChart({ batches: propBatches }: ProductionChartProps) {
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [isLoading, setIsLoading] = useState(!propBatches);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      if (propBatches) {
        processBatches(propBatches);
        return;
      }

      try {
        setIsLoading(true);
        const { batches } = await fetchBatches({ limit: 20 });
        processBatches(batches);
        setError(null);
      } catch (err) {
        console.error("Failed to load production data:", err);
        setError("Falha ao carregar dados de produção");
        setChartData(getSampleData());
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [propBatches]);

  const processBatches = (batches: Batch[]) => {
    if (batches.length === 0) {
      setChartData(getSampleData());
      return;
    }

    const data: ChartData[] = batches.slice(0, 10).map(batch => ({
      name: batch.id.slice(-6).toUpperCase(),
      producao: batch.size_kg / 1000,
      emissoes: batch.telemetry?.ghg_emissions || 0,
    }));

    setChartData(data.length > 0 ? data : getSampleData());
  };

  const getSampleData = (): ChartData[] => {
    return [
      { name: "Lote 01", producao: 1.8, emissoes: 2.3 },
      { name: "Lote 02", producao: 2.2, emissoes: 3.1 },
      { name: "Lote 03", producao: 1.5, emissoes: 2.8 },
      { name: "Lote 04", producao: 1.9, emissoes: 3.5 },
      { name: "Lote 05", producao: 2.1, emissoes: 2.1 },
      { name: "Lote 06", producao: 1.7, emissoes: 2.6 },
      { name: "Lote 07", producao: 2.0, emissoes: 2.9 },
      { name: "Lote 08", producao: 1.6, emissoes: 2.4 },
    ];
  };

  if (isLoading) {
    return (
      <div className="bg-card text-card-foreground rounded-lg border shadow-sm p-6 h-80 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
          <p className="mt-2 text-sm text-muted-foreground">Carregando dados de produção...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-card text-card-foreground rounded-lg border shadow-sm p-6 h-80 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 mb-2">⚠️</div>
          <p className="text-sm text-muted-foreground">{error}</p>
          <p className="text-xs text-muted-foreground mt-1">Mostrando dados de demonstração</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card text-card-foreground rounded-lg border shadow-sm p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold">Produção vs Emissões</h3>
        <p className="text-sm text-muted-foreground">Comparativo entre produção e emissões por lote</p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis dataKey="name" className="text-xs" />
            <YAxis className="text-xs" />
            <Tooltip />
            <Legend />
            <Bar dataKey="producao" fill="#10B981" name="Produção (ton)" radius={[4, 4, 0, 0]} />
            <Bar dataKey="emissoes" fill="#F59E0B" name="Emissões (kgCO₂e/kgH₂)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
