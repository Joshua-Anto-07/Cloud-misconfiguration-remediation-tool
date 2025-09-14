import json
import os

def save_report(results, filename="reports/assessment_report.json"):
    os.makedirs("reports", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
