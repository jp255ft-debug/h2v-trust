import type { CBAMReport } from "./compliance";

export interface Batch {
  id: string;
  telemetry_id?: number;
  producer_wallet?: string;
  producer_id?: string;
  facility_id?: string;
  production_location?: string;
  size_kg: number;
  is_compliant: boolean;
  blockchain_status?: string;
  compliance_report?: ComplianceReport;
  batch_hash?: string;
  telemetry?: TelemetrySummary;
  created_at?: string;
}

export interface ComplianceReport {
  is_compliant: boolean;
  checks: ComplianceChecks;
  violations: string[];
  cbam_report?: CBAMReport;
  score?: number;
  standard?: string;
  ghg_emissions?: number;
  ghg_limit?: number;
  ghg_compliant?: boolean;
  water_consumption?: number;
  water_limit?: number;
  water_compliant?: boolean;
  energy_source?: string;
  water_source?: string;
}

export interface ComplianceChecks {
  ghg: CheckResult;
  water: CheckResult;
  energy: CheckResult;
  additionality: CheckResult;
}

export interface CheckResult {
  ok: boolean;
  message: string;
}

export interface TelemetrySummary {
  id: number;
  sensor_id: string;
  timestamp?: string;
  energy_source: string;
  power_generated_mwh: number;
  ghg_emissions: number;
  water_consumption_liters: number;
  water_source?: string;
}

export interface BatchListResponse {
  batches: Batch[];
  total: number;
}

export interface BatchFilters {
  producer_id?: string;
  compliant_only?: boolean;
  skip?: number;
  limit?: number;
}
