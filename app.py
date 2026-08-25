import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

from src.agent.investigator import investigate
from src.config import TRANSACTIONS_PATH
from src.utils.report import format_report, extract_risk_level, extract_risk_score
from src.utils.history import save_investigation, get_history, get_investigation_by_id
from src.utils.pdf_report import create_pdf_report

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="AI Fraud Investigation Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    h1, h2, h3 { color: #38bdf8 !important; }
    .stButton > button {
        background: linear-gradient(90deg, #0ea5e9, #0284c7);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #0284c7, #0369a1);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
    .risk-critical { color: #ef4444; font-weight: bold; }
    .risk-high { color: #f97316; font-weight: bold; }
    .risk-medium { color: #eab308; font-weight: bold; }
    .risk-low { color: #22c55e; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ====================== HELPER: RISK GAUGE ======================
def create_risk_gauge(score: int):
    if score >= 75:
        color = "#ef4444"
    elif score >= 55:
        color = "#f97316"
    elif score >= 35:
        color = "#eab308"
    else:
        color = "#22c55e"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Score", 'font': {'size': 18, 'color': '#e2e8f0'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#94a3b8'},
            'bar': {'color': color},
            'bgcolor': "#1e293b",
            'borderwidth': 2,
            'bordercolor': "#334155",
            'steps': [
                {'range': [0, 35], 'color': '#14532d'},
                {'range': [35, 55], 'color': '#713f12'},
                {'range': [55, 75], 'color': '#7c2d12'},
                {'range': [75, 100], 'color': '#7f1d1d'}
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#e2e8f0"},
        height=250,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# ====================== HEADER ======================
st.title("🛡️ AI Fraud Investigation Agent")
st.markdown("### Autonomous multi-tool AI agent for financial fraud investigation")
st.markdown("---")

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    
    try:
        df = pd.read_csv(TRANSACTIONS_PATH)
        fraud_txns = df[df["is_fraud"] == True]["transaction_id"].tolist()
    except:
        fraud_txns = []
        df = pd.DataFrame()

    sample_choice = st.selectbox(
        "Quick pick (Fraud Samples)",
        ["-- select --"] + fraud_txns[:20]
    )
    
    manual_id = st.text_input("Or enter Transaction ID", placeholder="e.g. TXN000123")
    
    run_btn = st.button("🚀 Start Investigation", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("**Model:** `openai/gpt-oss-20b`")
    st.markdown("**Provider:** Groq")
    
    # History Section
    st.markdown("---")
    st.markdown("### 📜 Investigation History")
    history = get_history()
    
    if history:
        for item in history[:8]:
            risk = item.get("risk_level", "UNKNOWN")
            label = f"{item['transaction_id']} | {risk}"
            if st.button(label, key=f"hist_{item['id']}", use_container_width=True):
                st.session_state["selected_history"] = item["id"]
    else:
        st.caption("No investigations yet")

# ====================== MAIN AREA ======================
tx_id = sample_choice if sample_choice != "-- select --" else manual_id.strip()

# Show selected history
if "selected_history" in st.session_state:
    inv = get_investigation_by_id(st.session_state["selected_history"])
    if inv:
        st.info(f"📂 Viewing past investigation: **{inv['transaction_id']}**")
        st.markdown(inv["report"])
        
        # PDF Download for history
        try:
            pdf_bytes = create_pdf_report(inv["transaction_id"], inv["report"])
            st.download_button(
                "⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=f"Fraud_Report_{inv['transaction_id']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"PDF generation failed: {e}")

# New Investigation
if run_btn and tx_id:
    with st.spinner(f"🔍 Investigating **{tx_id}** ... Agent is gathering evidence..."):
        try:
            result = investigate(tx_id)
            report = format_report(result)
            
            risk_level = extract_risk_level(result)
            risk_score = extract_risk_score(result)
            
            # Save to history
            save_investigation(tx_id, report, risk_level)
            
            st.success("✅ Investigation Complete")
            
            # Risk Gauge + Level
            col1, col2 = st.columns([1, 2])
            with col1:
                st.plotly_chart(create_risk_gauge(risk_score), use_container_width=True)
            with col2:
                st.markdown(f"### Risk Level: **{risk_level}**")
                st.markdown(f"**Score:** {risk_score}/100")
                st.markdown(f"**Transaction:** `{tx_id}`")
            
            st.markdown("---")
            st.markdown("### 📄 Investigation Report")
            st.markdown(report)
            
            # Download Buttons
            col_a, col_b = st.columns(2)
            
            with col_a:
                # Text download
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    "📄 Download Text Report",
                    data=report,
                    file_name=f"Fraud_Report_{tx_id}_{timestamp}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_b:
                # PDF download
                try:
                    pdf_bytes = create_pdf_report(tx_id, report)
                    st.download_button(
                        "⬇️ Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"Fraud_Report_{tx_id}_{timestamp}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.warning(f"PDF error: {e}")
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("Check your API key in `.env` and make sure data files exist.")

elif run_btn:
    st.warning("⚠️ Please select or enter a Transaction ID")

# Sample data
with st.expander("📊 Sample Transactions (for testing)"):
    if not df.empty:
        st.dataframe(
            df.sample(min(10, len(df)))[["transaction_id", "customer_id", "amount", "merchant", "country", "is_fraud"]],
            use_container_width=True
        )
    else:
        st.write("No data found. Run `python data/generate_data.py` first.")