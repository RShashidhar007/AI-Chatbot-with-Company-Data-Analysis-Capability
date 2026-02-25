"""
main.py

Command-line entry point for the AI Chatbot with Company Data Analysis Capability.
"""

from __future__ import annotations

from typing import Optional

from app.analytics_engine import (
    AnalysisResult,
    monthly_trend,
    sales_by_region,
    total_sales,
    top_n_products,
    year_comparison,
)
from app.data_loader import load_sales_data
from app.insight_generator import export_pdf, summarize
from app.nlp_processor import ParsedQuery, parse_user_message
from app.visualization import visualize_result


def handle_query(message: str, data, parsed: ParsedQuery) -> Optional[AnalysisResult]:
    """Route the query to the appropriate analytical function."""
    intent = parsed.intent
    years = parsed.years or None
    regions = parsed.regions or None

    if intent == "total_sales":
        return total_sales(data, years=years, regions=regions)
    if intent == "top_products":
        n = parsed.top_n or 5
        return top_n_products(data, n=n, years=years, regions=regions)
    if intent == "sales_by_region":
        return sales_by_region(data, years=years)
    if intent == "monthly_trend":
        year = years[0] if years else None
        region = regions[0] if regions else None
        return monthly_trend(data, year=year, region=region)
    if intent == "year_comparison":
        region = regions[0] if regions else None
        return year_comparison(data, years=years, region=region)

    return None


def run_cli() -> None:
    """Interactive console loop."""
    data = load_sales_data()
    print("=== AI Sales Chatbot ===")
    print("Ask a question about sales (type 'exit' to quit).")

    last_result: Optional[AnalysisResult] = None
    last_summary: Optional[str] = None
    last_chart_path: Optional[str] = None

    while True:
        message = input("\nYou: ").strip()
        if message.lower() in {"exit", "quit", "q"}:
            print("Bot: Goodbye!")
            break

        if message.lower() in {"help", "examples"}:
            print(
                "Bot: Example queries:\n"
                "  - Total sales in 2023\n"
                "  - Top 5 products in the North region\n"
                "  - Sales by region for 2022\n"
                "  - Monthly trend for 2024 in South\n"
                "  - Compare 2022 vs 2023\n"
                "  - export pdf (export last insight as PDF)\n"
            )
            continue

        if message.lower().startswith("export pdf"):
            if last_result and last_summary:
                pdf_path = export_pdf(last_summary, last_result, chart_path=last_chart_path)
                print(f"Bot: PDF report saved to {pdf_path}")
            else:
                print("Bot: There is no previous insight to export yet.")
            continue

        parsed = parse_user_message(message)
        if parsed.intent == "unknown":
            print(
                "Bot: I couldn't understand that. "
                "Try asking about total sales, top products, regional sales, "
                "monthly trends, or year comparisons."
            )
            continue

        result = handle_query(message, data, parsed)
        if result is None:
            print("Bot: I wasn't able to compute that request.")
            continue

        summary = summarize(result)
        chart_path = visualize_result(result)

        last_result = result
        last_summary = summary
        last_chart_path = chart_path

        print(f"Bot: {summary}")
        if chart_path:
            print(f"Bot: I also saved a chart to: {chart_path}")


if __name__ == "__main__":
    run_cli()

