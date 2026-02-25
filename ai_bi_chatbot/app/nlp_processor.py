"""
nlp_processor.py

Very lightweight natural language processing utilities for:
- intent classification (keyword-based)
- entity extraction (years, regions, top-N)

This keeps everything offline and easy to understand while still
feeling like a conversational BI assistant.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional


REGIONS = ["north", "south", "east", "west"]


@dataclass
class ParsedQuery:
    """Container for extracted intent and entities."""

    intent: str
    years: List[int]
    regions: List[str]
    top_n: Optional[int] = None


def detect_intent(message: str) -> str:
    """
    Infer the user's intent using simple keyword rules.

    Returns one of:
        - 'total_sales'
        - 'top_products'
        - 'sales_by_region'
        - 'monthly_trend'
        - 'year_comparison'
        - 'unknown'
    """
    text = message.lower()

    if any(word in text for word in ["compare", "vs", "versus"]) and re.search(
        r"\b20\d{2}\b", text
    ):
        return "year_comparison"

    if "trend" in text or "over time" in text or "monthly" in text:
        return "monthly_trend"

    if "region" in text or any(r in text for r in REGIONS):
        # Region-focused question
        return "sales_by_region"

    if "top" in text or "best" in text or "highest" in text:
        return "top_products"

    if "total" in text or "overall" in text or "revenue" in text:
        return "total_sales"

    return "unknown"


def extract_years(message: str) -> List[int]:
    """Extract 4-digit years like 2021, 2022 from the text."""
    years = re.findall(r"\b(20\d{2})\b", message)
    return sorted({int(y) for y in years})


def extract_regions(message: str) -> List[str]:
    """Extract region names using simple keyword matching."""
    text = message.lower()
    found = []
    for region in REGIONS:
        if region in text:
            found.append(region.capitalize())
    # De-duplicate while preserving order
    seen = set()
    unique = []
    for r in found:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    return unique


def extract_top_n(message: str) -> Optional[int]:
    """Try to detect 'top N' from phrases like 'top 5 products'."""
    match = re.search(r"top\s+(\d+)", message.lower())
    if match:
        try:
            return max(1, int(match.group(1)))
        except ValueError:
            return None
    return None


def parse_user_message(message: str) -> ParsedQuery:
    """
    High-level helper: get intent + entities in one call.
    """
    intent = detect_intent(message)
    years = extract_years(message)
    regions = extract_regions(message)
    top_n = extract_top_n(message)
    return ParsedQuery(intent=intent, years=years, regions=regions, top_n=top_n)


__all__ = ["ParsedQuery", "parse_user_message", "detect_intent"]

