export interface ComplianceCheckRequest {
  batch_id: string;
  ghg_emissions_kgCO2_per_kgH2: number;
  water_consumption_liters: number;
  water_source: string;
  energy_source: string;
  h2_kg: number;
}

export interface ComplianceCheckResponse {
  is_compliant: boolean;
  checks: Record<string, CheckDetail>;
  violations: string[];
  cbam_report?: CBAMReport;
}

export interface CheckDetail {
  ok: boolean;
  message: string;
}

export interface CBAMReport {
  declared_emissions_tco2: number;
  saved_emissions_vs_grey: number;
  certificate_eligible: boolean;
}

export interface ComplianceValidateRequest {
  batch_id: string;
  validator_wallet: string;
}

export interface ComplianceReportResponse {
  batch_id: string;
  is_compliant: boolean;
  ghg_emissions: number;
  water_consumption: number;
  energy_source: string;
  compliance_details: Record<string, unknown>;
  generated_at: string;
}

export interface DelegationCreateRequest {
  producer_id: string;
  declarant_address: string;
  valid_until: string;
}

export interface DelegationResponse {
  id: string;
  producer_id: string;
  producer_wallet?: string;
  declarant_address: string;
  valid_until?: string;
  status: string;
  blockchain_tx_hash?: string;
  revoked_at?: string;
  created_at?: string;
}

export interface DelegationStatusResponse {
  producer_id: string;
  has_active_delegation: boolean;
  declarant_address?: string;
  valid_until?: string;
  created_at?: string;
}

export interface DelegationRevokeRequest {
  producer_id: string;
}

export interface DelegationRevokeResponse {
  producer_id: string;
  status: string;
  revoked_at: string;
  message: string;
}
