"""
visualization.py

Creates Matplotlib charts for different analysis types and saves
them under the `output/` directory.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import matplotlib

# Use a non-interactive backend suitable for servers / scripts
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from .analytics_engine import AnalysisResult


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def _save_fig(fig: plt.Figure, filename: str) -> str:
    path = OUTPUT_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return str(path)


def plot_bar_from_table(result: AnalysisResult, x_col: str, y_col: str, title: Optional[str] = None) -> str:
    df = result.table
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df[x_col], df[y_col], color="#2563eb")
    ax.set_xlabel(x_col.replace("_", " ").title())
    ax.set_ylabel("Sales")
    ax.set_title(title or result.description)
    ax.set_xticklabels(df[x_col], rotation=30, ha="right")
    filename = f"{result.intent}_bar.png"
    return _save_fig(fig, filename)


def plot_line_from_table(result: AnalysisResult, x_col: str, y_col: str, title: Optional[str] = None) -> str:
    df = result.table
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df[x_col], df[y_col], marker="o", color="#10b981")
    ax.set_xlabel(x_col.replace("_", " ").title())
    ax.set_ylabel("Sales")
    ax.set_title(title or result.description)
    ax.grid(True, linestyle="--", alpha=0.4)
    filename = f"{result.intent}_line.png"
    return _save_fig(fig, filename)


def visualize_result(result: AnalysisResult) -> Optional[str]:
    """
    High-level helper that chooses a suitable chart for the intent.

    Returns:
        Path to the saved image (or None if no chart is applicable).
    """
    if result.intent == "top_products":
        return plot_bar_from_table(result, x_col="product", y_col="total_sales")
    if result.intent == "sales_by_region":
        return plot_bar_from_table(result, x_col="region", y_col="total_sales")
    if result.intent == "monthly_trend":
        return plot_line_from_table(result, x_col="month", y_col="total_sales")
    if result.intent == "year_comparison":
        return plot_line_from_table(result, x_col="year", y_col="total_sales")
    # For total sales, a chart is not very helpful
    return None


__all__ = ["visualize_result", "OUTPUT_DIR"]

