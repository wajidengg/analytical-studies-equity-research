import yfinance as yf

def load_company_data(ticker: str):
    stock = yf.Ticker(ticker)

    return {
        "info": stock.info,
        "financials": stock.financials,
        "balance_sheet": stock.balance_sheet,
        "cashflow": stock.cashflow,
        "history": stock.history(period="5y")
    }
