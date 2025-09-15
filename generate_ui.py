import os
import json

def generate_html_report():
    if not os.path.exists("reports/assessment_report.json"):
        print("Assessment report not found. Please run the benchmark first.")
        return

    with open("reports/assessment_report.json", "r") as f:
        results = json.load(f)

    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assessment Report</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Cloud Misconfiguration Assessment Report</h1>
    <table>
        <thead>
            <tr>
                <th>Setting</th>
                <th>Configured Properly</th>
                <th>Correction</th>
            </tr>
        </thead>
        <tbody>
'''

    for result in results:
        status = result.get("status", "pass")
        configured_properly = "Yes" if status == "pass" else "No"
        correction = "-" if status == "pass" else result.get("remediation", "N/A")
        description = result.get("description", "N/A")
        
        html_content += f'''
            <tr>
                <td>{description}</td>
                <td>{configured_properly}</td>
                <td>{correction}</td>
            </tr>
'''

    html_content += '''
        </tbody>
    </table>
</body>
</html>
'''
    os.makedirs("frontend", exist_ok=True)
    with open("frontend/index.html", "w") as f:
        f.write(html_content)

    css_content = '''
body {
    font-family: sans-serif;
    margin: 20px;
    background-color: #f4f4f9;
    color: #333;
}

h1 {
    text-align: center;
    color: #444;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    background-color: #fff;
}

th, td {
    padding: 12px 15px;
    border: 1px solid #ddd;
    text-align: left;
}

thead {
    background-color: #007bff;
    color: #fff;
}

tbody tr:nth-child(even) {
    background-color: #f2f2f2;
}

tbody tr:hover {
    background-color: #e9ecef;
}
'''
    with open("frontend/style.css", "w") as f:
        f.write(css_content)
    
    print("UI generated in frontend/index.html")
