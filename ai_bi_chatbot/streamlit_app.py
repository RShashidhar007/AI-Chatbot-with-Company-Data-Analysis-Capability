from __future__ import annotations

import textwrap

import streamlit as st


from modules.analytics_engine import (
    monthly_trend,
    sales_by_region,
    total_sales,
    top_n_products,
    year_comparison,
)
from modules.data_loader import load_sales_data
from modules.insight_generator import summarize
from modules.nlp_processor import parse_user_message
from modules.visualization import visualize_result


def main() -> None:
    st.set_page_config(
        page_title="AI Sales Chatbot",
        page_icon="📊",
        layout="wide",
    )

    st.title("AI Chatbot with Company Data Analysis")
    st.write(
        "Ask natural language questions about sales data. "
        "The assistant will analyse a synthetic dataset using Pandas, generate charts, "
        "and summarise insights in business language."
    )

    data = load_sales_data()

    with st.sidebar:
        st.header("About")
        st.markdown(
            textwrap.dedent(
                """
                **Example questions**

                - Total sales in 2023  
                - Top 5 products in the North region  
                - Sales by region for 2022  
                - Monthly trend for 2024 in South  
                - Compare 2022 vs 2023
                """
            )
        )
        st.caption("Note: Dataset is synthetic and generated locally.")

    user_query = st.text_input("Your question", placeholder="e.g. What were total sales in 2023?")
    if st.button("Analyse", type="primary"):
        if not user_query.strip():
            st.warning("Please enter a question.")
            return

        parsed = parse_user_message(user_query)
        if parsed.intent == "unknown":
            st.error(
                "I couldn't understand that. Please ask about total sales, top products, "
                "regional sales, monthly trends, or year comparisons."
            )
            return

        if parsed.intent == "total_sales":
            result = total_sales(data, years=parsed.years or None, regions=parsed.regions or None)
        elif parsed.intent == "top_products":
            n = parsed.top_n or 5
            result = top_n_products(data, n=n, years=parsed.years or None, regions=parsed.regions or None)
        elif parsed.intent == "sales_by_region":
            result = sales_by_region(data, years=parsed.years or None)
        elif parsed.intent == "monthly_trend":
            year = parsed.years[0] if parsed.years else None
            region = parsed.regions[0] if parsed.regions else None
            result = monthly_trend(data, year=year, region=region)
        elif parsed.intent == "year_comparison":
            region = parsed.regions[0] if parsed.regions else None
            result = year_comparison(data, years=parsed.years or None, region=region)
        else:
            st.error("Unsupported intent.")
            return

        summary = summarize(result)
        st.subheader("Insight")
        st.write(summary)

        st.subheader("Details")
        st.dataframe(result.table)

        chart_path = visualize_result(result)
        if chart_path:
            st.subheader("Chart")
            st.image(chart_path, use_container_width=True)


if __name__ == "__main__":
    main()
