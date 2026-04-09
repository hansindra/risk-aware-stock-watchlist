import pandas as pd
import yfinance as yf
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_ASPI_DIR = BASE_DIR / "data" / "raw" / "aspi"
RAW_STOCKS_DIR = BASE_DIR / "data" / "raw" / "stocks"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

RAW_ASPI_DIR.mkdir(parents=True, exist_ok=True)
RAW_STOCKS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

START = "2014-01-01"
END   = "2024-12-31"

ASPI_TICKER = "^CSE"


TICKERS = [
    "COMB-N0000.CM","DFCC-N0000.CM","HNB-N0000.CM","LOLC-N0000.CM","NTB-N0000.CM","SAMP-N0000.CM",
    "BUKI-N0000.CM","CARG-N0000.CM","DIST-N0000.CM","MAL-N0000.CM",
    "BIL-N0000.CM","HAYL-N0000.CM","JKH-N0000.CM","MELS-N0000.CM",
    "ACL-N0000.CM","CTHR-N0000.CM","LIOC-N0000.CM","TJL-N0000.CM",
    "DIAL-N0000.CM","EXPO-N0000.CM","LGL-N0000.CM"
]

SECTOR_MAP = {
    "COMB-N0000.CM":"Banking/Finance","DFCC-N0000.CM":"Banking/Finance","HNB-N0000.CM":"Banking/Finance",
    "LOLC-N0000.CM":"Banking/Finance","NTB-N0000.CM":"Banking/Finance","SAMP-N0000.CM":"Banking/Finance",
    "BUKI-N0000.CM":"Consumer","CARG-N0000.CM":"Consumer","DIST-N0000.CM":"Consumer","MAL-N0000.CM":"Consumer",
    "BIL-N0000.CM":"Diversified","HAYL-N0000.CM":"Diversified","JKH-N0000.CM":"Diversified","MELS-N0000.CM":"Diversified",
    "ACL-N0000.CM":"Industrial","CTHR-N0000.CM":"Industrial","LIOC-N0000.CM":"Industrial","TJL-N0000.CM":"Industrial",
    "DIAL-N0000.CM":"Telecom","EXPO-N0000.CM":"Telecom","LGL-N0000.CM":"Telecom"
}

def clean_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize yfinance output to columns: Date, Open, High, Low, Close, Volume"""
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)  # drop ticker level
    df = df.reset_index()
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    if "Date" not in df.columns:
        if "Datetime" in df.columns:
            df = df.rename(columns={"Datetime":"Date"})
        else:
            raise ValueError(f"No Date column found. Columns: {df.columns.tolist()}")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    keep = [c for c in ["Date","Open","High","Low","Close","Volume"] if c in df.columns]
    return df[keep].sort_values("Date")

print("Downloading ASPI...")
aspi = yf.download(ASPI_TICKER, start=START, end=END, auto_adjust=False, progress=True)
aspi = clean_ohlcv(aspi)
aspi_file = RAW_ASPI_DIR / "ASPI_2014_2024_raw.csv"
aspi.to_csv(aspi_file, index=False)
print("Saved:", aspi_file, "| rows:", len(aspi))

all_parts = []
failed = []

print("\nDownloading stocks...")
for t in TICKERS:
    try:
        df = yf.download(t, start=START, end=END, auto_adjust=False, progress=False)
        df = clean_ohlcv(df)
        if df.empty:
            failed.append(t)
            print("⚠ Empty:", t)
            continue

        df["Ticker"] = t
        df["Sector"] = SECTOR_MAP.get(t, "Unknown")

        df.to_csv(RAW_STOCKS_DIR / f"{t}.csv", index=False)

        all_parts.append(df)
        print(t, "| rows:", len(df))

    except Exception as e:
        failed.append(t)
        print( t, "|", e)

if not all_parts:
    raise RuntimeError("No stock data downloaded. Check internet or tickers.")

stocks_master = pd.concat(all_parts, ignore_index=True)
stocks_master = stocks_master.drop_duplicates(subset=["Date","Ticker"]).sort_values(["Ticker","Date"])

master_file = PROCESSED_DIR / "stocks_master_2014_2024.csv"
stocks_master.to_csv(master_file, index=False)
print("\n Saved master stocks file:", master_file, "| rows:", len(stocks_master), "| tickers:", stocks_master["Ticker"].nunique())

meta = pd.DataFrame({"Ticker": list(SECTOR_MAP.keys()), "Sector": list(SECTOR_MAP.values())})
meta = meta.sort_values(["Sector","Ticker"])
meta_file = PROCESSED_DIR / "stock_metadata.csv"
meta.to_csv(meta_file, index=False)
print(" Saved metadata file:", meta_file)

if failed:
    print("\n Failed tickers:", failed)
