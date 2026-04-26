"use client";

import { useState } from "react";

export default function AuditorPage() {
  const [search, setSearch] = useState("");

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Auditor H2V-Trust</h1>
          <p className="text-gray-600 mt-2">
            Sistema de auditoria e verificação de certificados de hidrogênio verde
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Pesquisar Certificados</h2>
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Digite ID do certificado, produtor ou lote..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Pesquisar
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Certificados Verificados</h3>
            <p className="text-3xl font-bold text-green-600">1,248</p>
            <p className="text-gray-500 text-sm mt-1">Total auditado</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Conformidade</h3>
            <p className="text-3xl font-bold text-blue-600">96.7%</p>
            <p className="text-gray-500 text-sm mt-1">Taxa de aprovação</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Emissões Médias</h3>
            <p className="text-3xl font-bold text-orange-600">2.1 kgCO₂e/kgH₂</p>
            <p className="text-gray-500 text-sm mt-1">Abaixo do limite CBAM</p>
          </div>
        </div>

        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Status do Sistema</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded">
              <span className="text-green-700">✅ Módulo de Auditoria</span>
              <span className="px-2 py-1 bg-green-100 text-green-800 text-sm rounded">Operacional</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded">
              <span className="text-blue-700">🔗 Conexão Blockchain</span>
              <span className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded">Configurada</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-purple-50 rounded">
              <span className="text-purple-700">📊 Banco de Dados</span>
              <span className="px-2 py-1 bg-purple-100 text-purple-800 text-sm rounded">Sincronizado</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}