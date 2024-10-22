from pydantic import BaseModel


class Result(BaseModel):
    """
    Represents a single vulnerability result in the audit.

    Attributes:
    line_number (str): The line number(s) where the vulnerability is found.
    code_snippet (str): The relevant code snippet containing the vulnerability.
    severity_level (str): The severity level of the vulnerability.
    severity_description (str): A brief description of the vulnerability and its potential impact.
    """
    line_number: str
    code_snippet: str
    severity_level: str
    severity_description: str


class AuditResponse(BaseModel):
    """
    Represents the overall audit response for a file.

    Attributes:
    vulnerabilities (list[Result]): A list of vulnerability results found in the file.
    file_path (str): The path of the audited file.
    """
    vulnerabilities: list[Result]
    file_path: str
