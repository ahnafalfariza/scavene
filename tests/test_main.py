import unittest
from unittest.mock import patch, MagicMock
from main import main


class TestMain(unittest.TestCase):

    @patch("main.argparse.ArgumentParser.parse_args")
    @patch("main.read_files_in_folder")
    @patch("main.initialize_retriever")
    @patch("main.audit")
    @patch("main.save_results_to_file")
    @patch("main.json.dumps")
    def test_main_function(
        self,
        mock_json_dumps,
        mock_save_results,
        mock_audit,
        mock_initialize_retriever,
        mock_read_files,
        mock_parse_args,
    ):
        # Setup mock returns
        mock_parse_args.return_value = MagicMock(
            folder_path="./test_folder",
            model="gpt-4o",
            output="test_output",
            format="json",
            log_level="INFO",
            no_log=False,
        )
        mock_read_files.return_value = {"test_file.rs": "test content"}
        mock_initialize_retriever.return_value = MagicMock()
        mock_audit.return_value = [{"vulnerability": "test"}]
        mock_json_dumps.return_value = '{"vulnerability": "test"}'

        # Call the main function
        result = main()

        # Assertions
        mock_read_files.assert_called_once_with("./test_folder")
        mock_initialize_retriever.assert_called_once()
        mock_audit.assert_called_once_with(
            {"test_file.rs": "test content"},
            "gpt-4o",
            mock_initialize_retriever.return_value,
        )
        mock_save_results.assert_called_once_with(
            [{"vulnerability": "test"}], "test_output.json", "json"
        )
        mock_json_dumps.assert_called_once_with([{"vulnerability": "test"}])

        self.assertEqual(result, [{"vulnerability": "test"}])


if __name__ == "__main__":
    unittest.main()
