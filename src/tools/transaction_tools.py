import pandas as pd
from langchain.tools import tool
from src.config import TRANSACTIONS_PATH

_df = None

def _load():
    global _df
    if _df is None:
        _df = pd.read_csv(TRANSACTIONS_PATH)
        _df["timestamp"] = pd.to_datetime(_df["timestamp"])
    return _df

@tool
def get_transaction(transaction_id: str) -> str:
    """Fetch full details of a single transaction by its ID (e.g. TXN000123)."""
    df = _load()
    row = df[df["transaction_id"] == transaction_id]
    if row.empty:
        return f"Transaction {transaction_id} not found."
    return str(row.iloc[0].to_dict())

@tool
def get_customer_transactions(customer_id: str, limit: int = 20) -> str:
    """Get recent transactions for a customer. Useful for velocity and pattern analysis."""
    df = _load()
    subset = df[df["customer_id"] == customer_id].sort_values("timestamp", ascending=False).head(limit)
    if subset.empty:
        return f"No transactions found for {customer_id}."
    return str(subset.to_dict(orient="records"))

@tool
def search_transactions_by_merchant(merchant: str, limit: int = 15) -> str:
    """Search transactions involving a specific merchant name."""
    df = _load()
    subset = df[df["merchant"].str.contains(merchant, case=False, na=False)].head(limit)
    if subset.empty:
        return f"No transactions found for merchant containing '{merchant}'."
    return str(subset[["transaction_id", "customer_id", "amount", "timestamp", "country", "is_fraud"]].to_dict(orient="records"))