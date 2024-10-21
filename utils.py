import os
import json
import csv


def save_results_to_file(audit_result, file_name, format="json"):
    # Create a new directory for audit results
    audit_dir = "audit_results"
    os.makedirs(audit_dir, exist_ok=True)

    # Construct the full path for the output file
    output_path = os.path.join(audit_dir, file_name)

    json_data = [
        result.dict() if hasattr(result, "dict") else result for result in audit_result
    ]

    if format == "json":
        with open(output_path, "w") as f:
            json.dump(json_data, f, indent=4)
    else:  # CSV format
        csv_data = transform_json(json_data)
        with open(output_path, "w", newline="") as f:
            if csv_data:
                writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                writer.writeheader()
                writer.writerows(csv_data)
            else:
                # Handle the case when there are no results
                writer = csv.writer(f)
                writer.writerow(["No audit results"])


def transform_json(input_json):
    output = []

    for file_entry in input_json:
        file_path = file_entry["file_path"]

        for vulnerability in file_entry["vulnerabilities"]:
            output_entry = {
                "line_number": vulnerability["line_number"],
                "code_snippet": vulnerability["code_snippet"],
                "severity_level": vulnerability["severity_level"],
                "severity_description": vulnerability["severity_description"],
                "file_path": file_path,
            }
            output.append(output_entry)

    return output
