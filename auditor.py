import logging
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from audit_response import AuditResponse
from prompts import prompt_default, prompt_ollama
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


def audit_file_with_knowledge(file_content, provider, model, retriever):
    """
    Audit a file using the specified model and external knowledge.

    Args:
    file_content (str): The content of the file to be audited.
    provider (str): The provider to use for the model.
    model (str): The model to use for auditing.
    retriever (VectorStoreRetriever): The retriever object for the knowledge base.

    Returns:
    dict or AuditResponse: The parsed audit response from the model.
    """
    query = f"Audit this Rust code for security vulnerabilities:\n\n {file_content}"
    logging.debug(f"Generated query for knowledge retrieval: {query[:100]}...")

    relevant_knowledge = get_relevant_knowledge(query, retriever)
    logging.debug(f"Retrieved relevant knowledge: {len(relevant_knowledge)} characters")

    if provider == "openai":
        return audit_file_openai(file_content, relevant_knowledge, model)
    elif provider == "anthropic":
        return audit_file_anthropic(file_content, relevant_knowledge, model)
    elif provider == "ollama":
        return audit_file_ollama(file_content, relevant_knowledge, model)
    elif provider == "huggingface":
        return audit_file_huggingface(file_content, relevant_knowledge, model)
    else:
        logging.error(f"Invalid or unsupported provider specified: {provider}")
        raise ValueError("Invalid or unsupported provider specified.")


def audit_file_huggingface(
    file_content, relevant_knowledge, model="microsoft/Phi-3-mini-4k-instruct"
):
    """
    Audit a file using the model from Hugging Face.

    Args:
    file_content (str): The content of the file to be audited.
    relevant_knowledge (str): Relevant knowledge for the audit.
    model (str): The Hugging Face model ID to use.

    Returns:
    dict: The parsed JSON response from the model, or an error dictionary if parsing fails.
    """
    logging.warning(
        "HuggingFace integration is not yet functional due to missing structured output support"
    )

    # NOTE: This function is currently not functional as ChatHuggingFace does not support
    # the with_structured_output method in the current version of langchain.
    # TODO: Implement alternative structured output handling or wait for library update

    try:
        get_required_env_var("HUGGINGFACEHUB_API_TOKEN")

        llm = HuggingFaceEndpoint(
            repo_id=model,
            task="text-generation",
            max_new_tokens=4096,
            do_sample=False,
            repetition_penalty=1.03,
        )

        chat_model = ChatHuggingFace(llm=llm).with_structured_output(AuditResponse)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_default),
                (
                    "user",
                    "Relevant knowledge:\n{knowledge}\n\nFile content:\n{content}",
                ),
            ]
        )

        # Use pipe operator for cleaner chain composition
        chain = prompt | chat_model
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


def audit_file_openai(file_content, relevant_knowledge, model="gpt-4o"):
    """
    Audit a file using the OpenAI model.

    Args:
    file_content (str): The content of the file to be audited.
    relevant_knowledge (str): Relevant knowledge for the audit.
    model (str): The OpenAI model ID to use.

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
                ("system", prompt_default),
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


def audit_file_ollama(file_content, relevant_knowledge, model="llama3.2:3b"):
    """
    Audit a file using the OpenAI model.

    Args:
    file_content (str): The content of the file to be audited.
    relevant_knowledge (str): Relevant knowledge for the audit.
    model (str): The OpenAI model ID to use.

    Returns:
    AuditResponse: The parsed audit response from the GPT-4o model.
    """
    try:

        llm = ChatOllama(model=model, temperature=0).with_structured_output(
            AuditResponse
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_ollama),
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


def audit_file_anthropic(
    file_content, relevant_knowledge, model="claude-3-5-sonnet-latest"
):
    """
    Audit a file using the Claude 3.5 Sonnet model.

    Args:
    file_content (str): The content of the file to be audited.
    relevant_knowledge (str): Relevant knowledge for the audit.
    model (str): The Claude model ID to use.

    Returns:
    dict: The parsed JSON response from the Claude model, or an error dictionary if parsing fails.
    """

    try:
        api_key = get_required_env_var("ANTHROPIC_API_KEY")
        llm = ChatAnthropic(
            api_key=api_key, model=model, temperature=0
        ).with_structured_output(AuditResponse)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_default),
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


def audit(files_content, provider="openai", model="gpt-4o", retriever=None):
    """
    Audit multiple files using the specified model and external knowledge.

    Args:
    files_content (dict): A dictionary where keys are file paths and values are file contents.
    provider (str): The provider to use for the model (default: "openai").
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
        chat_completion = audit_file_with_knowledge(content, provider, model, retriever)

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
