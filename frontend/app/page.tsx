// app/page.tsx
export default function LandingPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-green-900 via-emerald-800 to-teal-900">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <h1 className="text-5xl font-bold text-white">
              H2V-Trust
            </h1>
            <span className="bg-emerald-500/20 text-emerald-300 text-xs px-2 py-1 rounded-full border border-emerald-500/30">
              v1.0.0
            </span>
          </div>
          <p className="text-xl text-emerald-100 mb-8">
            Certificação Blockchain para Hidrogênio Verde<br />
            Conformidade com CBAM 2026
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <a
              href="/dashboard"
              className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3 px-6 rounded-lg transition"
            >
              Dashboard
            </a>
            <a
              href="/auditor"
              className="bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white font-semibold py-3 px-6 rounded-lg transition"
            >
              Portal do Auditor
            </a>
            <a
              href="/producer"
              className="bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white font-semibold py-3 px-6 rounded-lg transition"
            >
              Portal do Produtor
            </a>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl">
            <h3 className="text-xl font-semibold text-white mb-2">Blockchain Imutável</h3>
            <p className="text-emerald-100">Certificados SBT não-transferíveis, prevenindo double counting.</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl">
            <h3 className="text-xl font-semibold text-white mb-2">CBAM 2026 Ready</h3>
            <p className="text-emerald-100">Limite de 3.4 kgCO₂e/kgH₂, verificação por terceiros.</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl">
            <h3 className="text-xl font-semibold text-white mb-2">Rastreabilidade Total</h3>
            <p className="text-emerald-100">Do sensor no Pecém ao QR Code em Roterdã.</p>
          </div>
        </div>
      </div>
    </main>
  );
}
