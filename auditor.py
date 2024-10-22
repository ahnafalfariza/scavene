import os
import json
import anthropic
from openai import OpenAI

from file_reader import read_files_in_folder
from audit_response import AuditResponse
from prompts import prompt_4o, prompt_older_model


def write_relevant_knowledge_to_file(
    relevant_knowledge, filename="relevant_knowledge.txt"
):
    """
    Write the relevant knowledge to a text file.

    Args:
    relevant_knowledge (str): The relevant knowledge to be written to the file.
    filename (str): The name of the file to write to (default: "relevant_knowledge.txt").
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(relevant_knowledge)
    print(f"Relevant knowledge has been written to {filename}")


def get_relevant_knowledge(query, retriever):
    """
    Retrieve relevant knowledge from the external knowledge base.

    Args:
    query (str): The query to search for in the knowledge base.
    retriever (VectorStoreRetriever): The retriever object for the knowledge base.

    Returns:
    str: Relevant knowledge retrieved from the knowledge base.
    """
    documents = retriever.invoke(query)
    formatted_knowledge = []
    for doc in documents:
        formatted_knowledge.append(
            f"Source: {doc.metadata['source']}\n{doc.page_content}\n---"
        )
    relevant_knowledge = "\n\n".join(formatted_knowledge)

    return relevant_knowledge


def audit_file_with_knowledge(file_content, model, retriever):
    """
    Audit a file using the specified model and external knowledge.

    Args:
    file_content (str): The content of the file to be audited.
    model (str): The model to use for auditing.
    retriever (VectorStoreRetriever): The retriever object for the knowledge base.

    Returns:
    dict or AuditResponse: The parsed audit response from the model.
    """
    # Create a query that includes key information from the file content
    query = f"Audit this Rust code for security vulnerabilities: {file_content[:500]}..."  # Use first 500 characters as a sample
    relevant_knowledge = get_relevant_knowledge(query, retriever)

    if model == "gpt-4o":
        return audit_file_4o(file_content, relevant_knowledge)
    elif model == "gpt-3.5-turbo":
        return audit_file_old_model(file_content, relevant_knowledge)
    elif model == "claude-3.5-sonnet":
        return audit_file_claude(file_content, relevant_knowledge)
    else:
        raise ValueError("Invalid model specified.")


def audit_file_4o(file_content, relevant_knowledge):
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
            {
                "role": "user",
                "content": f"Relevant knowledge:\n{relevant_knowledge}\n\nFile content:\n{file_content}",
            },
        ],
        model="gpt-4o-2024-08-06",
        response_format=AuditResponse,
    )
    return chat_completion.choices[0].message.parsed


def audit_file_old_model(file_content, relevant_knowledge, model="gpt-3.5-turbo"):
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
            {
                "role": "user",
                "content": f"Relevant knowledge:\n{relevant_knowledge}\n\nFile content:\n{file_content}",
            },
        ],
        model=model,
        response_format={"type": "json_object"},
    )
    try:
        return json.loads(chat_completion.choices[0].message.content)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from GPT-3.5 Turbo model"}


def audit_file_claude(file_content, relevant_knowledge):
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
            {
                "role": "user",
                "content": f"Relevant knowledge:\n{relevant_knowledge}\n\nFile content:\n{file_content}",
            },
        ],
    )

    try:
        return json.loads(message.content[0].text)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from Claude model"}


def audit(files_content, model="gpt-4o", retriever=None):
    """
    Audit multiple files using the specified model and external knowledge.

    Args:
    files_content (dict): A dictionary where keys are file paths and values are file contents.
    model (str): The model to use for auditing (default: "gpt-4o").
    retriever (VectorStoreRetriever): The retriever object for the knowledge base.

    Returns:
    list: A list of audit results for files with vulnerabilities.

    Raises:
    ValueError: If an invalid model is specified or if the retriever is not provided.
    """
    if retriever is None:
        raise ValueError(
            "A retriever must be provided for the external knowledge base."
        )

    audit_result = []
    for filepath, content in files_content.items():
        chat_completion = audit_file_with_knowledge(content, model, retriever)

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
