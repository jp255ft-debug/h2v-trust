const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Configuração para produção com domínio personalizado
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/v1/:path*`,
      },
    ];
  },
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
