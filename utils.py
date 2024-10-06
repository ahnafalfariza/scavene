import os
import json


def save_results_to_file(audit_result, file_name):
    # Create a new directory for audit results
    audit_dir = "audit_results"
    os.makedirs(audit_dir, exist_ok=True)

    # Construct the full path for the output file
    output_path = os.path.join(audit_dir, file_name)

    with open(output_path, "w") as f:
        json_data = [
            result.dict() if hasattr(result, "dict") else result
            for result in audit_result
        ]
        json.dump(json_data, f, indent=4)
