"""Metrics collection and monitoring for H2V-Trust platform."""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from collections import defaultdict
import threading
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collects and aggregates platform metrics."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance
    
    def _initialize(self):
        """Initialize metrics collector."""
        self.metrics = {
            "api_requests": defaultdict(int),
            "api_errors": defaultdict(int),
            "api_latency": defaultdict(list),
            "batch_processing": {
                "total": 0,
                "compliant": 0,
                "non_compliant": 0,
                "errors": 0,
            },
            "certificate_operations": {
                "generated": 0,
                "minted": 0,
                "consumed": 0,
                "verified": 0,
            },
            "compliance_checks": {
                "total": 0,
                "passed": 0,
                "failed": 0,
            },
            "resource_usage": {
                "memory_mb": 0,
                "cpu_percent": 0,
                "active_connections": 0,
            },
            "timestamps": {
                "startup": datetime.utcnow().isoformat(),
                "last_reset": datetime.utcnow().isoformat(),
            },
        }
        self._lock = threading.RLock()
    
    def increment_api_request(self, endpoint: str, method: str = "GET"):
        """Increment API request counter."""
        with self._lock:
            key = f"{method}:{endpoint}"
            self.metrics["api_requests"][key] += 1
    
    def increment_api_error(self, endpoint: str, error_code: int, method: str = "GET"):
        """Increment API error counter."""
        with self._lock:
            key = f"{method}:{endpoint}:{error_code}"
            self.metrics["api_errors"][key] += 1
    
    def record_api_latency(self, endpoint: str, latency_ms: float, method: str = "GET"):
        """Record API latency."""
        with self._lock:
            key = f"{method}:{endpoint}"
            self.metrics["api_latency"][key].append(latency_ms)
            # Keep only last 1000 measurements
            if len(self.metrics["api_latency"][key]) > 1000:
                self.metrics["api_latency"][key] = self.metrics["api_latency"][key][-1000:]
    
    def increment_batch_processed(self, is_compliant: bool, had_error: bool = False):
        """Increment batch processing counters."""
        with self._lock:
            self.metrics["batch_processing"]["total"] += 1
            
            if had_error:
                self.metrics["batch_processing"]["errors"] += 1
            elif is_compliant:
                self.metrics["batch_processing"]["compliant"] += 1
            else:
                self.metrics["batch_processing"]["non_compliant"] += 1
    
    def increment_certificate_operation(self, operation: str):
        """Increment certificate operation counter."""
        with self._lock:
            if operation in self.metrics["certificate_operations"]:
                self.metrics["certificate_operations"][operation] += 1
    
    def increment_compliance_check(self, passed: bool):
        """Increment compliance check counter."""
        with self._lock:
            self.metrics["compliance_checks"]["total"] += 1
            
            if passed:
                self.metrics["compliance_checks"]["passed"] += 1
            else:
                self.metrics["compliance_checks"]["failed"] += 1
    
    def update_resource_usage(self, memory_mb: float, cpu_percent: float, connections: int):
        """Update resource usage metrics."""
        with self._lock:
            self.metrics["resource_usage"]["memory_mb"] = memory_mb
            self.metrics["resource_usage"]["cpu_percent"] = cpu_percent
            self.metrics["resource_usage"]["active_connections"] = connections
    
    def get_metrics(self, include_details: bool = True) -> Dict[str, Any]:
        """Get current metrics with optional aggregation."""
        with self._lock:
            metrics = self.metrics.copy()
            
            if not include_details:
                # Return only aggregated metrics
                aggregated = {
                    "api": {
                        "total_requests": sum(metrics["api_requests"].values()),
                        "total_errors": sum(metrics["api_errors"].values()),
                        "error_rate": (
                            sum(metrics["api_errors"].values()) / sum(metrics["api_requests"].values())
                            if sum(metrics["api_requests"].values()) > 0 else 0
                        ),
                    },
                    "batch_processing": metrics["batch_processing"],
                    "certificate_operations": metrics["certificate_operations"],
                    "compliance_checks": metrics["compliance_checks"],
                    "resource_usage": metrics["resource_usage"],
                    "uptime_seconds": (
                        datetime.utcnow() - datetime.fromisoformat(metrics["timestamps"]["startup"])
                    ).total_seconds(),
                }
                
                # Calculate average latencies
                aggregated["api"]["average_latency_ms"] = {}
                for key, latencies in metrics["api_latency"].items():
                    if latencies:
                        aggregated["api"]["average_latency_ms"][key] = sum(latencies) / len(latencies)
                
                return aggregated
            else:
                # Include detailed metrics
                return metrics
    
    def reset_metrics(self):
        """Reset all metrics (except startup timestamp)."""
        with self._lock:
            self._initialize()
            self.metrics["timestamps"]["startup"] = datetime.utcnow().isoformat()
            self.metrics["timestamps"]["last_reset"] = datetime.utcnow().isoformat()
            logger.info("Metrics reset")
    
    @contextmanager
    def measure_latency(self, endpoint: str, method: str = "GET"):
        """Context manager to measure API latency."""
        start_time = time.time()
        try:
            yield
        finally:
            latency_ms = (time.time() - start_time) * 1000
            self.record_api_latency(endpoint, latency_ms, method)


