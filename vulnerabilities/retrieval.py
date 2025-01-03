import csv
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from utils import get_required_env_var


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
    try:
        documents = []
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Validate required fields exist
                required_fields = [
                    "title",
                    "description",
                    "severity",
                    "detector_id",
                    "sample_code",
                ]
                if not all(field in row for field in required_fields):
                    raise KeyError(f"Missing required fields in CSV row: {row}")

                # Format content with clear section separation
                content = (
                    f"Title: {row['title']}\n"
                    f"Description: {row['description']}\n"
                    f"Severity: {row['severity']}\n"
                    f"Detector ID: {row['detector_id']}\n"
                    f"Sample Code:\n{row['sample_code'].strip()}"
                )

                doc = Document(
                    page_content=content,
                    metadata={
                        "source": row["detector_id"],
                        "severity": row["severity"],
                        "title": row["title"],
                    },
                )
                documents.append(doc)
        return documents
    except FileNotFoundError:
        raise FileNotFoundError(f"Vulnerability data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading vulnerability data: {str(e)}")


def initialize_retriever(provider="openai"):
    """
    Initialize and return a VectorStoreRetriever for the external knowledge base.

    Args:
        provider (str): The embedding provider to use ('openai' or 'ollama')

    Returns:
        VectorStoreRetriever: The initialized retriever object.
    """
    # Load vulnerabilities from CSV
    documents = load_vulnerabilities("vulnerabilities/list_vulnerabilities.csv")

    # Initialize embeddings based on provider
    if provider == "openai":
        api_key = get_required_env_var("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(api_key=api_key)
    elif provider == "ollama":
        embeddings = OllamaEmbeddings(model="llama2")
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")

    # Create the vector store
    vector_store = FAISS.from_documents(documents, embeddings)

    # Create and return a retriever
    return vector_store.as_retriever(search_kwargs={"k": 5})
