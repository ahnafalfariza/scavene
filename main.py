import argparse
import time
import json
import csv
import sys
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from auditor import audit
from file_reader import read_files_in_folder
from utils import save_results_to_file


def load_vulnerabilities(file_path):
    """
    Load vulnerability information from a CSV file and convert it into a list of Document objects.

    This function reads a CSV file containing vulnerability data and creates a Document object
    for each row. The Document objects contain formatted content with vulnerability details
    and metadata with the detector ID.

    Args:
        file_path (str): The path to the CSV file containing vulnerability information.

    Returns:
        list: A list of Document objects, each representing a vulnerability from the CSV file.

    Each Document object contains:
    - page_content: A formatted string with vulnerability details (title, description, severity, etc.)
    - metadata: A dictionary with the 'source' key set to the detector ID
    """
    documents = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            content = f"Title: {row['title']}\nDescription: {row['description']}\nSeverity: {row['severity']}\nDetector ID: {row['detector_id']}\nSample Code:\n{row['sample_code']}"
            doc = Document(page_content=content, metadata={"source": row['detector_id']})
            documents.append(doc)
    return documents


def initialize_retriever():
    """
    Initialize and return a VectorStoreRetriever for the external knowledge base.

    Returns:
    VectorStoreRetriever: The initialized retriever object.
    """
    # Load vulnerabilities from CSV
    documents = load_vulnerabilities("vulnerabilities/list_vulnerabilities.csv")

    # Initialize embeddings
    embeddings = OpenAIEmbeddings()

    # Create the vector store
    vector_store = FAISS.from_documents(documents, embeddings)

    # Create and return a retriever
    return vector_store.as_retriever(search_kwargs={"k": 5})


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
        "--model",
        choices=["gpt-4o", "gpt-3.5-turbo", "claude-3.5-sonnet"],
        default="gpt-4o",
        help="Choose the model to use for auditing (default: gpt-4o)",
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

    args = parser.parse_args()
    files_content = read_files_in_folder(args.folder_path)

    # Initialize the retriever for the external knowledge base
    retriever = initialize_retriever()

    # Pass the retriever to the audit function
    audit_result = audit(files_content, args.model, retriever)

    output_file = f"{args.output}.{args.format}"
    save_results_to_file(audit_result, output_file, args.format)

    formatted_audit_result = [
        result.dict() if hasattr(result, "dict") else result for result in audit_result
    ]
    print(json.dumps(formatted_audit_result))

    return audit_result


if __name__ == "__main__":
    main()
