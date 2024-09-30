import os


def read_files_in_folder(folder_path):
    """
    Read all files in the specified folder and return their contents.

    Args:
    folder_path (str): Path to the folder containing the files.

    Returns:
    dict: A dictionary where keys are file names and values are file contents.
    """
    file_contents = {}

    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                    file_contents[filename] = content
                except Exception as e:
                    print(f"Error reading file {filename}: {str(e)}")

    except Exception as e:
        print(f"Error accessing folder {folder_path}: {str(e)}")

    return file_contents


if __name__ == "__main__":
    folder_to_read = "path/to/your/folder"
    files_content = read_files_in_folder(folder_to_read)

    for filename, content in files_content.items():
        print(f"File: {filename}")
        print(f"Content:\n{content}")
        print("-" * 50)
