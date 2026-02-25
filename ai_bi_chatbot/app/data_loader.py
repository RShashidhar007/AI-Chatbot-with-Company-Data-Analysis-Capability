"""
data_loader.py

Responsible for loading or generating the synthetic sales dataset.
The dataset is kept small and clean so it is easy to inspect and reason
about during an internship or learning project.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_PATH = DATA_DIR / "sales_data.csv"


@dataclass
class DataConfig:
    """Configuration for synthetic data generation."""

    start_year: int = 2021
    end_year: int = 2024
    regions: tuple[str, ...] = ("North", "South", "East", "West")
    products: tuple[str, ...] = (
        "Laptop",
        "Desktop",
        "Tablet",
        "Printer",
        "Monitor",
    )
    categories: tuple[str, ...] = (
        "Computers",
        "Accessories",
    )
    n_rows: int = 800


def _generate_synthetic_data(config: Optional[DataConfig] = None) -> pd.DataFrame:
    """
    Generate a simple, realistic synthetic sales dataset.

    Columns:
        - order_date (datetime)
        - year (int)
        - month (int)
        - region (str)
        - product (str)
        - category (str)
        - quantity (int)
        - unit_price (float)
        - total_sales (float)
    """
    if config is None:
        config = DataConfig()

    rng = np.random.default_rng(seed=42)

    years = rng.integers(config.start_year, config.end_year + 1, size=config.n_rows)
    months = rng.integers(1, 13, size=config.n_rows)
    days = rng.integers(1, 28, size=config.n_rows)  # keep dates valid

    order_dates = pd.to_datetime(
        {
            "year": years,
            "month": months,
            "day": days,
        }
    )

    regions = rng.choice(config.regions, size=config.n_rows)
    products = rng.choice(config.products, size=config.n_rows)
    # Simple mapping from product to category
    product_to_category = {
        "Laptop": "Computers",
        "Desktop": "Computers",
        "Tablet": "Computers",
        "Printer": "Accessories",
        "Monitor": "Accessories",
    }
    categories = [product_to_category.get(p, "Other") for p in products]

    quantity = rng.integers(1, 20, size=config.n_rows)
    base_prices = {
        "Laptop": 800,
        "Desktop": 700,
        "Tablet": 300,
        "Printer": 200,
        "Monitor": 250,
    }
    unit_price = np.array([base_prices.get(p, 100) for p in products], dtype=float)
    # Add some random noise to prices
    unit_price *= rng.normal(loc=1.0, scale=0.1, size=config.n_rows)

    total_sales = quantity * unit_price

    df = pd.DataFrame(
        {
            "order_date": order_dates,
            "year": years,
            "month": months,
            "region": regions,
            "product": products,
            "category": categories,
            "quantity": quantity,
            "unit_price": unit_price.round(2),
            "total_sales": total_sales.round(2),
        }
    )

    return df


def load_sales_data(force_regenerate: bool = False) -> pd.DataFrame:
    """
    Load the sales data from disk, generating a synthetic dataset on first run.

    Args:
        force_regenerate: if True, ignores any existing CSV and regenerates data.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    if DATA_PATH.exists() and not force_regenerate:
        df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    else:
        df = _generate_synthetic_data()
        df.to_csv(DATA_PATH, index=False)

    return df


__all__ = ["load_sales_data", "DataConfig", "DATA_PATH"]

