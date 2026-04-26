import { NextRequest, NextResponse } from 'next/server';

// Configuração do backend
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const API_TIMEOUT = parseInt(process.env.API_TIMEOUT || '10000'); // 10 segundos

// Headers que serão repassados do frontend para o backend
const FORWARDED_HEADERS = [
  'authorization',
  'content-type',
  'accept',
  'user-agent',
  'x-forwarded-for',
  'x-real-ip',
];

// Rotas que não precisam de autenticação
const PUBLIC_ROUTES = [
  '/api/health',
  '/api/docs',
  '/api/openapi.json',
  '/api/auth/login',
  '/api/auth/register',
];

// Métodos HTTP suportados
const SUPPORTED_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'];

export async function GET(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleProxyRequest(request, params, 'GET');
}

export async function POST(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleProxyRequest(request, params, 'POST');
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleProxyRequest(request, params, 'PUT');
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleProxyRequest(request, params, 'DELETE');
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleProxyRequest(request, params, 'PATCH');
}

export async function OPTIONS(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  return handleProxyRequest(request, params, 'OPTIONS');
}

async function handleProxyRequest(
  request: NextRequest,
  params: { path: string[] },
  method: string
) {
  try {
    // Construir o path da API
    const apiPath = `/${params.path.join('/')}`;
    const fullUrl = `${BACKEND_URL}${apiPath}`;

    // Log da requisição (apenas em desenvolvimento)
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Proxy] ${method} ${apiPath} -> ${fullUrl}`);
    }

    // Verificar se o método é suportado
    if (!SUPPORTED_METHODS.includes(method)) {
      return NextResponse.json(
        { error: `Método ${method} não suportado` },
        { status: 405 }
      );
    }

    // Verificar autenticação para rotas protegidas
    if (!isPublicRoute(apiPath)) {
      const authResult = await checkAuthentication(request);
      if (!authResult.authenticated) {
        return NextResponse.json(
          { error: 'Não autorizado', message: authResult.message },
          { status: 401 }
        );
      }
    }

    // Preparar headers para o backend
    const headers = prepareHeaders(request);

    // Preparar body para o backend
    let body: any = null;
    if (['POST', 'PUT', 'PATCH'].includes(method)) {
      const contentType = request.headers.get('content-type') || '';
      
      if (contentType.includes('application/json')) {
        body = await request.json();
      } else if (contentType.includes('multipart/form-data')) {
        // Para form-data, precisamos passar o stream
        body = request.body;
      } else if (contentType.includes('application/x-www-form-urlencoded')) {
        const formData = await request.formData();
        body = Object.fromEntries(formData.entries());
      } else {
        body = await request.text();
      }
    }

    // Fazer a requisição para o backend com timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

    try {
      const response = await fetch(fullUrl, {
        method,
        headers,
        body: body instanceof ReadableStream ? body : JSON.stringify(body),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Processar a resposta do backend
      return processBackendResponse(response, apiPath);

    } catch (fetchError: any) {
      clearTimeout(timeoutId);
      
      if (fetchError.name === 'AbortError') {
        return NextResponse.json(
          { error: 'Timeout da API', message: 'A requisição excedeu o tempo limite' },
          { status: 504 }
        );
      }

      throw fetchError;
    }

  } catch (error: any) {
    console.error('[API Proxy Error]', error);

    // Retornar erro apropriado
    return NextResponse.json(
      { 
        error: 'Erro interno do servidor',
        message: process.env.NODE_ENV === 'development' ? error.message : 'Tente novamente mais tarde'
      },
      { status: 500 }
    );
  }
}

function isPublicRoute(path: string): boolean {
  return PUBLIC_ROUTES.some(route => path.startsWith(route));
}

async function checkAuthentication(request: NextRequest): Promise<{ authenticated: boolean; message?: string }> {
  try {
    // Verificar token JWT no header Authorization
    const authHeader = request.headers.get('authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return { authenticated: false, message: 'Token de autenticação não fornecido' };
    }

    const token = authHeader.split(' ')[1];
    
    // Em produção, você validaria o token JWT aqui
    // Por enquanto, apenas verificamos se existe um token
    if (!token || token.length < 10) {
      return { authenticated: false, message: 'Token inválido' };
    }

    // Opcional: Validar o token com o backend de autenticação
    if (process.env.VALIDATE_TOKENS === 'true') {
      const validationResponse = await fetch(`${BACKEND_URL}/api/auth/validate`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (!validationResponse.ok) {
        return { authenticated: false, message: 'Token inválido ou expirado' };
      }
    }

    return { authenticated: true };

  } catch (error) {
    console.error('[Auth Check Error]', error);
    return { authenticated: false, message: 'Erro na verificação de autenticação' };
  }
}

function prepareHeaders(request: NextRequest): HeadersInit {
  const headers: Record<string, string> = {};

  // Copiar headers relevantes do frontend
  FORWARDED_HEADERS.forEach(headerName => {
    const value = request.headers.get(headerName);
    if (value) {
      headers[headerName] = value;
    }
  });

  // Adicionar headers específicos do proxy
  headers['x-forwarded-host'] = request.headers.get('host') || '';
  headers['x-forwarded-proto'] = request.headers.get('x-forwarded-proto') || 'http';
  headers['x-forwarded-for'] = request.headers.get('x-forwarded-for') || request.ip || '';

  // Adicionar CORS headers se necessário
  if (!headers['origin']) {
    headers['origin'] = request.headers.get('origin') || `${request.nextUrl.protocol}//${request.nextUrl.host}`;
  }

  return headers;
}

async function processBackendResponse(response: Response, apiPath: string): Promise<NextResponse> {
  // Determinar o content type da resposta
  const contentType = response.headers.get('content-type') || '';
  
  // Clonar headers importantes
  const responseHeaders = new Headers();
  
  // Copiar headers do backend para o frontend
  const headersToForward = [
    'content-type',
    'content-length',
    'cache-control',
    'etag',
    'last-modified',
    'location',
  ];

  headersToForward.forEach(header => {
    const value = response.headers.get(header);
    if (value) {
      responseHeaders.set(header, value);
    }
  });

  // Adicionar CORS headers
  responseHeaders.set('access-control-allow-origin', '*');
  responseHeaders.set('access-control-allow-methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS');
  responseHeaders.set('access-control-allow-headers', 'Content-Type, Authorization');

  // Processar diferentes tipos de resposta
  if (contentType.includes('application/json')) {
    const data = await response.json();
    
    // Log de resposta (apenas em desenvolvimento)
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Proxy Response] ${apiPath}:`, {
        status: response.status,
        data: data
      });
    }

    return NextResponse.json(data, {
      status: response.status,
      headers: responseHeaders,
    });

  } else if (contentType.includes('text/')) {
    const text = await response.text();
    
    return new NextResponse(text, {
      status: response.status,
      headers: responseHeaders,
    });

  } else if (contentType.includes('application/octet-stream') || 
             contentType.includes('application/pdf') ||
             contentType.includes('image/')) {
    // Para arquivos binários
    const buffer = await response.arrayBuffer();
    
    return new NextResponse(buffer, {
      status: response.status,
      headers: responseHeaders,
    });

  } else {
    // Para outros tipos, retornar a resposta como está
    const body = response.body;
    
    return new NextResponse(body, {
      status: response.status,
      headers: responseHeaders,
    });
  }
}

// Configuração do route handler
export const dynamic = 'force-dynamic'; // Sempre executar dinamicamente
export const runtime = 'nodejs'; // Usar runtime Node.js
export const maxDuration = 30; // Timeout máximo de 30 segundos

