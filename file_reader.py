import os


def read_files_in_folder(folder_path, file_extension=".rs"):
    """
    Read all files with specified extension in the folder and its subfolders, and return their contents.

    Args:
    folder_path (str): Path to the folder containing the files.
    file_extension (str): File extension to filter (default: ".rs" for Rust files).

    Returns:
    dict: A dictionary where keys are relative file paths and values are file contents.
    """
    file_contents = {}

    try:
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith(file_extension):
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, folder_path)
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            content = file.read()
                        file_contents[relative_path] = content
                    except Exception as e:
                        print(f"Error reading file {relative_path}: {str(e)}")

    except Exception as e:
        print(f"Error accessing folder {folder_path}: {str(e)}")

    return file_contents
