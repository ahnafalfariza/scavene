import os
import json
import csv


def save_results_to_file(audit_result, file_name, format="json"):
    """
    Save audit results to a file in the specified format.

    Args:
    audit_result (list): The audit results to save.
    file_name (str): The name of the output file.
    format (str): The output format, either "json" or "csv" (default: "json").
    """
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
    """
    Transform the input JSON data into a flattened format suitable for CSV export.

    Args:
    input_json (list): The input JSON data to transform.

    Returns:
    list: A list of dictionaries with flattened data structure.
    """
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

def export_to_csv(data, output_file):
    """
    Export data to a CSV file.
    
    Args:
    data (list): List of dictionaries containing the data to be exported.
    output_file (str): Path to the output CSV file.
    """
    if not data:
        print("No data to export.")
        return

    fieldnames = data[0].keys()

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Data exported to {output_file}")

