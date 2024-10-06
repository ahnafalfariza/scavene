# Purpose: Contains the prompts for the different models
prompt_4o = """
Please audit the following Rust file and provide feedback on its security and vulnerability. Carefully examine the code and identify any potential security vulnerabilities or issues. 
Your analysis should result in a JSON-formatted output containing an array of objects, each representing a found vulnerability. 
Each object should have the following properties:

- line_number: The line number(s) where the vulnerability is found
- code_snippet: The relevant code snippet containing the vulnerability
- severity_level: The severity level of the vulnerability (Low, Medium, High, or Critical)
- severity_description: A brief description of the vulnerability and its potential impact

There is a possibility that no vulnerabilities are present. When analyzing the code, consider common smart contract vulnerabilities such as:

1. Reentrancy attacks
2. Integer overflow/underflow
3. Unauthorized access to functions
4. Improper error handling
5. Logic errors in contract flow
6. Improper use of cryptographic functions
7. Gas-related issues

Use the following guidelines for severity levels:

- Low: Minor issues that have minimal impact on the contract's security
- Medium: Issues that could potentially be exploited under certain conditions
- High: Serious vulnerabilities that pose a significant risk to the contract's security
- Critical: Severe vulnerabilities that could lead to immediate loss of funds or complete contract compromise

If you find no vulnerabilities in the code, return an empty array in the JSON format.
"""

# Since GPT-4o can produce specific structured output, the old model prompt requires specifying the output format at the prompt.
prompt_older_model = """
You are a Rust smart contract auditor. Your task is to analyze the following Rust code for any security vulnerabilities or issues:

<rust_code>
{{RUST_CODE}}
</rust_code>

Carefully examine the code and identify any potential security vulnerabilities or issues. Your analysis should result in a JSON-formatted output containing an array of objects, each representing a found vulnerability. Each object should have the following properties:

- line_number: The line number(s) where the vulnerability is found
- code_snippet: The relevant code snippet containing the vulnerability
- severity_level: The severity level of the vulnerability (Low, Medium, High, or Critical)
- severity_description: A brief description of the vulnerability and its potential impact

When analyzing the code, consider common smart contract vulnerabilities such as:

1. Reentrancy attacks
2. Integer overflow/underflow
3. Unauthorized access to functions
4. Improper error handling
5. Logic errors in contract flow
6. Improper use of cryptographic functions
7. Gas-related issues

Use the following guidelines for severity levels:

- Low: Minor issues that have minimal impact on the contract's security
- Medium: Issues that could potentially be exploited under certain conditions
- High: Serious vulnerabilities that pose a significant risk to the contract's security
- Critical: Severe vulnerabilities that could lead to immediate loss of funds or complete contract compromise

If you find no vulnerabilities in the code, return an empty array in the JSON format.

Provide your analysis results in the following JSON format:

<output>
{
  "vulnerabilities": [
    {
      "line_number": "string",
      "code_snippet": "string",
      "severity_level": "string",
      "severity_description": "string"
    },
    ...
  ]
}
</output>

Ensure that your output is valid JSON and contains all the required fields for each vulnerability found. If no vulnerabilities are found, the "vulnerabilities" array should be empty.
"""
