from app.services.risk_agent import run_risk_analysis

if __name__ == "__main__":
    result = run_risk_analysis("AMD")
    print("\n⚠️ Risk Summary:")
    print(result["risk_summary"])
    print(f"\n📄 Based on {result['source_chunks']} matched filing chunks.")
