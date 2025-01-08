# Output Format Documentation

## Overview

Scavene provides audit results in two formats:
- JSON (default)
- CSV

## JSON Format

### Structure
```json
[
    {
        "vulnerabilities": [
            {
                "line_number": "48-52",
                "code_snippet": "pub fn mint(&mut self) -> Balance {\n    self.tokens.insert(self.supply.to_le_bytes()[0], env::predecessor_account_id());\n    let id = self.supply;\n    self.supply += 1;\n    id as Balance\n}",
                "severity_level": "High",
                "severity_description": "The mint function has no access control, allowing any account to mint new tokens. This could lead to unauthorized token creation and inflation of the token supply. Additionally, there's a potential overflow vulnerability when converting supply (u16) to Balance (u8)."
            }
        ],
        "file_path": "src/lib.rs"
    }
]
```

### Field Descriptions

#### Vulnerability Fields
| Field | Type | Description |
|-------|------|-------------|
| line_number | string | Location range in source file (e.g., "48-52") |
| code_snippet | string | The relevant code section being analyzed |
| severity_level | string | High, Medium, or Low |
| severity_description | string | Detailed explanation of the vulnerability and its implications |
| file_path | string | Path to the source file |

## CSV Format

### Structure
```csv
File Path,Line Number,Severity Level,Code Snippet,Severity Description
src/lib.rs,48-52,High,"pub fn mint(&mut self) -> Balance {...}","The mint function has no access control..."
```

### Column Descriptions
1. **File Path**: Source file location
2. **Line Number**: Range of affected lines
3. **Severity Level**: Vulnerability severity
4. **Code Snippet**: Relevant code section
5. **Severity Description**: Detailed explanation

## Severity Levels

### High
- Critical security concerns
- Immediate attention required
- Potential for significant impact

### Medium
- Notable security issues
- Should be addressed soon
- Moderate potential impact

### Low
- Minor concerns
- Can be addressed later
- Limited potential impact

## Usage Examples

### Generating JSON Output
```sh
python main.py --provider anthropic --model claude-3.5-sonnet-latest --format json
```

### Generating CSV Output
```sh
python main.py --provider anthropic --model claude-3.5-sonnet-latest --format csv
```

### Custom Output File
```sh
python main.py --provider anthropic --model claude-3.5-sonnet-latest --output my_audit_results
```

## Processing Results

### Python Example
```python
import json

# Read JSON results
with open('audit_results.json', 'r') as f:
    results = json.load(f)

# Process high severity findings
high_severity = [
    vuln for result in results
    for vuln in result['vulnerabilities']
    if vuln['severity_level'] == 'High'
]
```
