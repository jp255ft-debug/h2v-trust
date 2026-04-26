# CBAM 2026 constants
CBAM_GHG_LIMIT_KGCO2_PER_KGH2 = 3.4  # tCO2e/tH2 = 3.4 kgCO2e/kgH2
CBAM_PENALTY_EUR_PER_TON = 50  # maximum penalty for non-compliance
CBAM_DEFAULT_VALUE_MULTIPLIER = 2.5  # default values overestimate by ~2.5x

# Water Framework Directive
WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2 = 20  # based on electrolysis efficiency
ALLOWED_WATER_SOURCES = ["desalination", "treated_wastewater", "surface_water", "groundwater", "recycled"]

# Energy sources
RENEWABLE_SOURCES = ["wind", "solar", "hydro", "biomass"]
NON_RENEWABLE_SOURCES = ["grid", "natural_gas", "coal", "diesel"]

# Batch sizes
DEFAULT_BATCH_SIZE_KG = 1000  # 1 ton

# Blockchain
GAS_LIMIT_MINT = 200000
GAS_PRICE_GWEI = 30