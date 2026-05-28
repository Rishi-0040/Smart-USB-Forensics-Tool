import os

SUSPICIOUS_EXTENSIONS = [
    ".exe",
    ".dll",
    ".bat",
    ".cmd",
    ".vbs",
    ".js",
    ".ps1",
    ".scr",
    ".pif",
    ".com",
    ".cpl",
    ".msi"   
]

SUSPICIOUS_KEYWORDS = [
    "password",
    "bank",
    "account",
    "login",
    "credentials",
    "secret",
    "confidential",
    "private",
    "ssn",
    "social security",
    "credit card",
    "cvv",
    "expiry",
    "pin",
    "key",
    "token",
    "api",
    "wallet",
    "crypto",
    "bitcoin",
    "ethereum",
    "monero",
    "dash",
    "zcash",
    "ripple",
    "litecoin",
    "dogecoin",
    "tron",
    "stellar",
    "cardano",
    "polkadot",
    "solana",
    "avalanche",
    "binance",
    "coinbase",
    "kraken",
    "gemini",
    "bitfinex",
    "huobi",
    "okex",
    "bittrex",
    "bitstamp",
    "bitmex",
    "deribit",
    "bybit",
    "ftx",
    "kraken",
    "binance",
    "coinbase"
]

def calculate_risk(file_path):

    risk_score = 0
    reasons = []

    filename = os.path.basename(file_path).lower()

    # Check for suspicious file extensions
    for ext in SUSPICIOUS_EXTENSIONS:
        
        if filename.endswith(ext):
            risk_score += 10
            reasons.append(f"Suspicious file extension: {ext}")

    # Check for suspicious keywords in filename
    for keyword in SUSPICIOUS_KEYWORDS:
        
        if keyword in filename:
            risk_score += 7
            reasons.append(f"Suspicious/sensitive keyword in filename: {keyword}")
    
    # Check for hidden files
    if filename.startswith("."):
        risk_score += 5
        reasons.append(f"Hidden file: {filename}")

    return risk_score, reasons