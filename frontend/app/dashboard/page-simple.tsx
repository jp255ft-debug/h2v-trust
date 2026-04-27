"use client";

import { useState } from "react";

export default function Dashboard() {
  const [timeRange, setTimeRange] = useState("month");

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Monitoramento de produ├º├úo de hidrog├¬nio verde
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700">Produ├º├úo Total</h3>
            <p className="text-3xl font-bold text-green-600 mt-2">28,000 kg</p>
            <p className="text-gray-500 text-sm mt-1">Junho 2024</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700">Conformidade</h3>
            <p className="text-3xl font-bold text-blue-600 mt-2">94%</p>
            <p className="text-gray-500 text-sm mt-1">Taxa de sucesso</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700">Emiss├Áes GHG</h3>
            <p className="text-3xl font-bold text-orange-600 mt-2">2.3 kgCOÔéée/kgHÔéé</p>
            <p className="text-gray-500 text-sm mt-1">M├®dia mensal</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700">Consumo de ├ügua</h3>
            <p className="text-3xl font-bold text-cyan-600 mt-2">11.6 L/kgHÔéé</p>
            <p className="text-gray-500 text-sm mt-1">M├®dia mensal</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Resumo do Sistema</h2>
          <p className="text-gray-600">
            Sistema de monitoramento H2V-Trust funcionando corretamente. 
            Todos os componentes est├úo operacionais e integrados.
          </p>
          <div className="mt-4 p-4 bg-green-50 rounded border border-green-200">
            <p className="text-green-700 font-medium">Ô£à Status: Operacional</p>
            <p className="text-green-600 text-sm mt-1">
              Frontend, backend e blockchain integrados com sucesso.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
