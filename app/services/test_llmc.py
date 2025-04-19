from app.services.llm_coordinator import generate_analyst_report

if __name__ == "__main__":
    result = generate_analyst_report("AMD")
    print("\n📈 Final Analyst Report:\n")
    print(result["report"])
