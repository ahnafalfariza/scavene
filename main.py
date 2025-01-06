import argparse
import time
import json
import logging
from dotenv import load_dotenv

from auditor import audit
from file_reader import read_files_in_folder
from utils import save_results_to_file
from vulnerabilities.retrieval import initialize_retriever
from logging_config import setup_logging

load_dotenv()


def main():
    """
    Main function to run the Near Smart Contract Auditor.

    Parses command-line arguments, reads files from the specified folder,
    performs the audit, saves the results, and prints the output.

    Returns:
    list: The audit results.
    """
    parser = argparse.ArgumentParser(description="Near Smart Contract Auditor")
    parser.add_argument(
        "folder_path",
        nargs="?",
        default=".",
        help="Path to the folder containing Rust files to audit (default: current directory)",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "ollama", "huggingface"],
        help="Choose the provider for the model. Eg. openai, anthropic, ollama",
        required=True,
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Choose the model from the provider to use for auditing. Eg. gpt-4o, gpt-3.5-turbo, etc",
    )
    parser.add_argument(
        "--retrieval-provider",
        choices=["openai", "ollama"],
        default="openai",
        help="Choose the provider for embeddings (default: openai)",
    )
    parser.add_argument(
        "--output",
        default=f"audit_results_{int(time.time())}",
        help="Output file name for audit results without extension (default: audit_results_<timestamp>)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Choose the output format (default: json)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level (default: INFO)",
    )
    parser.add_argument("--no-log", action="store_true", help="Disable all logging")

    args = parser.parse_args()

    setup_logging(args.log_level, args.no_log)

    logging.info(
        f"Starting audit process with provider: {args.provider} and model: {args.model}"
    )
    logging.info(f"Reading files from folder: {args.folder_path}")

    files_content = read_files_in_folder(args.folder_path)
    logging.info(f"Found {len(files_content)} Rust files to audit")
    for file_name in files_content.keys():
        logging.info(f"File to audit: {file_name}")
    logging.info("Starting audit process")

    logging.info(f"Initializing retriever with provider: {args.retrieval_provider}")
    retriever = initialize_retriever(args.retrieval_provider)

    logging.info("Starting audit")
    audit_result = audit(files_content, args.provider, args.model, retriever)

    output_file = f"{args.output}.{args.format}"
    logging.info(f"Saving audit results to {output_file}")
    save_results_to_file(audit_result, output_file, args.format)

    formatted_audit_result = [
        result.dict() if hasattr(result, "dict") else result for result in audit_result
    ]
    print(json.dumps(formatted_audit_result))

    return audit_result


if __name__ == "__main__":
    main()
