# 🛡️ AI Fraud Investigation Agent

An autonomous multi-tool AI agent that investigates suspicious financial transactions, gathers evidence from multiple sources, calculates interpretable risk scores, and generates structured investigation reports with PDF export.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-Agent-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **Multi-tool AI Agent** – Transaction lookup, customer velocity, IP risk, merchant risk, similar past cases
- **Risk Scoring** – Interpretable score (0-100) with visual gauge
- **PDF + Text Report Download** – Professional investigation reports
- **Investigation History** – Save and revisit past cases
- **Dark Professional UI** – Clean and modern interface
- **Works with Groq (free) / OpenAI**

## 🏗️ Architecture
User → Streamlit UI → Investigator Agent → Tools (CSV + Risk Checks) → Structured Report + PDF
text


## 🚀 Quick Start

```bash
git clone https://github.com/Gotamkumar2402f/Ai-fraud-investigation-agent.git
cd Ai-fraud-investigation-agent
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python data/generate_data.

Create a .env file:
GROQ_API_KEY=your_groq_api_key
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-20b

Run the app:
Bash:streamlit run app.py

Tech Stack:
Python
LangChain + LangChain-Classic (Tool-calling Agent)
Streamlit (UI)
Plotly (Risk Gauge)
FPDF2 (PDF Reports)
Groq / OpenAI
Pandas

📂 Project Structure
Ai-fraud-investigation-agent/
├── app.py
├── data/
│   ├── generate_data.py
│   ├── transactions.csv
│   └── customers.csv
├── src/
│   ├── agent/
│   │   └── investigator.py
│   ├── tools/
│   │   ├── transaction_tools.py
│   │   ├── customer_tools.py
│   │   ├── risk_tools.py
│   │   └── knowledge_tools.py
│   └── utils/
│       ├── report.py
│       ├── history.py
│       └── pdf_report.py
├── requirements.txt
└── README.md


