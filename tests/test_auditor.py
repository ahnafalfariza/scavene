import unittest
from unittest.mock import patch, MagicMock
from auditor import audit_file_with_knowledge, audit


class TestAuditor(unittest.TestCase):

    @patch("auditor.get_relevant_knowledge")
    @patch("auditor.audit_file_4o")
    def test_audit_file_with_knowledge_gpt4o(
        self, mock_audit_file_4o, mock_get_relevant_knowledge
    ):
        mock_get_relevant_knowledge.return_value = "Relevant knowledge"
        mock_audit_file_4o.return_value = {"vulnerabilities": ["test vulnerability"]}

        result = audit_file_with_knowledge("test content", "gpt-4o", MagicMock())

        mock_get_relevant_knowledge.assert_called_once()
        mock_audit_file_4o.assert_called_once_with("test content", "Relevant knowledge")
        self.assertEqual(result, {"vulnerabilities": ["test vulnerability"]})

    @patch("auditor.get_relevant_knowledge")
    @patch("auditor.audit_file_old_model")
    def test_audit_file_with_knowledge_gpt35(
        self, mock_audit_file_old_model, mock_get_relevant_knowledge
    ):
        mock_get_relevant_knowledge.return_value = "Relevant knowledge"
        mock_audit_file_old_model.return_value = {
            "vulnerabilities": ["test vulnerability"]
        }

        result = audit_file_with_knowledge("test content", "gpt-3.5-turbo", MagicMock())

        mock_get_relevant_knowledge.assert_called_once()
        mock_audit_file_old_model.assert_called_once_with(
            "test content", "Relevant knowledge"
        )
        self.assertEqual(result, {"vulnerabilities": ["test vulnerability"]})

    @patch("auditor.audit_file_with_knowledge")
    def test_audit(self, mock_audit_file_with_knowledge):
        mock_audit_file_with_knowledge.return_value = {
            "vulnerabilities": ["test vulnerability"]
        }
        files_content = {"test_file.rs": "test content"}
        retriever = MagicMock()

        result = audit(files_content, "gpt-4o", retriever)

        mock_audit_file_with_knowledge.assert_called_once_with(
            "test content", "gpt-4o", retriever
        )
        self.assertEqual(
            result,
            [{"vulnerabilities": ["test vulnerability"], "file_path": "test_file.rs"}],
        )


if __name__ == "__main__":
    unittest.main()
