from pydantic import BaseModel


class Result(BaseModel):
    line_number: str
    code_snippet: str
    severity_level: str
    severity_description: str


class AuditResponse(BaseModel):
    vulnerabilities: list[Result]
    file_path: str
