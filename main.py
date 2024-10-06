import argparse
import time

from auditor import audit
from file_reader import read_files_in_folder
from utils import save_results_to_file


def main():
    parser = argparse.ArgumentParser(description="Near Smart Contract Auditor")
    parser.add_argument(
        "folder_path", help="Path to the folder containing Rust files to audit"
    )
    parser.add_argument(
        "--model",
        choices=["gpt-4o", "gpt-3.5-turbo"],
        default="gpt-4o",
        help="Choose the model to use for auditing (default: gpt-4o)",
    )
    parser.add_argument(
        "--output",
        default=f"audit_results_{int(time.time())}.json",
        help="Output file name for audit results with timestamp (default: audit_results_<timestamp>.json)",
    )

    args = parser.parse_args()
    files_content = read_files_in_folder(args.folder_path)

    audit_result = audit(files_content, args.model)
    save_results_to_file(audit_result, args.output)

    return audit_result


if __name__ == "__main__":
    main()
