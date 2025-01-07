# Scavene

Scavene is an advanced tool designed to automatically audit Rust-based smart contracts for potential vulnerabilities using Large Language Models (LLMs). It leverages state-of-the-art AI technology with retrieval-augmented generation to enhance its analysis. By retrieving facts from an external knowledge base, such as common vulnerabilities in NEAR, security issues, and best practices, Scavene can identifies security threats and provides comprehensive vulnerability reports to developers and auditors

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
    branches:
      - main
  pull_request:
    branches:
      - main
jobs:
  audit:
    runs-on: ubuntu-latest
    permissions: "write-all"
    steps:
      - name: Scavene Audit
        uses: ahnafalfariza/scavene@master
        with:
          openai_api_key: '${{ secrets.OPENAI_API_KEY }}'
          anthropic_api_key: '${{ secrets.ANTHROPIC_API_KEY }}'
          provider: anthropic
          model: claude-3.5-sonnet
          myToken: '${{ secrets.GITHUB_TOKEN }}'
```

4. Add your API keys as secrets in your GitHub repository:
   - Go to your repository settings
   - Click on "Secrets and variables" > "Actions"
   - Add `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` as new repository secrets

Now, Scavene will automatically run on every push to the main branch and on pull requests, auditing your smart contract code and providing the results for you to review.

_Screenshot result on Pull Request and on the action terminal_

<img width="350" alt="image" src="https://github.com/user-attachments/assets/9aba7074-d582-4e9f-b36c-c89d5cbffcc7">
<img width="579" alt="image" src="https://github.com/user-attachments/assets/028e9ba7-e35f-4582-b258-b4ff73b9b47c">


## 2. Using Scavene Locally
## Requirements

- Python 3.7+
- OpenAI API key
- Anthropic API key (for Claude model)

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/ahnafalfariza/scavene.git
   cd scavene
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

To use the Scavene, run the `main.py` script with the following syntax:

```sh
python main.py [folder_path] --provider PROVIDER --model MODEL [additional options]
```

### Model Providers
Scavene supports both remote (cloud-based) and local model providers:

Remote Providers:
- `openai`: OpenAI's models (requires API key)
- `anthropic`: Anthropic's Claude models (requires API key)

Local Providers:
- `ollama`: Run models locally using Ollama
- `huggingface`: Use local Hugging Face models

### Arguments
Required arguments:
- `--provider`: Choose the provider for the model
  - Options: openai, anthropic, ollama, huggingface
- `--model`: Specify the model to use from the chosen provider
  - Examples: gpt-4o, claude-3.5-sonnet-latest, llama3.2:3b

Optional arguments:
- `folder_path`: Path to the folder containing Rust files to audit (default: current directory)
- `--retrieval-provider`: Choose the provider for embeddings (default: openai)
  - Options: openai, ollama
- `--output`: Output file name for audit results without extension (default: audit_results_<timestamp>)
- `--format`: Specifies the output format (default: json)
  - Options: json, csv
- `--log-level`: Set the logging level (default: INFO)
  - Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `--no-log`: Disable all logging

Examples:
```sh
# Audit current directory using Claude
python main.py --provider anthropic --model claude-3.5-sonnet-latest

# Audit specific folder using GPT-4
python main.py /path/to/your/rust/files --provider openai --model gpt-4o --log-level DEBUG

# Use Ollama for both model and embeddings
python main.py --provider ollama --model llama3.2:3b --retrieval-provider ollama
```

The audit results will be saved in the `audit_results` directory.

## Configuration
### API Keys

For remote providers, you'll need to set up API keys:
- OpenAI: Required when using `--provider openai`
- Anthropic: Required when using `--provider anthropic`
- Hugging Face: Required when using `--provider huggingface`

Local providers:
- Ollama: No API key required, but needs the Ollama environment set up locally
- Hugging Face: Requires `HUGGINGFACEHUB_API_TOKEN` for authentication and local model setup

You can set up your API keys in your environment or .env file:
```sh
OPENAI_API_KEY='your-openai-api-key'
ANTHROPIC_API_KEY='your-anthropic-api-key'
HUGGINGFACEHUB_API_TOKEN='your-huggingface-token'
```


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
