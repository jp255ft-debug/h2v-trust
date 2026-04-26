export interface Certificate {
  id: string;
  batch_id: string;
  token_id: number;
  blockchain_tx_hash: string;
  qr_code_data?: string;
  is_consumed: boolean;
  consumed_at?: string;
  created_at?: string;
}

export interface CertificateConsumeRequest {
  consumer_wallet: string;
  purpose: string;
}

export interface CertificateVerifyResponse {
  is_valid: boolean;
  token_id: number;
  batch_id?: string;
  producer?: string;
  emissions_data?: Record<string, unknown>;
  is_consumed: boolean;
  blockchain_verified: boolean;
}

export interface CertificateMintResult {
  certificate_id: string;
  tx_hash: string;
  token_id: number;
}