class PerformanceMonitor:
    """Monitors platform performance and generates alerts."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.alerts = []
        self.thresholds = {
            "api_error_rate": 0.05,  # 5% error rate
            "api_latency_p95_ms": 1000,  # 1 second P95 latency
            "batch_error_rate": 0.01,  # 1% batch processing errors
            "memory_usage_mb": 1024,  # 1GB memory limit
            "cpu_usage_percent": 80,  # 80% CPU limit
        }
    
    def check_performance(self) -> List[Dict[str, Any]]:
        """Check performance against thresholds and generate alerts."""
        metrics = self.metrics.get_metrics(include_details=False)
        alerts = []
        
        # Check API error rate
        error_rate = metrics["api"].get("error_rate", 0)
        if error_rate > self.thresholds["api_error_rate"]:
            alerts.append({
                "level": "WARNING",
                "metric": "api_error_rate",
                "value": error_rate,
                "threshold": self.thresholds["api_error_rate"],
                "message": f"API error rate {error_rate:.1%} exceeds threshold {self.thresholds['api_error_rate']:.1%}",
            })
        
        # Check API latency
        for endpoint, latency in metrics["api"].get("average_latency_ms", {}).items():
            if latency > self.thresholds["api_latency_p95_ms"]:
                alerts.append({
                    "level": "WARNING",
                    "metric": "api_latency",
                    "endpoint": endpoint,
                    "value": latency,
                    "threshold": self.thresholds["api_latency_p95_ms"],
                    "message": f"API latency for {endpoint}: {latency:.0f}ms exceeds threshold {self.thresholds['api_latency_p95_ms']}ms",
                })
        
        # Check batch error rate
        batch_total = metrics["batch_processing"]["total"]
        batch_errors = metrics["batch_processing"]["errors"]
        if batch_total > 0:
            batch_error_rate = batch_errors / batch_total
            if batch_error_rate > self.thresholds["batch_error_rate"]:
                alerts.append({
                    "level": "ERROR",
                    "metric": "batch_error_rate",
                    "value": batch_error_rate,
                    "threshold": self.thresholds["batch_error_rate"],
                    "message": f"Batch processing error rate {batch_error_rate:.1%} exceeds threshold {self.thresholds['batch_error_rate']:.1%}",
                })
        
        # Check resource usage
        memory_usage = metrics["resource_usage"]["memory_mb"]
        if memory_usage > self.thresholds["memory_usage_mb"]:
            alerts.append({
                "level": "WARNING",
                "metric": "memory_usage",
                "value": memory_usage,
                "threshold": self.thresholds["memory_usage_mb"],
                "message": f"Memory usage {memory_usage:.0f}MB exceeds threshold {self.thresholds['memory_usage_mb']}MB",
            })
        
        cpu_usage = metrics["resource_usage"]["cpu_percent"]
        if cpu_usage > self.thresholds["cpu_usage_percent"]:
            alerts.append({
                "level": "WARNING",
                "metric": "cpu_usage",
                "value": cpu_usage,
                "threshold": self.thresholds["cpu_usage_percent"],
                "message": f"CPU usage {cpu_usage:.0f}% exceeds threshold {self.thresholds['cpu_usage_percent']}%",
            })
        
        # Store alerts
        self.alerts.extend(alerts)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
        
        return alerts
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        metrics = self.metrics.get_metrics(include_details=False)
        alerts = self.check_performance()
        
        # Calculate health score (0-100)
        health_score = 100
        
        # Deductions for issues
        error_rate = metrics["api"].get("error_rate", 0)
        health_score -= min(30, error_rate * 100 * 30)  # Up to 30 points for error rate
        
        # Deduct for high latency
        max_latency = max(metrics["api"].get("average_latency_ms", {}).values(), default=0)
        if max_latency > 100:
            health_score -= min(20, (max_latency - 100) / 50 * 20)  # Up to 20 points for latency
        
        # Deduct for resource usage
        memory_ratio = metrics["resource_usage"]["memory_mb"] / self.thresholds["memory_usage_mb"]
        cpu_ratio = metrics["resource_usage"]["cpu_percent"] / self.thresholds["cpu_usage_percent"]
        resource_penalty = max(0, (max(memory_ratio, cpu_ratio) - 0.8) * 25)  # Penalty above 80% usage
        health_score -= min(25, resource_penalty)
        
        health_score = max(0, min(100, health_score))
        
        # Health level
        if health_score >= 90:
            health_level = "EXCELLENT"
        elif health_score >= 75:
            health_level = "GOOD"
        elif health_score >= 60:
            health_level = "FAIR"
        elif health_score >= 40:
            health_level = "POOR"
        else:
            health_level = "CRITICAL"
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "health_score": round(health_score, 1),
            "health_level": health_level,
            "metrics_summary": {
                "api_requests": metrics["api"]["total_requests"],
                "api_error_rate": round(error_rate * 100, 2),
                "batch_processed": metrics["batch_processing"]["total"],
                "certificates_generated": metrics["certificate_operations"]["generated"],
                "compliance_checks": metrics["compliance_checks"]["total"],
                "uptime_hours": round(metrics["uptime_seconds"] / 3600, 2),
            },
            "resource_usage": metrics["resource_usage"],
            "alerts": alerts,
            "recommendations": self._generate_recommendations(alerts, metrics),
        }
    
    def _generate_recommendations(
        self,
        alerts: List[Dict[str, Any]],
        metrics: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on performance issues."""
        recommendations = []
        
        # Check for high error rates
        if any(a["metric"] == "api_error_rate" for a in alerts):
            recommendations.append(
                "Investigate API error rate increase. Check logs for error patterns."
            )
        
        # Check for high latency
        if any(a["metric"] == "api_latency" for a in alerts):
            recommendations.append(
                "Optimize slow API endpoints. Consider caching or database indexing."
            )
        
        # Check for batch processing issues
        if any(a["metric"] == "batch_error_rate" for a in alerts):
            recommendations.append(
                "Review batch processing pipeline. Check telemetry data quality."
            )
        
        # Check for resource constraints
        if any(a["metric"] in ["memory_usage", "cpu_usage"] for a in alerts):
            recommendations.append(
                "Consider scaling resources or optimizing memory/cpu usage."
            )
        
        # General recommendations based on load
        if metrics["api"]["total_requests"] > 10000:
            recommendations.append(
                "High API load detected. Consider implementing rate limiting or scaling horizontally."
            )
        
        if metrics["batch_processing"]["total"] > 1000:
            recommendations.append(
                "High batch processing volume. Consider batch size optimization."
            )
        
        return recommendations


