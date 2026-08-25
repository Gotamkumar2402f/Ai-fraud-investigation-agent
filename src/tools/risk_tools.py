from langchain.tools import tool

@tool
def check_ip_risk(ip_address: str) -> str:
    """Check risk level of an IP address (proxy/VPN/tor, geo mismatch, known bad IPs)."""
    try:
        last_octet = int(ip_address.split(".")[-1])
    except:
        last_octet = 50

    if last_octet > 200:
        risk = "HIGH"
        reasons = ["Known VPN/Proxy range", "High abuse score"]
    elif last_octet > 150:
        risk = "MEDIUM"
        reasons = ["Datacenter IP", "Possible proxy"]
    else:
        risk = "LOW"
        reasons = ["Residential-looking IP"]
    return str({"ip": ip_address, "risk": risk, "reasons": reasons})

@tool
def check_merchant_risk(merchant: str) -> str:
    """Get risk assessment for a merchant name."""
    high_risk = ["DarkWebMarket", "CryptoExchange", "Unknown Merchant"]
    if any(h.lower() in merchant.lower() for h in high_risk):
        return str({"merchant": merchant, "risk": "HIGH", "note": "High-risk or unregistered merchant category"})
    return str({"merchant": merchant, "risk": "LOW", "note": "Known legitimate merchant"})

@tool
def calculate_simple_risk_score(
    amount: float,
    is_new_country: bool,
    velocity_count: int,
    ip_risk: str,
    merchant_risk: str,
    customer_risk_tier: str
) -> str:
    """Calculate a simple interpretable risk score (0-100) based on multiple signals."""
    score = 0
    reasons = []

    if amount > 3000:
        score += 25
        reasons.append("High amount")
    elif amount > 1500:
        score += 15
        reasons.append("Elevated amount")

    if is_new_country:
        score += 20
        reasons.append("New/unusual country")

    if velocity_count >= 5:
        score += 20
        reasons.append("High velocity")
    elif velocity_count >= 3:
        score += 10
        reasons.append("Moderate velocity")

    if ip_risk == "HIGH":
        score += 25
        reasons.append("High IP risk")
    elif ip_risk == "MEDIUM":
        score += 12
        reasons.append("Medium IP risk")

    if merchant_risk == "HIGH":
        score += 20
        reasons.append("High-risk merchant")

    if customer_risk_tier == "high":
        score += 15
        reasons.append("Customer on high risk tier")
    elif customer_risk_tier == "medium":
        score += 8

    score = min(score, 100)
    level = "CRITICAL" if score >= 75 else "HIGH" if score >= 55 else "MEDIUM" if score >= 35 else "LOW"
    return str({"score": score, "level": level, "reasons": reasons})