"use client";

import { useState, useCallback } from "react";
import { checkCompliance, validateCompliance, fetchDelegationStatus, authorizeDelegation, revokeDelegation } from "../lib/api";
import type { ComplianceCheckResponse, DelegationStatusResponse, DelegationResponse, DelegationRevokeResponse } from "../types/compliance";

interface UseComplianceCheckReturn {
  result: ComplianceCheckResponse | null;
  isLoading: boolean;
  error: string | null;
  check: (batchId: string) => Promise<void>;
}

interface UseComplianceValidateReturn {
  result: { status: string } | null;
  isLoading: boolean;
  error: string | null;
  validate: (batchId: string, validatorWallet: string) => Promise<void>;
}

interface UseDelegationReturn {
  status: DelegationStatusResponse | null;
  isLoading: boolean;
  error: string | null;
  fetchStatus: (producerId: string) => Promise<void>;
  authorize: (producerId: string, declarantAddress: string, validUntil: string) => Promise<DelegationResponse | null>;
  revoke: (producerId: string) => Promise<DelegationRevokeResponse | null>;
}

export function useComplianceCheck(): UseComplianceCheckReturn {
  const [result, setResult] = useState<ComplianceCheckResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const check = useCallback(async (batchId: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await checkCompliance(batchId);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Compliance check failed");
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { result, isLoading, error, check };
}

export function useComplianceValidate(): UseComplianceValidateReturn {
  const [result, setResult] = useState<{ status: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validate = useCallback(async (batchId: string, validatorWallet: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await validateCompliance(batchId, validatorWallet);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Validation failed");
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { result, isLoading, error, validate };
}

export function useDelegation(): UseDelegationReturn {
  const [status, setStatus] = useState<DelegationStatusResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async (producerId: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchDelegationStatus(producerId);
      setStatus(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch delegation status");
      setStatus(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const authorize = useCallback(async (producerId: string, declarantAddress: string, validUntil: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await authorizeDelegation(producerId, declarantAddress, validUntil);
      setStatus({
        producer_id: data.producer_id,
        has_active_delegation: data.status === "active",
        declarant_address: data.declarant_address,
        valid_until: data.valid_until,
        created_at: data.created_at,
      });
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authorization failed");
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const revoke = useCallback(async (producerId: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await revokeDelegation(producerId);
      setStatus({
        producer_id: data.producer_id,
        has_active_delegation: false,
      });
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Revocation failed");
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { status, isLoading, error, fetchStatus, authorize, revoke };
}
