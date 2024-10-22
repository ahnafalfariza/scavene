import csv
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


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
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            content = f"Title: {row['title']}\nDescription: {row['description']}\nSeverity: {row['severity']}\nDetector ID: {row['detector_id']}\nSample Code:\n{row['sample_code']}"
            doc = Document(
                page_content=content, metadata={"source": row["detector_id"]}
            )
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
