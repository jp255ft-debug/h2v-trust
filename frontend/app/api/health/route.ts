import { NextResponse } from 'next/server';
import dns from 'dns';
import http from 'http';

// Resolve o nome do host manualmente para evitar o bug de DNS do Node.js 20
// que ignora dns.setDefaultResultOrder('verbatim') em alguns contextos.
function resolveHost(hostname: string): Promise<string> {
  return new Promise((resolve, reject) => {
    dns.lookup(hostname, { all: true, verbatim: true }, (err, addresses) => {
      if (err) return reject(err);
      // Prefere IPv4
      const ipv4 = addresses.find(a => a.family === 4);
      resolve(ipv4 ? ipv4.address : addresses[0].address);
    });
  });
}

function httpGet(hostname: string, port: number, path: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const options = {
      hostname,
      port,
      path,
      method: 'GET',
      family: 4, // Força IPv4
    };
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data);
        } else {
          reject(new Error(`HTTP ${res.statusCode}`));
        }
      });
    });
    req.on('error', (err: NodeJS.ErrnoException) => {
      reject(new Error(`${err.code || 'UNKNOWN'}: ${err.message}`));
    });
    req.end();
  });
}

export async function GET() {
  try {
    // Em produção (Docker), o backend está no serviço 'backend:8000'
    // Em dev local, usar .env.local com BACKEND_URL
    const backendHost = process.env.BACKEND_HOST || 'backend';
    const backendPort = parseInt(process.env.BACKEND_PORT || '8000', 10);
    
    // Resolve o hostname manualmente para evitar bug de DNS
    const resolvedIp = await resolveHost(backendHost);
    
    const data = await httpGet(resolvedIp, backendPort, '/health');
    const parsed = JSON.parse(data);
    return NextResponse.json(parsed);
  } catch (error) {
    return NextResponse.json(
      { 
        status: 'error', 
        message: 'Backend unreachable',
        detail: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 502 }
    );
  }
}

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
