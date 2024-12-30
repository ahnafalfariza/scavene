import os
import json
import anthropic
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from audit_response import AuditResponse
from prompts import prompt_4o, prompt_older_model
from utils import get_required_env_var


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
    query = (
        f"Audit this Rust code for security vulnerabilities: {file_content[:500]}..."
    )
    logging.debug(f"Generated query for knowledge retrieval: {query[:100]}...")

    relevant_knowledge = get_relevant_knowledge(query, retriever)
    logging.debug(f"Retrieved relevant knowledge: {len(relevant_knowledge)} characters")

    if model == "gpt-4o":
        return audit_file_openai(file_content, relevant_knowledge)
    elif model == "gpt-3.5-turbo":
        return audit_file_old_model(file_content, relevant_knowledge)
    elif model == "claude-3.5-sonnet":
        return audit_file_claude(file_content, relevant_knowledge)
    # elif model == "near-fine-tuned-4o":
    #     return audit_file_near_ecosystem(file_content, relevant_knowledge)
    else:
        logging.error(f"Invalid model specified: {model}")
        raise ValueError("Invalid model specified.")


def audit_file_openai(file_content, relevant_knowledge, model="gpt-4o"):
    """
    Audit a file using the OpenAI model.

    Args:
    file_content (str): The content of the file to be audited.

    Returns:
    AuditResponse: The parsed audit response from the GPT-4o model.
    """
    try:
        api_key = get_required_env_var("OPENAI_API_KEY")

        llm = ChatOpenAI(
            api_key=api_key, model=model, temperature=0
        ).with_structured_output(AuditResponse)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_4o),
                (
                    "user",
                    "Relevant knowledge:\n{knowledge}\n\nFile content:\n{content}",
                ),
            ]
        )

        # Use pipe operator for cleaner chain composition
        chain = prompt | llm
        output = chain.invoke(
            {"knowledge": relevant_knowledge, "content": file_content}
        )

        logging.info("Successfully completed audit")
        logging.debug(f"Audit response: {output}")

        return output

    except ValueError as e:
        logging.error(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Error during audit: {str(e)}")
        raise


def audit_file_old_model(file_content, relevant_knowledge, model="gpt-3.5-turbo"):
    """
    Audit a file using an older GPT model.

    Args:
    file_content (str): The content of the file to be audited.
    model (str): The model to use for auditing (default: "gpt-3.5-turbo").

    Returns:
    dict: The parsed JSON response from the model, or an error dictionary if parsing fails.
    """
    api_key = get_required_env_var("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=api_key)
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
    api_key = get_required_env_var("ANTHROPIC_API_KEY")
    anthropic_client = anthropic.Anthropic(api_key=api_key)
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


def audit_file_near_ecosystem(file_content, relevant_knowledge):
    """
    Audit a file using the ahnafalfariza/near-fine-tuned-4o model from Hugging Face.

    Args:
    file_content (str): The content of the file to be audited.
    relevant_knowledge (str): Relevant knowledge for the audit.

    Returns:
    dict: The parsed JSON response from the model, or an error dictionary if parsing fails.
    """

    # tokenizer = AutoTokenizer.from_pretrained("ahnafalfariza/near-fine-tuned-4o")
    # model = AutoModelForCausalLM.from_pretrained("ahnafalfariza/near-fine-tuned-4o")

    # prompt = f"Relevant knowledge:\n{relevant_knowledge}\n\nFile content:\n{file_content}\n\nAudit this code for security vulnerabilities and provide the result in JSON format."

    # inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    # outputs = model.generate(**inputs, max_length=2048, num_return_sequences=1)

    # response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # try:
    #     return json.loads(response)
    # except json.JSONDecodeError:
    #     return {"error": "Invalid JSON response from Near Ecosystem model"}


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
        logging.error("Retriever not provided for the external knowledge base")
        raise ValueError(
            "A retriever must be provided for the external knowledge base."
        )

    logging.info(f"Auditing files with model: {model}")

    audit_result = []
    for filepath, content in files_content.items():
        logging.info(f"Auditing file: {filepath}")
        chat_completion = audit_file_with_knowledge(content, model, retriever)

        if (
            isinstance(chat_completion, dict)
            and "vulnerabilities" in chat_completion
            and chat_completion["vulnerabilities"]
        ):
            logging.info(f"Vulnerabilities found in {filepath}")
            chat_completion["file_path"] = filepath
            audit_result.append(chat_completion)
        elif (
            hasattr(chat_completion, "vulnerabilities")
            and chat_completion.vulnerabilities != []
        ):
            logging.info(f"Vulnerabilities found in {filepath}")
            chat_completion.file_path = filepath
            audit_result.append(chat_completion)

    logging.info(f"Audit completed. Found vulnerabilities in {len(audit_result)} files")
    return audit_result


if __name__ == "__main__":
    audit()
