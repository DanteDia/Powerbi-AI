#!/usr/bin/env python3
"""
Power BI Migration Analysis Pipeline

Analyzes .pbix files and generates a complete migration plan from
Excel-based Power BI to SQL-backed Power BI.

Usage:
    python run_analysis.py                    # Run full pipeline
    python run_analysis.py --step extract     # Run a single step
    python run_analysis.py --input ./my_pbix  # Custom input directory
    python run_analysis.py --help             # Show all options
"""

import os
import sys
import time

import click

from scripts.extract_pbix import extract_all
from scripts.analyze_model import analyze_model
from scripts.analyze_dax import analyze_dax
from scripts.analyze_reports import analyze_reports
from scripts.generate_sql_model import generate_sql_model

STEPS = ["extract", "model", "dax", "reports", "sql"]


def _banner():
    print("=" * 60)
    print("  Power BI Migration Analysis Pipeline")
    print("=" * 60)
    print()


def _run_step(step_name, func, *args):
    print(f"[{step_name.upper()}] Starting...")
    start = time.time()
    try:
        result = func(*args)
        elapsed = time.time() - start
        print(f"[{step_name.upper()}] Done ({elapsed:.1f}s)")
        return result
    except Exception as e:
        elapsed = time.time() - start
        print(f"[{step_name.upper()}] FAILED ({elapsed:.1f}s): {e}")
        return None


@click.command()
@click.option(
    "--input", "input_dir",
    default="input",
    help="Directory containing .pbix files",
    type=click.Path(),
)
@click.option(
    "--output", "output_dir",
    default="output",
    help="Base output directory",
    type=click.Path(),
)
@click.option(
    "--step",
    type=click.Choice(STEPS + ["all"], case_sensitive=False),
    default="all",
    help="Run a specific step or 'all'",
)
def main(input_dir, output_dir, step):
    """Analyze Power BI .pbix files and generate SQL migration artifacts."""
    _banner()

    extracted_dir = os.path.join(output_dir, "extracted")
    model_dir = os.path.join(output_dir, "model")
    measures_dir = os.path.join(output_dir, "measures")
    reports_dir = os.path.join(output_dir, "reports")
    sql_dir = os.path.join(output_dir, "sql")

    steps_to_run = STEPS if step == "all" else [step]
    total_start = time.time()

    for s in steps_to_run:
        print()
        if s == "extract":
            _run_step("extract", extract_all, input_dir, extracted_dir)

        elif s == "model":
            _run_step("model", analyze_model, extracted_dir, model_dir)

        elif s == "dax":
            _run_step("dax", analyze_dax, extracted_dir, measures_dir)

        elif s == "reports":
            _run_step("reports", analyze_reports, extracted_dir, reports_dir)

        elif s == "sql":
            _run_step("sql", generate_sql_model, model_dir, measures_dir, sql_dir)

    total_elapsed = time.time() - total_start
    print()
    print("=" * 60)
    print(f"  Pipeline complete ({total_elapsed:.1f}s)")
    print(f"  Results in: {os.path.abspath(output_dir)}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
