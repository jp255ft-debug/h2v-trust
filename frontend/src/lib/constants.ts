// API Configuration
// Em produção (via Nginx), usa caminho relativo para o proxy reverso
// Em desenvolvimento, usa localhost:8000 diretamente
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "";
export const API_PREFIX = "/api/v1";

// CBAM Constants
export const CBAM_GHG_LIMIT_KGCO2_PER_KGH2 = 3.4;
export const CBAM_PENALTY_EUR_PER_TON = 50;
export const WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2 = 20;

// Energy Sources
export const RENEWABLE_SOURCES = ["wind", "solar", "hydro", "biomass"] as const;
export const NON_RENEWABLE_SOURCES = ["grid", "natural_gas", "coal", "diesel"] as const;

// Water Sources
export const ALLOWED_WATER_SOURCES = [
  "desalination",
  "treated_wastewater",
  "surface_water",
  "groundwater",
  "recycled",
] as const;

// Batch Defaults
export const DEFAULT_BATCH_SIZE_KG = 1000;

// Blockchain
export const GAS_LIMIT_MINT = 200000;
export const GAS_PRICE_GWEI = 30;

// Route paths
export const ROUTES = {
  HOME: "/",
  DASHBOARD: "/dashboard",
  AUDITOR: "/auditor",
  AUDITOR_VERIFY: (batchId: string) => `/auditor/verify/${batchId}`,
  PRODUCER: "/producer",
  PRODUCER_BATCHES: "/producer/batches",
  PRODUCER_CERTIFICATES: "/producer/certificates",
  PRODUCER_DELEGATION: "/producer/delegation",
} as const;

// API Endpoints
export const API_ENDPOINTS = {
  HEALTH: "/health",
  TELEMETRY: `${API_PREFIX}/telemetry`,
  BATCHES: `${API_PREFIX}/batches`,
  BATCH: (id: string) => `${API_PREFIX}/batches/${id}`,
  BATCH_COMPLIANCE: (id: string) => `${API_PREFIX}/batches/${id}/compliance`,
  CERTIFICATES: `${API_PREFIX}/certificates`,
  CERTIFICATE: (id: string) => `${API_PREFIX}/certificates/${id}`,
  CERTIFICATE_CONSUME: (id: string) => `${API_PREFIX}/certificates/${id}/consume`,
  COMPLIANCE_CHECK: (batchId: string) => `${API_PREFIX}/compliance/check/${batchId}`,
  COMPLIANCE_VALIDATE: `${API_PREFIX}/compliance/validate`,
  DELEGATION_AUTHORIZE: `${API_PREFIX}/delegation/authorize`,
  DELEGATION_STATUS: (producerId: string) => `${API_PREFIX}/delegation/status/${producerId}`,
  DELEGATION_REVOKE: `${API_PREFIX}/delegation/revoke`,
  REPORTS_CBAM: (year: number) => `${API_PREFIX}/reports/cbam/${year}`,
  REPORTS_CBAM_DOWNLOAD: (year: number) => `${API_PREFIX}/reports/cbam/${year}/download`,
} as const;

// Status labels
export const BATCH_STATUS = {
  COMPLIANT: { label: "Verificado", color: "bg-green-100 text-green-800" },
  NON_COMPLIANT: { label: "Atenção Necessária", color: "bg-red-100 text-red-800" },
  PENDING: { label: "Pendente", color: "bg-yellow-100 text-yellow-800" },
} as const;
