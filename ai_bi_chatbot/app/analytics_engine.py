"""
analytics_engine.py

Implements core analytical queries over the sales dataset:
- total sales
- top N products
- sales by region
- monthly trend
- year-on-year comparison
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import pandas as pd


@dataclass
class AnalysisResult:
    """Tabular result plus useful metadata for downstream components."""

    intent: str
    table: pd.DataFrame
    years: List[int]
    regions: List[str]
    description: str


def _filter_data(
    df: pd.DataFrame, years: Optional[List[int]] = None, regions: Optional[List[str]] = None
) -> pd.DataFrame:
    """Apply optional year and region filters."""
    filtered = df.copy()
    if years:
        filtered = filtered[filtered["year"].isin(years)]
    if regions:
        filtered = filtered[filtered["region"].isin(regions)]
    return filtered


def total_sales(df: pd.DataFrame, years=None, regions=None) -> AnalysisResult:
    data = _filter_data(df, years, regions)
    total = data["total_sales"].sum()
    table = pd.DataFrame({"total_sales": [round(float(total), 2)]})
    desc = "Total sales"
    if years:
        desc += f" for years {', '.join(map(str, years))}"
    if regions:
        desc += f" in regions {', '.join(regions)}"
    return AnalysisResult(intent="total_sales", table=table, years=years or [], regions=regions or [], description=desc)


def top_n_products(df: pd.DataFrame, n: int = 5, years=None, regions=None) -> AnalysisResult:
    data = _filter_data(df, years, regions)
    grouped = (
        data.groupby("product")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
    desc = f"Top {n} products by sales"
    if years:
        desc += f" in years {', '.join(map(str, years))}"
    if regions:
        desc += f" for regions {', '.join(regions)}"
    return AnalysisResult(intent="top_products", table=grouped, years=years or [], regions=regions or [], description=desc)


def sales_by_region(df: pd.DataFrame, years=None) -> AnalysisResult:
    data = _filter_data(df, years, None)
    grouped = (
        data.groupby("region")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    desc = "Sales by region"
    if years:
        desc += f" for years {', '.join(map(str, years))}"
    return AnalysisResult(intent="sales_by_region", table=grouped, years=years or [], regions=list(grouped["region"]), description=desc)


def monthly_trend(df: pd.DataFrame, year: Optional[int] = None, region: Optional[str] = None) -> AnalysisResult:
    data = df.copy()
    years = []
    regions = []
    if year is not None:
        data = data[data["year"] == year]
        years = [year]
    if region is not None:
        data = data[data["region"] == region]
        regions = [region]

    grouped = (
        data.groupby("month")["total_sales"]
        .sum()
        .sort_index()
        .reset_index()
    )
    desc = "Monthly sales trend"
    if year is not None:
        desc += f" for {year}"
    if region is not None:
        desc += f" in {region}"
    return AnalysisResult(intent="monthly_trend", table=grouped, years=years, regions=regions, description=desc)


def year_comparison(df: pd.DataFrame, years=None, region: Optional[str] = None) -> AnalysisResult:
    if not years or len(years) < 2:
        # If user did not specify enough years, compare all available
        years = sorted(df["year"].unique().tolist())
    data = _filter_data(df, years, [region] if region else None)
    grouped = (
        data.groupby("year")["total_sales"]
        .sum()
        .reset_index()
        .sort_values("year")
    )
    regions = [region] if region else []
    desc = "Year-on-year sales comparison"
    if region:
        desc += f" for region {region}"
    return AnalysisResult(intent="year_comparison", table=grouped, years=years, regions=regions, description=desc)


__all__ = [
    "AnalysisResult",
    "total_sales",
    "top_n_products",
    "sales_by_region",
    "monthly_trend",
    "year_comparison",
]

