"use client";

import { useState, useEffect, useCallback } from "react";
import { fetchCertificate, verifyCertificate, consumeCertificate } from "../lib/api";
import type { Certificate, CertificateVerifyResponse } from "../types/certificate";

interface UseCertificateReturn {
  certificate: Certificate | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

interface UseCertificateVerifyReturn {
  verification: CertificateVerifyResponse | null;
  isLoading: boolean;
  error: string | null;
  verify: () => Promise<void>;
}

interface UseCertificateConsumeReturn {
  isConsuming: boolean;
  result: { status: string; tx_hash: string } | null;
  error: string | null;
  consume: (consumerWallet: string) => Promise<void>;
}

export function useCertificate(certificateId: string): UseCertificateReturn {
  const [certificate, setCertificate] = useState<Certificate | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCertificate = useCallback(async () => {
    if (!certificateId) return;
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchCertificate(certificateId);
      setCertificate(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load certificate");
      setCertificate(null);
    } finally {
      setIsLoading(false);
    }
  }, [certificateId]);

  useEffect(() => {
    loadCertificate();
  }, [loadCertificate]);

  return { certificate, isLoading, error, refetch: loadCertificate };
}

export function useCertificateVerify(certificateId: string): UseCertificateVerifyReturn {
  const [verification, setVerification] = useState<CertificateVerifyResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const verify = useCallback(async () => {
    if (!certificateId) return;
    try {
      setIsLoading(true);
      setError(null);
      const data = await verifyCertificate(certificateId);
      setVerification(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to verify certificate");
      setVerification(null);
    } finally {
      setIsLoading(false);
    }
  }, [certificateId]);

  return { verification, isLoading, error, verify };
}

export function useCertificateConsume(certificateId: string): UseCertificateConsumeReturn {
  const [isConsuming, setIsConsuming] = useState(false);
  const [result, setResult] = useState<{ status: string; tx_hash: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const consume = useCallback(async (consumerWallet: string) => {
    if (!certificateId) return;
    try {
      setIsConsuming(true);
      setError(null);
      const data = await consumeCertificate(certificateId, consumerWallet);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to consume certificate");
      setResult(null);
    } finally {
      setIsConsuming(false);
    }
  }, [certificateId]);

  return { isConsuming, result, error, consume };
}
