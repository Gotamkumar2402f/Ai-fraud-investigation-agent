from langchain.tools import tool
import pandas as pd
from src.config import TRANSACTIONS_PATH

@tool
def find_similar_past_cases(amount: float, merchant_category: str, country: str) -> str:
    """Find similar past transactions (especially confirmed fraud) for pattern matching."""
    df = pd.read_csv(TRANSACTIONS_PATH)
    similar = df[
        (df["amount"].between(amount * 0.6, amount * 1.5)) &
        (df["merchant_category"] == merchant_category)
    ].head(8)

    fraud_count = int(similar["is_fraud"].sum())
    return str({
        "similar_cases_found": len(similar),
        "confirmed_fraud_in_similar": fraud_count,
        "sample": similar[["transaction_id", "amount", "country", "is_fraud"]].to_dict(orient="records")
    })