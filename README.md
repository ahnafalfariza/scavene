# Smart Contract Auditor

The Smart Contract Auditor is a tool designed to automatically audit Rust-based smart contracts for potential vulnerabilities using LLM models.

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
python main.py <folder_path> [--model MODEL] [--output OUTPUT_FILE]
```

- `<folder_path>`: Path to the folder containing Rust files to audit, if not exist it will scan current directory
- `--model`: Choose the model to use for auditing (optional, default: gpt-4o)
  - Options: gpt-4o, gpt-3.5-turbo, claude-3.5-sonnet
- `--output`: Output file name for audit results (optional, default: audit_results_<timestamp>.json)

Example:
```sh
python main.py /path/to/your/rust/files --model claude-3.5-sonnet --output my_audit_results.json
```

The audit results will be saved in the `audit_results` directory.

## Configuration

The tool uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key (required for OpenAI models)
- `ANTHROPIC_API_KEY`: Your Anthropic API key (required for Claude model)

You can set this in your shell or use a `.env` file (make sure to add `.env` to your `.gitignore`).

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
