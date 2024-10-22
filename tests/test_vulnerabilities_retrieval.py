import unittest
from unittest.mock import patch, mock_open
from vulnerabilities.retrieval import load_vulnerabilities, initialize_retriever


class TestVulnerabilitiesRetrieval(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="title,description,severity,detector_id,sample_code\nTest Vuln,Test Description,High,TEST-001,print('test')",
    )
    def test_load_vulnerabilities(self, mock_file):
        documents = load_vulnerabilities("dummy_path.csv")
        self.assertEqual(len(documents), 1)
        self.assertIn("Title: Test Vuln", documents[0].page_content)
        self.assertIn("Description: Test Description", documents[0].page_content)
        self.assertIn("Severity: High", documents[0].page_content)
        self.assertIn("Detector ID: TEST-001", documents[0].page_content)
        self.assertIn("Sample Code:\nprint('test')", documents[0].page_content)
        self.assertEqual(documents[0].metadata, {"source": "TEST-001"})

    @patch("vulnerabilities.retrieval.load_vulnerabilities")
    @patch("vulnerabilities.retrieval.OpenAIEmbeddings")
    @patch("vulnerabilities.retrieval.FAISS")
    def test_initialize_retriever(
        self, mock_faiss, mock_embeddings, mock_load_vulnerabilities
    ):
        mock_load_vulnerabilities.return_value = [{"dummy": "document"}]
        mock_vector_store = mock_faiss.from_documents.return_value

        retriever = initialize_retriever()

        mock_load_vulnerabilities.assert_called_once_with(
            "vulnerabilities/list_vulnerabilities.csv"
        )
        mock_embeddings.assert_called_once()
        mock_faiss.from_documents.assert_called_once()
        mock_vector_store.as_retriever.assert_called_once_with(search_kwargs={"k": 5})
        self.assertEqual(retriever, mock_vector_store.as_retriever.return_value)


if __name__ == "__main__":
    unittest.main()
