import os
import json
import anthropic
from openai import OpenAI

from file_reader import read_files_in_folder
from audit_response import AuditResponse
from prompts import prompt_4o, prompt_older_model


def audit_file_4o(file_content):
    """
    Audit a file using the GPT-4o model.

    Args:
    file_content (str): The content of the file to be audited.

    Returns:
    AuditResponse: The parsed audit response from the GPT-4o model.
    """
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = openai_client.beta.chat.completions.parse(
        messages=[
            {"role": "system", "content": prompt_4o},
            {"role": "user", "content": file_content},
        ],
        model="gpt-4o-2024-08-06",
        response_format=AuditResponse,
    )
    return chat_completion.choices[0].message.parsed


def audit_file_old_model(file_content, model="gpt-3.5-turbo"):
    """
    Audit a file using an older GPT model.

    Args:
    file_content (str): The content of the file to be audited.
    model (str): The model to use for auditing (default: "gpt-3.5-turbo").

    Returns:
    dict: The parsed JSON response from the model, or an error dictionary if parsing fails.
    """
    openai_client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = openai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt_older_model},
            {"role": "user", "content": file_content},
        ],
        model=model,
        response_format={"type": "json_object"},
    )
    try:
        return json.loads(chat_completion.choices[0].message.content)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from GPT-3.5 Turbo model"}


def audit_file_claude(file_content):
    """
    Audit a file using the Claude 3.5 Sonnet model.

    Args:
    file_content (str): The content of the file to be audited.

    Returns:
    dict: The parsed JSON response from the Claude model, or an error dictionary if parsing fails.
    """
    anthropic_client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        temperature=0,
        system=prompt_older_model,
        messages=[
            {"role": "user", "content": file_content},
        ],
    )

    try:
        return json.loads(message.content[0].text)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from Claude model"}


def audit(files_content, model="gpt-4o"):
    """
    Audit multiple files using the specified model.

    Args:
    files_content (dict): A dictionary where keys are file paths and values are file contents.
    model (str): The model to use for auditing (default: "gpt-4o").

    Returns:
    list: A list of audit results for files with vulnerabilities.

    Raises:
    ValueError: If an invalid model is specified.
    """
    audit_result = []
    for filepath, content in files_content.items():
        chat_completion = None
        if model == "gpt-4o":
            chat_completion = audit_file_4o(content)
        elif model == "gpt-3.5-turbo":
            chat_completion = audit_file_old_model(content)
        elif model == "claude-3.5-sonnet":
            chat_completion = audit_file_claude(content)
        else:
            raise ValueError(
                "Invalid model specified. Please choose 'gpt-4o', 'gpt-3.5-turbo', or 'claude-3.5-sonnet'."
            )

        if (
            isinstance(chat_completion, dict)
            and "vulnerabilities" in chat_completion
            and chat_completion["vulnerabilities"]
        ):
            chat_completion["file_path"] = filepath
            audit_result.append(chat_completion)
        elif (
            hasattr(chat_completion, "vulnerabilities")
            and chat_completion.vulnerabilities != []
        ):
            chat_completion.file_path = filepath
            audit_result.append(chat_completion)

    return audit_result


if __name__ == "__main__":
    audit()
