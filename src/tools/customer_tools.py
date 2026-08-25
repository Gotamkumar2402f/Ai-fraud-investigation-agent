import pandas as pd
from langchain.tools import tool
from src.config import CUSTOMERS_PATH, TRANSACTIONS_PATH

_cust = None
_tx = None

def _load_cust():
    global _cust
    if _cust is None:
        _cust = pd.read_csv(CUSTOMERS_PATH)
    return _cust

def _load_tx():
    global _tx
    if _tx is None:
        _tx = pd.read_csv(TRANSACTIONS_PATH)
        _tx["timestamp"] = pd.to_datetime(_tx["timestamp"])
    return _tx

@tool
def get_customer_profile(customer_id: str) -> str:
    """Get customer profile: age, country, account age, average spend, risk tier, watchlist status."""
    df = _load_cust()
    row = df[df["customer_id"] == customer_id]
    if row.empty:
        return f"Customer {customer_id} not found."
    return str(row.iloc[0].to_dict())

@tool
def get_customer_velocity(customer_id: str, hours: int = 24) -> str:
    """Calculate transaction velocity (count + total amount) in the last N hours for a customer."""
    tx = _load_tx()
    subset = tx[tx["customer_id"] == customer_id].copy()
    if subset.empty:
        return "No transactions."
    latest = subset["timestamp"].max()
    window = subset[subset["timestamp"] >= (latest - pd.Timedelta(hours=hours))]
    return str({
        "count": len(window),
        "total_amount": round(window["amount"].sum(), 2),
        "window_hours": hours,
        "latest_tx": str(latest)
    })