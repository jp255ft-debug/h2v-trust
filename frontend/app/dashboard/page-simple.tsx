"use client";

import Link from "next/link";

export default function DashboardSimple() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-6">
            <Link href="/" className="text-xl font-bold text-gray-900">H2V-Trust</Link>
            <div className="flex gap-4">
              <Link href="/dashboard" className="text-sm font-medium text-blue-600">Dashboard</Link>
              <Link href="/auditor" className="text-sm font-medium text-gray-600 hover:text-blue-600">Auditor</Link>
              <Link href="/producer" className="text-sm font-medium text-gray-600 hover:text-blue-600">Produtor</Link>
            </div>
          </div>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard H2V-Trust</h1>
          <p className="text-gray-600 mt-2">
            Monitoramento de produção de hidrogênio verde
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700">Produção Total</h3>
            <p className="text-3xl font-bold text-green-600 mt-2">28,000 kg</p>
            <p className="text-gray-500 text-sm mt-1">Total acumulado</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700">Emissões GHG</h3>
            <p className="text-3xl font-bold text-orange-600 mt-2">2.3 kgCO₂e/kgH₂</p>
            <p className="text-gray-500 text-sm mt-1">Média mensal</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700">Consumo de Água</h3>
            <p className="text-3xl font-bold text-cyan-600 mt-2">11.6 L/kgH₂</p>
            <p className="text-gray-500 text-sm mt-1">Média mensal</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700">Conformidade</h3>
            <p className="text-3xl font-bold text-green-600 mt-2">96.7%</p>
            <p className="text-gray-500 text-sm mt-1">Taxa de aprovação</p>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Status do Sistema</h2>
          <p className="text-gray-600">
            Sistema de monitoramento H2V-Trust funcionando corretamente.
          </p>
          <p className="text-gray-600 mt-2">
            Todos os componentes estão operacionais e integrados.
          </p>
        </div>
      </div>
    </div>
  );
}
