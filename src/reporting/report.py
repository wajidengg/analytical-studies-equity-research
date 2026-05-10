from datetime import datetime

def generate_report(ticker, features, interpretation):
    date = datetime.now().strftime("%Y-%m-%d")

    report = f"""
# Analytical Studies in Equity Research

## Study: {ticker}
Date: {date}

---

## Company Overview
{features.get("company")} | Sector: {features.get("sector")}

---

## Key Metrics
- P/E: {features.get("pe_ratio")}
- Margin: {features.get("profit_margin")}
- Growth: {features.get("revenue_growth")}
- Debt/Equity: {features.get("debt_to_equity")}
- ROE: {features.get("roe")}

---

## Interpretation

"""

    for i in interpretation:
        report += f"- {i}\n"

    return report
