"""
insight_generator.py

Transforms raw numerical results into short, business-style
insight summaries.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .analytics_engine import AnalysisResult


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def summarize(result: AnalysisResult) -> str:
    """
    Turn an AnalysisResult into a human-readable business insight.
    """
    df = result.table

    if result.intent == "total_sales":
        total = float(df["total_sales"].iloc[0])
        return f"Total sales amount to {format_currency(total)}. {result.description}."

    if result.intent == "top_products":
        lines = []
        for _, row in df.iterrows():
            lines.append(f"{row['product']} ({format_currency(float(row['total_sales']))})")
        joined = "; ".join(lines)
        return f"{result.description}: {joined}."

    if result.intent == "sales_by_region":
        best_region = df.iloc[0]
        worst_region = df.iloc[-1]
        return (
            f"{result.description}. Best performing region is {best_region['region']} "
            f"with {format_currency(float(best_region['total_sales']))}, while the lowest "
            f"is {worst_region['region']} at {format_currency(float(worst_region['total_sales']))}."
        )

    if result.intent == "monthly_trend":
        first = df.iloc[0]
        last = df.iloc[-1]
        direction = "increased" if last["total_sales"] >= first["total_sales"] else "decreased"
        return (
            f"{result.description}. Sales {direction} from "
            f"{format_currency(float(first['total_sales']))} in month {int(first['month'])} "
            f"to {format_currency(float(last['total_sales']))} in month {int(last['month'])}."
        )

    if result.intent == "year_comparison":
        best = df.loc[df["total_sales"].idxmax()]
        worst = df.loc[df["total_sales"].idxmin()]
        return (
            f"{result.description}. Highest sales were in {int(best['year'])} "
            f"at {format_currency(float(best['total_sales']))}, compared with "
            f"{format_currency(float(worst['total_sales']))} in {int(worst['year'])}."
        )

    return "No clear insight available for this query."


def export_pdf(summary: str, result: AnalysisResult, chart_path: Optional[str] = None) -> str:
    """
    Create a simple PDF report with the summary and optional chart path.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    pdf_path = OUTPUT_DIR / "latest_report.pdf"

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4
    margin = 40

    y = height - margin
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Sales Insight Report")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(margin, y, f"Description: {result.description}")
    y -= 20

    text_obj = c.beginText(margin, y)
    text_obj.setFont("Helvetica", 10)
    for line in summary.split(". "):
        text_obj.textLine(line.strip())
    c.drawText(text_obj)

    if chart_path:
        # Just mention the chart path; embedding the image is possible but optional
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(margin, margin, f"Chart image: {chart_path}")

    c.showPage()
    c.save()

    return str(pdf_path)


__all__ = ["summarize", "export_pdf"]

