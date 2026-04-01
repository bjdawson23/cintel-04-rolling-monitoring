"""
rolling_monitor_case.py - Project script (example).

Author: Branton Dawson
Date: 2026-04

Time-Series Air Quality Data

- Data is taken from a system that records air quality metrics over time.
- Each row represents one observation at a specific timestamp.
- The CSV file includes these columns:
  - timestamp: when the observation occurred
  - co_level: carbon monoxide level
  - no2_level: nitrogen dioxide level
  - o3_level: ozone level

Purpose

- Read time-series air quality metrics from a CSV file.
- Demonstrate rolling monitoring using a moving window.
- Compute rolling averages to smooth short-term variation.
- Save the resulting monitoring signals as a CSV artifact.
- Log the pipeline process to assist with debugging and transparency.

Questions to Consider

- How does air quality change over time?
- Why might a rolling average reveal patterns that individual observations hide?
- How can smoothing short-term variation help us understand longer-term trends?

Paths (relative to repo root)

    INPUT FILE: data/kc_air_co_data_2023.csv
    OUTPUT FILE: artifacts/air_quality_rolling_metrics.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.rolling_monitor_dawson_air_quality

OBS:
  Don't edit this file - it should remain a working example.
  Use as much of this code as you can when creating your own pipeline script,
  and change the monitoring logic as needed for your project.
"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P5", level="DEBUG")

# === DEFINE GLOBAL PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "kc_air_co_data_2023.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "air_quality_rolling_metrics.csv"

# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the pipeline.

    log_header() logs a standard run header.
    log_path() logs repo-relative paths (privacy-safe).
    """
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    # Ensure artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ----------------------------------------------------
    # STEP 1: READ CSV DATA FILE INTO A POLARS DATAFRAME (TABLE)
    # ----------------------------------------------------
    df = pl.read_csv(DATA_FILE)

    LOG.info(f"Loaded {df.height} time-series records")

    # ----------------------------------------------------
    # STEP 2: PARSE AND SORT DATA BY DATE
    # ----------------------------------------------------
    # Time-series analysis requires observations to be ordered.
    df = df.with_columns(pl.col("Date").str.to_date("%-m/%-d/%Y")).sort("Date")

    LOG.info("Parsed Date column and sorted records by Date")

    # ----------------------------------------------------
    # STEP 3: DEFINE A 30-DAY ROLLING WINDOW
    # ----------------------------------------------------
    # This dataset is daily, so a 30-row window represents ~30 days.
    WINDOW_SIZE: int = 30

    # ----------------------------------------------------
    # STEP 3.1: 30-DAY ROLLING MEAN OF CO CONCENTRATION
    # ----------------------------------------------------
    co_rolling_30d_mean_recipe: pl.Expr = (
        pl.col("Daily Max 8-hour CO Concentration")
        .rolling_mean(WINDOW_SIZE)
        .round(4)
        .alias("co_rolling_30d_mean")
    )

    # ----------------------------------------------------
    # STEP 3.2: 30-DAY ROLLING MEAN OF AQI
    # ----------------------------------------------------
    # Smooths daily AQI values into a monthly trend signal.
    aqi_rolling_30d_mean_recipe: pl.Expr = (
        pl.col("Daily AQI Value")
        .rolling_mean(WINDOW_SIZE)
        .round(4)
        .alias("aqi_rolling_30d_mean")
    )

    # ----------------------------------------------------
    # STEP 3.3: APPLY ROLLING RECIPES
    # ----------------------------------------------------
    df_with_rolling = df.with_columns(
        [
            co_rolling_30d_mean_recipe,
            aqi_rolling_30d_mean_recipe,
        ]
    )

    LOG.info("Computed 30-day rolling CO mean and AQI mean")

    # ----------------------------------------------------
    # STEP 4: SAVE RESULTS AS AN ARTIFACT
    # ----------------------------------------------------
    df_with_rolling.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote rolling monitoring file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
