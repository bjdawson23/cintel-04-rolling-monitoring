# cintel-04-rolling-monitoring

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](#)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Professional Python project for continuous intelligence.

Continuous intelligence systems monitor data streams, detect change, and respond in real time.
This course builds those capabilities through working projects.

In the age of generative AI, durable skills are grounded in real work:
setting up a professional environment,
reading and running code,
understanding the logic,
and pushing work to a shared repository.
Each project follows the structure of professional Python projects.
We learn by doing.

## This Project

This project introduces **rolling monitoring**.

The goal is to copy this repository,
set up your environment,
run the example analysis,
and explore how system metrics change over time.

You will run the example pipeline, read the code,
and make small modifications to understand
how rolling windows help smooth short-term variation and
reveal trends in time-series data.

Phase 5 Custom Project:

1. **System Metrics (Dawson):** Added ROLLING ERROR RATE (PERCENTAGE)
   - rolling_error_rate_pct = (rolling_errors / rolling_requests) * 100
   - Expresses the percentage of requests that resulted in an error over the rolling window
   - 0% = no errors; 100% = all requests failed
   - Displayed in logs with 2 decimal place precision

2. **Air Quality (Kansas City 2023):** Added rolling metrics pipeline and visualization
   - **Dataset:** `data/kc_air_co_data_2023.csv` (148 daily observations)
   - **Rolling Metrics:** 30-day rolling CO mean and 30-day rolling AQI mean
   - **Pipeline:** `src/cintel/rolling_monitor_dawson_air_quality.py`
   - **Visualization:** `src/cintel/visualize_air_quality.py`  ![VISUAL](artifacts/air_quality_rolling_chart.png)
   - Key insight: CO and AQI trends track closely; Feb-Mar 2023 showed peak degradation

## Air Quality Analysis - Quick Start

Run the air quality rolling metrics pipeline and visualization:

```bash
# Generate 30-day rolling metrics (CO and AQI)
uv run python -m cintel.rolling_monitor_dawson_air_quality

# Create visualization charts
uv run python -m cintel.visualize_air_quality
```

Outputs:

- **Metrics CSV:** `artifacts/air_quality_rolling_metrics.csv` (with `co_rolling_30d_mean` and `aqi_rolling_30d_mean`)
- **Static Chart:** `artifacts/air_quality_rolling_chart.png`

---

The example pipeline reads time-series system metrics from:

`data/system_metrics_timeseries_case.csv`

Each row represents one observation at a specific timestamp.
The pipeline computes rolling averages for requests, errors, and latency, then saves the monitoring results as an artifact.

## Working Files

You'll work with just these areas:

- **data/** - it starts with the data
- **docs/** - tell the story
- **src/cintel/** - where the magic happens
- **pyproject.toml** - update authorship & links
- **zensical.toml** - update authorship & links

## Instructions

Follow the [step-by-step workflow guide](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/) to complete:

1. Phase 1. **Start & Run**
2. Phase 2. **Change Authorship**
3. Phase 3. **Read & Understand**
4. Phase 4. **Modify**
5. Phase 5. **Apply**

## Challenges

Challenges are expected.
Sometimes instructions may not quite match your operating system.
When issues occur, share screenshots, error messages, and details about what you tried.
Working through issues is part of implementing professional projects.

## Success

After completing Phase 1. **Start & Run**, you'll have your own GitHub project, running on your machine, and running the example will print out:

```shell
========================
Pipeline executed successfully!
========================
```

And a new file named `project.log` will appear in the project folder.

## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

Follow the guide for the **full instructions**.

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
# Replace username with YOUR GitHub username.
git clone https://github.com/bjdawson23/cintel-04-rolling-monitoring

cd cintel-04-rolling-monitoring
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
git add -A
uvx pre-commit run --all-files

uv run python -m cintel.rolling_monitor_case
uv run python -m cintel.rolling_monitor_dawson

uv run ruff format .
uv run ruff check . --fix
uv run zensical build

git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.
