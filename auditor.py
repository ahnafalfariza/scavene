import os
import json
from openai import OpenAI

from file_reader import read_files_in_folder
from audit_response import AuditResponse
from prompts import prompt_4o, prompt_older_model

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def audit_file_4o(file_content):
    chat_completion = client.beta.chat.completions.parse(
        messages=[
            {"role": "system", "content": prompt_4o},
            {"role": "user", "content": file_content},
        ],
        model="gpt-4o-2024-08-06",
        response_format=AuditResponse,
    )
    return chat_completion.choices[0].message.parsed


def audit_file_old_model(file_content, model="gpt-3.5-turbo"):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt_older_model},
            {"role": "user", "content": file_content},
        ],
        model=model,
        response_format={"type": "json_object"},
    )
    return json.loads(chat_completion.choices[0].message.content)


def audit(files_content, model="gpt-4o"):
    audit_result = []
    for filepath, content in files_content.items():
        chat_completion = None
        if model == "gpt-4o":
            chat_completion = audit_file_4o(content)
        elif model == "gpt-3.5-turbo":
            chat_completion = audit_file_old_model(content)
        else:
            raise ValueError(
                "Invalid model specified. Please choose 'gpt-4o' or 'gpt-3.5-turbo'."
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
