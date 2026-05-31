const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  // NOTA: O proxy da API é feito via route.ts em app/api/[...path]/route.ts
  // que suporta blobs binários (PDF, CSV) e passa headers corretamente.
  // O rewrites() foi removido porque entra em conflito com o route.ts
  // e causa duplicação do prefixo /api/v1/ na URL de destino.
  images: {
    domains: ['localhost', 'h2vtrust.com.br', 'www.h2vtrust.com.br', 'h2v-trust-api.onrender.com'],
  },
  // Força o webpack a resolver o alias @ corretamente
  webpack: (config) => {
    config.resolve.alias['@'] = path.resolve(__dirname, 'src');
    return config;
  },
  // Configuração para Turbopack (usado pelo Render e Vercel)
  experimental: {
    turbo: {
      resolveAlias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
  },
};

module.exports = nextConfig;
