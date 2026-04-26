"use client";

import { useState, useEffect, useCallback } from "react";
import { fetchBatches, fetchBatch, fetchBatchCompliance } from "../lib/api";
import type { Batch, BatchListResponse, BatchFilters } from "../types/batch";
import type { ComplianceReportResponse } from "../types/compliance";

interface UseBatchReturn {
  batches: Batch[];
  total: number;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

interface UseBatchDetailReturn {
  batch: Batch | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

interface UseBatchComplianceReturn {
  compliance: ComplianceReportResponse | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useBatches(filters: BatchFilters = {}): UseBatchReturn {
  const [batches, setBatches] = useState<Batch[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadBatches = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchBatches(filters);
      setBatches(data.batches);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load batches");
      setBatches([]);
      setTotal(0);
    } finally {
      setIsLoading(false);
    }
  }, [JSON.stringify(filters)]);

  useEffect(() => {
    loadBatches();
  }, [loadBatches]);

  return { batches, total, isLoading, error, refetch: loadBatches };
}

export function useBatchDetail(batchId: string): UseBatchDetailReturn {
  const [batch, setBatch] = useState<Batch | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadBatch = useCallback(async () => {
    if (!batchId) return;
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchBatch(batchId);
      setBatch(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load batch");
      setBatch(null);
    } finally {
      setIsLoading(false);
    }
  }, [batchId]);

  useEffect(() => {
    loadBatch();
  }, [loadBatch]);

  return { batch, isLoading, error, refetch: loadBatch };
}

export function useBatchCompliance(batchId: string): UseBatchComplianceReturn {
  const [compliance, setCompliance] = useState<ComplianceReportResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCompliance = useCallback(async () => {
    if (!batchId) return;
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchBatchCompliance(batchId);
      setCompliance(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load compliance");
      setCompliance(null);
    } finally {
      setIsLoading(false);
    }
  }, [batchId]);

  useEffect(() => {
    loadCompliance();
  }, [loadCompliance]);

  return { compliance, isLoading, error, refetch: loadCompliance };
}
