"use client";

import { useState, useEffect } from "react";
import { fetchStats } from "@/lib/api";

interface EmissionsGaugeProps {
  avgEmissions?: number;
}

export default function EmissionsGauge({ avgEmissions: propAvgEmissions }: EmissionsGaugeProps) {
  const [avgEmissions, setAvgEmissions] = useState<number>(propAvgEmissions || 0);
  const [isLoading, setIsLoading] = useState(!propAvgEmissions);
  const [error, setError] = useState<string | null>(null);

  const CBAM_LIMIT = 3.4; // kgCO2e/kgH2
  const TARGET = 2.0; // Target emissions level

  useEffect(() => {
    const loadData = async () => {
      if (propAvgEmissions !== undefined) {
        setAvgEmissions(propAvgEmissions);
        return;
      }

      try {
        setIsLoading(true);
        const stats = await fetchStats();
        setAvgEmissions(stats.avgEmissions);
        setError(null);
      } catch (err) {
        console.error("Failed to load emissions data:", err);
        setError("Falha ao carregar dados de emiss├Áes");
        // Fallback to sample data
        setAvgEmissions(2.1);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [propAvgEmissions]);

  const calculatePercentage = (value: number, max: number) => {
    return Math.min((value / max) * 100, 100);
  };

  const getEmissionsLevel = (value: number) => {
    if (value <= TARGET) return "Excelente";
    if (value <= CBAM_LIMIT) return "Dentro do Limite";
    return "Acima do Limite";
  };

  const getEmissionsColor = (value: number) => {
    if (value <= TARGET) return "text-green-600 dark:text-green-400";
    if (value <= CBAM_LIMIT) return "text-yellow-600 dark:text-yellow-400";
    return "text-red-600 dark:text-red-400";
  };

  const getGaugeColor = (value: number) => {
    if (value <= TARGET) return "#10B981"; // green
    if (value <= CBAM_LIMIT) return "#F59E0B"; // yellow
    return "#EF4444"; // red
  };

  const getGaugeBackgroundColor = (value: number) => {
    if (value <= TARGET) return "bg-green-100 dark:bg-green-900/30";
    if (value <= CBAM_LIMIT) return "bg-yellow-100 dark:bg-yellow-900/30";
    return "bg-red-100 dark:bg-red-900/30";
  };

  const emissionsPercentage = calculatePercentage(avgEmissions, CBAM_LIMIT);
  const targetPercentage = calculatePercentage(TARGET, CBAM_LIMIT);
  const gaugeColor = getGaugeColor(avgEmissions);
  const gaugeBgClass = getGaugeBackgroundColor(avgEmissions);

  if (isLoading) {
    return (
      <div className="bg-card text-card-foreground rounded-lg border shadow-sm p-6 h-80 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
          <p className="mt-2 text-sm text-muted-foreground">Carregando dados de emiss├Áes...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-card text-card-foreground rounded-lg border shadow-sm p-6 h-80 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 mb-2">ÔÜá´©Å</div>
          <p className="text-sm text-muted-foreground">{error}</p>
          <p className="text-xs text-muted-foreground mt-1">Mostrando dados de demonstra├º├úo</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card text-card-foreground rounded-lg border shadow-sm p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold">Emiss├Áes de GHG</h3>
        <p className="text-sm text-muted-foreground">M├®dia de emiss├Áes por kg de HÔéé produzido</p>
      </div>

      <div className="flex flex-col items-center justify-center">
        {/* Circular Gauge */}
        <div className="relative w-48 h-48 mb-6">
          {/* Background circle */}
          <div className="absolute inset-0 rounded-full bg-gray-100 dark:bg-gray-800"></div>
          
          {/* Emissions fill */}
          <div 
            className="absolute inset-4 rounded-full"
            style={{
              background: `conic-gradient(${gaugeColor} 0% ${emissionsPercentage}%, #E5E7EB ${emissionsPercentage}% 100%)`
            }}
          ></div>
          
          {/* Inner circle */}
          <div className="absolute inset-8 rounded-full bg-card"></div>
          
          {/* Center content */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className="text-3xl font-bold" style={{ color: gaugeColor }}>
              {avgEmissions.toFixed(1)}
            </div>
            <div className="text-sm text-muted-foreground">kgCOÔéée/kgHÔéé</div>
            <div className={`text-xs font-medium mt-1 ${getEmissionsColor(avgEmissions)}`}>
              {getEmissionsLevel(avgEmissions)}
            </div>
          </div>
          
          {/* Target marker */}
          <div 
            className="absolute top-0 left-1/2 w-1 h-4 -translate-x-1/2"
            style={{ 
              transform: `translateX(-50%) rotate(${targetPercentage * 3.6}deg)`,
              transformOrigin: 'center 96px'
            }}
          >
            <div className="w-3 h-3 rounded-full bg-purple-600 border-2 border-card"></div>
          </div>
        </div>

        {/* Legend and details */}
        <div className="w-full space-y-4">
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Limite CBAM:</span>
              <span className="font-medium">{CBAM_LIMIT} kgCOÔéée/kgHÔéé</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Meta:</span>
              <span className="font-medium text-purple-600 dark:text-purple-400">{TARGET} kgCOÔéée/kgHÔéé</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Atual:</span>
              <span className={`font-medium ${getEmissionsColor(avgEmissions)}`}>
                {avgEmissions.toFixed(1)} kgCOÔéée/kgHÔéé
              </span>
            </div>
          </div>

          {/* Progress bars */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">Baixo</span>
              <span className="text-xs text-muted-foreground">Alto</span>
            </div>
            <div className="h-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div 
                className="h-full rounded-full"
                style={{ 
                  width: `${emissionsPercentage}%`,
                  backgroundColor: gaugeColor
                }}
              ></div>
            </div>
            <div className="flex justify-between text-xs">
              <span className="text-green-600 dark:text-green-400">0</span>
              <span className="text-yellow-600 dark:text-yellow-400">{TARGET}</span>
              <span className="text-red-600 dark:text-red-400">{CBAM_LIMIT}</span>
            </div>
          </div>

          {/* Status indicators */}
          <div className={`p-3 rounded-lg ${gaugeBgClass} border ${getEmissionsColor(avgEmissions).replace('text-', 'border-')}`}>
            <div className="flex items-start gap-2">
              <div className={`mt-0.5 w-3 h-3 rounded-full ${getEmissionsColor(avgEmissions).replace('text-', 'bg-')}`}></div>
              <div>
                <p className="text-sm font-medium">
                  {getEmissionsLevel(avgEmissions)} - {((CBAM_LIMIT - avgEmissions) / CBAM_LIMIT * 100).toFixed(1)}% abaixo do limite
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {avgEmissions <= CBAM_LIMIT 
                    ? "Em conformidade com os requisitos CBAM da UE" 
                    : "Acima do limite CBAM - requer aten├º├úo"}
                </p>
              </div>
            </div>
          </div>

          {/* Savings calculation */}
          <div className="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
            <p className="text-sm font-medium text-blue-700 dark:text-blue-400">
              Economia estimada de carbono
            </p>
            <p className="text-xs text-blue-600 dark:text-blue-500 mt-1">
              Comparado com hidrog├¬nio cinza (10 kgCOÔéée/kgHÔéé): {(10 - avgEmissions).toFixed(1)} kgCOÔéée/kgHÔéé
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
