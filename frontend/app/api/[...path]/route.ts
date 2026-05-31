import { NextRequest, NextResponse } from 'next/server';

/**
 * Proxy de API do H2V-Trust
 * 
 * Encaminha requisições de /api/:path* para o backend em BACKEND_URL/api/v1/:path*
 * 
 * IMPORTANTE: Este arquivo está em app/api/[...path]/route.ts, então o path
 * capturado já inclui o prefixo "v1" quando a URL é /api/v1/....
 * Exemplo: /api/v1/reports/cbam/2026/download → path = ['v1', 'reports', 'cbam', '2026', 'download']
 * 
 * Suporta tanto respostas JSON quanto binárias (PDF, CSV, ZIP).
 * 
 * A variável de ambiente BACKEND_URL deve apontar para o serviço backend:
 *   - Docker: http://backend:8000
 *   - Local:  http://localhost:8000
 */

function getBackendURL(): string {
  // 1. BACKEND_URL é a variável principal (definida no .env.local)
  if (process.env.BACKEND_URL) {
    return process.env.BACKEND_URL;
  }
  // 2. Fallback para NEXT_PUBLIC_API_URL
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  // 3. Fallback baseado no ambiente
  return process.env.NODE_ENV === 'production'
    ? 'http://backend:8000'
    : 'http://localhost:8000';
}

export async function GET(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return proxyRequest(request, params.path, 'GET');
}

export async function POST(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return proxyRequest(request, params.path, 'POST');
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return proxyRequest(request, params.path, 'PUT');
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return proxyRequest(request, params.path, 'DELETE');
}

async function proxyRequest(
  request: NextRequest,
  pathSegments: string[],
  method: string
): Promise<NextResponse> {
  const backendUrl = getBackendURL();
  const path = pathSegments.join('/');
  const searchParams = request.nextUrl.searchParams.toString();
  // NOTA: O path já inclui o prefixo "v1" quando a URL é /api/v1/...
  // Exemplo: /api/v1/reports/cbam/2026/download → path = "v1/reports/cbam/2026/download"
  // Por isso NÃO adicionamos /api/v1/ novamente aqui.
  const targetUrl = `${backendUrl}/api/${path}${searchParams ? `?${searchParams}` : ''}`;

  try {
    // Construir headers para o backend
    const headers = new Headers();
    
    // Copiar headers relevantes do request original
    const headerNames = [
      'content-type',
      'authorization',
      'x-api-key',
      'x-tenant-id',
      'accept',
    ];
    for (const name of headerNames) {
      const value = request.headers.get(name);
      if (value) {
        headers.set(name, value);
      }
    }

    // Configurar opções do fetch
    const fetchOptions: RequestInit = {
      method,
      headers,
    };

    // Para métodos com body, copiar o body
    if (method !== 'GET' && method !== 'HEAD') {
      fetchOptions.body = request.body;
      // Node.js >= 18 exige duplex: 'half' para streams no fetch
      (fetchOptions as any).duplex = 'half';
    }

    // Fazer a requisição para o backend
    const response = await fetch(targetUrl, fetchOptions);

    // Construir a resposta
    const responseHeaders = new Headers();
    
    // Copiar headers relevantes da resposta do backend
    const responseHeaderNames = [
      'content-type',
      'content-disposition',
      'content-length',
      'cache-control',
      'etag',
    ];
    for (const name of responseHeaderNames) {
      const value = response.headers.get(name);
      if (value) {
        responseHeaders.set(name, value);
      }
    }

    // Ler o body da resposta
    const responseBody = await response.arrayBuffer();

    // Retornar a resposta com o mesmo status e body
    return new NextResponse(responseBody, {
      status: response.status,
      statusText: response.statusText,
      headers: responseHeaders,
    });
  } catch (error) {
    console.error(`[API Proxy] Erro ao encaminhar requisição para ${targetUrl}:`, error);
    return NextResponse.json(
      {
        detail: 'Erro de conexão com o backend',
        message: error instanceof Error ? error.message : 'Erro desconhecido',
      },
      { status: 502 }
    );
  }
}
