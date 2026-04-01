"""
visualize_air_quality.py - Visualization of rolling air quality metrics.

Author: Branton Dawson
Date: 2026-04

Purpose

- Read the air quality rolling metrics artifact CSV.
- Create a dual-axis line chart showing:
  - 30-day rolling CO concentration (ppm) on left Y-axis
  - 30-day rolling AQI mean on right Y-axis
- Save the visualization as an HTML file and a PNG.

Paths (relative to repo root)

    INPUT FILE: artifacts/air_quality_rolling_metrics.csv
    OUTPUT FILES:
      - artifacts/air_quality_rolling_chart.png (static image)

Terminal command to run this file from the root project folder

    uv run python -m cintel.visualize_air_quality
"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import pandas as pd
import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path
from matplotlib.dates import DateFormatter, MonthLocator

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P5", level="DEBUG")

# === DEFINE GLOBAL PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

INPUT_FILE: Final[Path] = ARTIFACTS_DIR / "air_quality_rolling_metrics.csv"
OUTPUT_PNG: Final[Path] = ARTIFACTS_DIR / "air_quality_rolling_chart.png"
OUTPUT_HTML: Final[Path] = ARTIFACTS_DIR / "air_quality_rolling_chart.html"

# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Generate dual-axis visualization of rolling air quality metrics."""
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "INPUT_FILE", INPUT_FILE)
    log_path(LOG, "OUTPUT_PNG", OUTPUT_PNG)
    log_path(LOG, "OUTPUT_HTML", OUTPUT_HTML)

    # Ensure artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ============================================================
    # STEP 1: READ THE ARTIFACT CSV
    # ============================================================
    df = pl.read_csv(INPUT_FILE)

    LOG.info(f"Loaded {df.height} records from artifact")

    # ============================================================
    # STEP 2: EXTRACT COLUMNS AND FILTER OUT NULLS
    # ============================================================
    # We need to drop rows where either rolling metric is null
    # (they occur at the start of the dataset before the window fills).
    df_clean = df.select(["Date", "co_rolling_30d_mean", "aqi_rolling_30d_mean"])
    df_clean = df_clean.drop_nulls()

    # Extract as lists and convert dates to datetime
    date_list = df_clean.select(["Date"]).to_series().to_list()
    dates = pd.to_datetime(date_list)
    co_values = df_clean.select(["co_rolling_30d_mean"]).to_series().to_list()
    aqi_values = df_clean.select(["aqi_rolling_30d_mean"]).to_series().to_list()

    LOG.info(
        f"Plotting {len(dates)} clean data points from {dates.min()} to {dates.max()}"
    )

    # ============================================================
    # STEP 3: CREATE DUAL-AXIS LINE CHART
    # ============================================================
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot CO on left Y-axis
    color_co = "#1f77b4"  # blue
    ax1.set_xlabel("Date", fontsize=12, fontweight="bold")
    ax1.set_ylabel(
        "30-Day Rolling CO Mean (ppm)", color=color_co, fontsize=12, fontweight="bold"
    )
    line1 = ax1.plot(
        dates, co_values, color=color_co, linewidth=2.5, label="CO Conc. (30d mean)"
    )
    ax1.tick_params(axis="y", labelcolor=color_co)
    ax1.grid(True, alpha=0.3)

    # Plot AQI on right Y-axis
    ax2 = ax1.twinx()
    color_aqi = "#ff7f0e"  # orange
    ax2.set_ylabel(
        "30-Day Rolling AQI Mean", color=color_aqi, fontsize=12, fontweight="bold"
    )
    line2 = ax2.plot(
        dates, aqi_values, color=color_aqi, linewidth=2.5, label="AQI (30d mean)"
    )
    ax2.tick_params(axis="y", labelcolor=color_aqi)

    # Configure title and legend
    plt.title(
        "Kansas City Air Quality: 30-Day Rolling Metrics",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )

    # Combine legends from both axes
    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc="upper left", fontsize=11, framealpha=0.95)

    # Format X-axis to show every month
    ax1.xaxis.set_major_locator(MonthLocator(interval=1))
    ax1.xaxis.set_major_formatter(DateFormatter("%b %Y"))
    plt.xticks(rotation=45, ha="right")

    # Tight layout to prevent label cutoff
    plt.tight_layout()

    # ============================================================
    # STEP 4: SAVE AS PNG
    # ============================================================
    plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
    LOG.info(f"Saved PNG visualization: {OUTPUT_PNG}")

    # ============================================================
    # STEP 5: SAVE AS INTERACTIVE HTML (PLOTLY)
    # ============================================================
    try:
        import plotly.graph_objects as go

        fig_plotly = go.Figure()

        # Add CO trace
        fig_plotly.add_trace(
            go.Scatter(
                x=dates,
                y=co_values,
                name="CO Conc. - 30d Mean (ppm)",
                line=dict(color="#1f77b4", width=2.5),
                yaxis="y1",
            )
        )

        # Add AQI trace
        fig_plotly.add_trace(
            go.Scatter(
                x=dates,
                y=aqi_values,
                name="AQI - 30d Mean",
                line=dict(color="#ff7f0e", width=2.5),
                yaxis="y2",
            )
        )

        # Configure layout with dual Y-axes
        fig_plotly.update_layout(
            title="Kansas City Air Quality: 30-Day Rolling Metrics (Interactive)",
            xaxis=dict(title="Date"),
            yaxis=dict(
                title="30-Day Rolling CO Mean (ppm)",
                titlefont=dict(color="#1f77b4"),
                tickfont=dict(color="#1f77b4"),
            ),
            yaxis2=dict(
                title="30-Day Rolling AQI Mean",
                titlefont=dict(color="#ff7f0e"),
                tickfont=dict(color="#ff7f0e"),
                anchor="free",
                overlaying="y",
                side="right",
                position=0.99,
            ),
            hovermode="x unified",
            plot_bgcolor="rgba(240,240,240,0.5)",
            height=700,
            width=1400,
        )

        fig_plotly.write_html(OUTPUT_HTML)
        LOG.info(f"Saved interactive HTML visualization: {OUTPUT_HTML}")

    except ImportError:
        LOG.warning("Plotly not installed; skipping interactive HTML output.")

    LOG.info("========================")
    LOG.info("Visualization complete!")
    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
