# Scavene

Scavene is an advanced tool designed to automatically audit Rust-based smart contracts for potential vulnerabilities using Large Language Models (LLMs). It leverages state-of-the-art AI technology to analyze smart contract code, identify security issues, and provide vulnerability reports to developers and auditors.

## Table of Contents

1. [Introduction](#scavene)
2. [Usage Options](#usage-options)
   1. [Using Scavene as a GitHub Action](#1-using-scavene-as-a-github-action)
   2. [Using Scavene Locally](#2-using-scavene-locally)
      - [Requirements](#requirements)
      - [Installation](#installation)
      - [Usage Guide](#usage-guide)
      - [Configuration](#configuration)
3. [Audit Process](#audit-process)
4. [License](#license)
5. [Contributing](#contributing)
6. [Disclaimer](#disclaimer)

## Usage Options

## 1. Using Scavene as a GitHub Action

To integrate Scavene into your GitHub workflow, follow these steps:

1. Create a `.github/workflows` directory in your repository if it doesn't already exist.

2. Create a new file named `scavene-audit.yml` in the `.github/workflows` directory.

3. Add the following content to the `scavene-audit.yml` file:

```yaml
name: Scavene Smart Contract Audit

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  audit:
    runs-on: ubuntu-latest
    permissions: "write-all"
    steps:
    - uses: actions/checkout@v4
    - name: Run Scavene Audit
      uses: ahnafalfariza/scavene-action@v1
      with:
        openai_api_key: ${{ secrets.OPENAI_API_KEY }}
        anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
        model: 'gpt-4'
```

4. Add your API keys as secrets in your GitHub repository:
   - Go to your repository settings
   - Click on "Secrets and variables" > "Actions"
   - Add `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` as new repository secrets

Now, Scavene will automatically run on every push to the main branch and on pull requests, auditing your smart contract code and providing the results for you to review.

*`[Add PR screenshot of the audit results here]`*

## 2. Using Scavene Locally
## Requirements

- Python 3.7+
- OpenAI API key
- Anthropic API key (for Claude model)

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/ahnafalfariza/smart-contract-auditor.git
   cd smart-contract-auditor
   ```

2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  
   
   # On Windows, use 
   `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up your API keys as environment variables:
   ```sh
   export OPENAI_API_KEY='your-openai-api-key-here'
   export ANTHROPIC_API_KEY='your-anthropic-api-key-here'
   ```

## Usage Guide

To use the Smart Contract Auditor, run the `main.py` script with the following syntax:

```sh
python main.py <folder_path> [--model MODEL] [--output OUTPUT_FILE] [--format FORMAT] [--log-level LOG_LEVEL] [--no-log]
```

- `<folder_path>`: Path to the folder containing Rust files to audit, if not exist it will scan current directory
- `--model`: Choose the model to use for auditing (optional, default: gpt-4o)
   - Options: gpt-4o, gpt-3.5-turbo, claude-3.5-sonnet
- `--output`: Output file name for audit results (optional, default: audit_results_<timestamp>.json)
- `--format`: Specifies the output format for the audit results. (optional)
   - Options: json, csv
- `--log-level`: Set the logging level (optional, default: INFO)
   - Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `--no-log`: Disable all logging (optional)

Example:
```sh
python main.py /path/to/your/rust/files --model claude-3.5-sonnet --log-level DEBUG
```

To run the audit without any logging:
```sh
python main.py /path/to/your/rust/files --model gpt-4o --no-log
```

The audit results will be saved in the `audit_results` directory.

## Configuration

The tool uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key (required for OpenAI models)
- `ANTHROPIC_API_KEY`: Your Anthropic API key (required for Claude model)

You can set this in your shell or use a `.env` file (make sure to add `.env` to your `.gitignore`).


## Audit Process

Scavene uses a Retrieval Augmented Generation (RAG) process to enhance the quality and accuracy of smart contract audits. Here's a brief overview of the process:

1. **Knowledge Base**: We maintain a database of known vulnerabilities and best practices for Near smart contracts.
2. **Embedding and Storage**: The knowledge base is converted into vector embeddings and stored in a FAISS vector database.
3. **Code Analysis**: For each function or code block in the smart contract:
   - The code is analyzed to determine its purpose and potential vulnerabilities.
   - Relevant information is retrieved from the knowledge base.
   - The code and retrieved information are sent to the language model for analysis.
4. **Report Generation**: The language model generates audit findings, which are compiled into a comprehensive report.

This approach combines the power of large language models with a curated knowledge base, leading to more accurate and informative audit results.

For a more detailed explanation of the RAG process and how it fits into the overall audit workflow, please refer to the [Retrieval Augmented Generation document](retriever.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the existing coding style.

## Disclaimer

This tool is provided as-is and should be used as part of a comprehensive security review process. It does not guarantee the detection of all vulnerabilities or the absence of false positives.
