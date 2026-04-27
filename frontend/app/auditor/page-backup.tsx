"use client";

import { useState } from "react";
import Link from "next/link";
import { Search, CheckCircle, Cloud, FileText } from "lucide-react";

export default function AuditorPageBackup() {
  const [search, setSearch] = useState("");
  const [searchResult, setSearchResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = () => {
    setIsLoading(true);
    setTimeout(() => {
      setSearchResult({
        id: "cert_001",
        batchId: "batch_045",
        producer: "Produtor A",
        ghgEmissions: 2.3,
        waterConsumption: 11.8,
        isCompliant: true,
        verifiedAt: "2024-06-15",
      });
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-6">
            <Link href="/" className="text-xl font-bold text-gray-900">H2V-Trust</Link>
            <div className="flex gap-4">
              <Link href="/dashboard" className="text-sm font-medium text-gray-600 hover:text-blue-600">Dashboard</Link>
              <Link href="/auditor" className="text-sm font-medium text-blue-600">Auditor</Link>
              <Link href="/producer" className="text-sm font-medium text-gray-600 hover:text-blue-600">Produtor</Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Auditor H2V-Trust</h1>
          <p className="text-gray-600 mt-2">
            Sistema de auditoria e verificação de certificados de hidrogênio verde
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Pesquisar Certificados</h2>
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Digite ID do certificado, produtor ou lote..."
              className="flex-1 border rounded-md px-4 py-2"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button
              onClick={handleSearch}
              disabled={isLoading}
              className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {isLoading ? "Buscando..." : "Pesquisar"}
            </button>
          </div>

          {searchResult && (
            <div className="mt-6 p-4 border rounded-lg bg-gray-50">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold">Certificado {searchResult.id}</h3>
                  <p className="text-sm text-gray-500">Lote: {searchResult.batchId}</p>
                  <p className="text-sm text-gray-500">Produtor: {searchResult.producer}</p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${searchResult.isCompliant ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}>
                  {searchResult.isCompliant ? "Conforme" : "Não conforme"}
                </span>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-4">
                <div>
                  <p className="text-xs text-gray-500">Emissões GHG</p>
                  <p className="font-semibold">{searchResult.ghgEmissions} kgCO₂e/kgH₂</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Consumo de Água</p>
                  <p className="font-semibold">{searchResult.waterConsumption} L/kgH₂</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Verificado em</p>
                  <p className="font-semibold">{searchResult.verifiedAt}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm font-medium text-gray-500">Certificados Verificados</p>
            <p className="text-3xl font-bold text-blue-600">1,248</p>
            <p className="text-gray-500 text-sm mt-1">Total auditado</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm font-medium text-gray-500">Conformidade</p>
            <p className="text-3xl font-bold text-blue-600">96.7%</p>
            <p className="text-gray-500 text-sm mt-1">Taxa de aprovação</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Emissões Médias</h3>
            <p className="text-3xl font-bold text-orange-600">2.1 kgCO₂e/kgH₂</p>
            <p className="text-gray-500 text-sm mt-1">Abaixo do limite CBAM</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow">
          <div className="p-6">
            <h2 className="text-xl font-semibold text-gray-800">Status do Sistema</h2>
          </div>
          <div className="p-6 pt-0 space-y-4">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded">
              <span className="text-green-700">✅ Módulo de Auditoria</span>
              <span className="px-2 py-1 bg-green-100 text-green-800 text-sm rounded">Operacional</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded">
              <span className="text-blue-700">🔗 Conexão Blockchain</span>
              <span className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded">Configurada</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
