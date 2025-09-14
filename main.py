from backend.benchmark_runner import check_public_storage_access, SUBSCRIPTION_ID
from backend.report_generator import save_report
from generate_ui import generate_html_report

if __name__ == "__main__":
    print("Running public access check on storage accounts...")
    results = check_public_storage_access(SUBSCRIPTION_ID)
    save_report(results)
    print("Done. Results saved in reports/assessment_report.json")
    generate_html_report()