from backend.benchmark_runner import run_benchmarks, SUBSCRIPTION_ID
from backend.report_generator import save_report
from generate_ui import generate_html_report
from backend.remediation import remediate_misconfigurations

if __name__ == "__main__":
    print("Running benchmarks...")
    results = run_benchmarks()
    save_report(results)
    print("Done. Results saved in reports/assessment_report.json")
    generate_html_report()

    remediate = input("Do you want to remediate the misconfigured resources? (y/n): ")
    if remediate.lower() == 'y':
        remediate_misconfigurations(results, SUBSCRIPTION_ID)