# Global metrics collector instance
metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return metrics_collector


def calculate_environmental_impact(
    ghg_emissions_kgco2_per_kgh2: float,
    batch_size_kg: float,
    water_consumption_liters_per_kgh2: float,
    energy_source: str,
) -> Dict[str, Any]:
    """
    Calculate environmental impact metrics for H2 production.
    
    Args:
        ghg_emissions_kgco2_per_kgh2: GHG emissions per kg H2
        batch_size_kg: Total batch size in kg
        water_consumption_liters_per_kgh2: Water consumption per kg H2
        energy_source: Source of energy (renewable, grid, etc.)
        
    Returns:
        Dictionary with environmental impact metrics
    """
    # Calculate totals
    total_emissions_kg = ghg_emissions_kgco2_per_kgh2 * batch_size_kg
    total_water_liters = water_consumption_liters_per_kgh2 * batch_size_kg
    
    # Calculate savings compared to grey hydrogen (assume 10 kgCO2/kgH2)
    grey_h2_emissions_per_kg = 10.0  # kgCO2/kgH2 for grey hydrogen
    emissions_saved_per_kg = grey_h2_emissions_per_kg - ghg_emissions_kgco2_per_kgh2
    total_emissions_saved_kg = emissions_saved_per_kg * batch_size_kg
    
    # Convert to meaningful equivalents
    # 1 kg CO2 = 4.6 km driven by average car (0.217 kg CO2/km)
    equivalent_car_km = total_emissions_kg / 0.217 if total_emissions_kg > 0 else 0
    
    # 1 tree absorbs ~21.77 kg CO2 per year
    equivalent_trees_needed = total_emissions_kg / 21.77 if total_emissions_kg > 0 else 0
    
    # Water equivalents
    # Olympic swimming pool = 2,500,000 liters
    equivalent_olympic_pools = total_water_liters / 2500000
    
    # Average person's daily water consumption = 150 liters
    equivalent_person_days = total_water_liters / 150
    
    # Energy source impact
    renewable_energy_sources = ["solar", "wind", "hydro", "geothermal", "biomass", "renewable"]
    is_renewable = energy_source.lower() in renewable_energy_sources
    
    # Environmental score (0-100, higher is better)
    emissions_score = max(0, 100 - (ghg_emissions_kgco2_per_kgh2 / grey_h2_emissions_per_kg) * 100)
    water_score = max(0, 100 - (water_consumption_liters_per_kgh2 / 20) * 100)  # 20 L/kgH2 as baseline
    energy_score = 100 if is_renewable else 50
    
    overall_score = (emissions_score * 0.5) + (water_score * 0.3) + (energy_score * 0.2)
    
    # Impact level
    if overall_score >= 90:
        impact_level = "EXCELLENT"
        recommendation = "Continue current practices"
    elif overall_score >= 75:
        impact_level = "GOOD"
        recommendation = "Minor improvements possible"
    elif overall_score >= 60:
        impact_level = "FAIR"
        recommendation = "Consider efficiency improvements"
    elif overall_score >= 40:
        impact_level = "POOR"
        recommendation = "Significant improvements needed"
    else:
        impact_level = "CRITICAL"
        recommendation = "Immediate action required"
    
    return {
        "batch_size_kg": round(batch_size_kg, 2),
        "ghg_emissions_kgco2_per_kgh2": round(ghg_emissions_kgco2_per_kgh2, 3),
        "total_emissions_kg": round(total_emissions_kg, 2),
        "water_consumption_liters_per_kgh2": round(water_consumption_liters_per_kgh2, 2),
        "total_water_liters": round(total_water_liters, 2),
        "energy_source": energy_source,
        "is_renewable": is_renewable,
        "emissions_savings": {
            "saved_per_kg": round(emissions_saved_per_kg, 3),
            "total_saved_kg": round(total_emissions_saved_kg, 2),
            "equivalent_car_km": round(equivalent_car_km, 2),
            "equivalent_trees_needed": round(equivalent_trees_needed, 2),
        },
        "water_equivalents": {
            "olympic_pools": round(equivalent_olympic_pools, 6),
            "person_days": round(equivalent_person_days, 2),
        },
        "environmental_scores": {
            "emissions": round(emissions_score, 1),
            "water": round(water_score, 1),
            "energy": round(energy_score, 1),
            "overall": round(overall_score, 1),
        },
        "impact_level": impact_level,
        "recommendation": recommendation,
        "calculation_timestamp": datetime.utcnow().isoformat(),
    }
