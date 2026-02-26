# AI Chatbot with Company Data Analysis Capability

This project is an offline, internship-level Business Intelligence (BI) assistant.  
It accepts natural language questions about sales data, analyses a synthetic dataset with Pandas, generates Matplotlib charts, and returns human-readable business insights.

Two interfaces are provided:

- Command-line chatbot (`python -m app.main`)
- Streamlit web app (`streamlit run app/streamlit_app.py`)
ai_bi_chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── data_loader.py
│   ├── nlp_processor.py
│   ├── analytics_engine.py
│   ├── visualization.py
│   ├── insight_generator.py
│   └── streamlit_app.py
├── data/              # Auto-created synthetic sales dataset
├── output/            # Generated charts and PDF reports
├── requirements.txt
└── README.md
```

## Installation

```bash
cd ai_bi_chatbot
python -m venv .venv
source .venv/Scripts/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## Running the command-line chatbot

```bash
cd ai_bi_chatbot
python -m app.main
```

Then type questions like:

- \"What were the total sales in 2023?\"
- \"Show top 5 products in the South region.\"
- \"Monthly trend for 2022\"
- \"Compare sales between 2022 and 2023\"

To exit, type `exit`, `quit`, or `q`.

## Running the Streamlit web app

```bash
cd ai_bi_chatbot
streamlit run app/streamlit_app.py
```

This opens a browser UI where you can type questions, see charts, and read auto-generated insights.


