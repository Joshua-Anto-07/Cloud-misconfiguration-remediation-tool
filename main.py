from backend.benchmark_runner import run_benchmarks
from backend.report_generator import save_report
from generate_ui import generate_html_report

if __name__ == "__main__":
    print("Running benchmarks...")
    results = run_benchmarks()
    save_report(results)
    print("Done. Results saved in reports/assessment_report.json")
    generate_html_report()
