import asyncio
from services.stock_data import fetch_stock_summary

if __name__ == "__main__":
    ticker = "AMD"

    result = asyncio.run(fetch_stock_summary(ticker))

    if "error" in result:
        print("❌ Error:", result["error"])
    else:
        print("\n🔎 Stock Summary:")
        for k, v in result["summary"].items():
            print(f"{k}: {v}")

        print("\n📊 Technical Indicators:")
        for k, v in result["technicals"].items():
            print(f"{k}: {v}")
