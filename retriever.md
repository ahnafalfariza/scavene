# Retrieval Augmented Generation

## Overview

Scavene implements a Retrieval Augmented Generation (RAG) process to enhance the quality and accuracy of smart contract audits. This document explains the RAG process and how it fits into the overall audit workflow.

## Retrieval Augmented Generation (RAG)

RAG is a technique that combines the power of large language models with the ability to retrieve relevant information from an external knowledge base. In our case, this knowledge base consists of known vulnerabilities and best practices for Near smart contracts.

### The RAG Process

1. **Knowledge Base Creation**: We maintain a database of known vulnerabilities, security best practices, and common issues in Near smart contracts, integrated from [BlockSec's Rustle detector repository](https://github.com/blocksecteam/rustle?tab=readme-ov-file#detectors). This database is stored in [this file](/vulnerabilities/list_vulnerabilities.csv)

Sample of the knowledge base:

| Detector ID             | Description                                                                                 | Severity |
| ----------------------- | ------------------------------------------------------------------------------------------- | -------- |
| `Use of incorrect json type`     | Don't use type `i64`, `i128`, `u64`, or `u128` as the parameters or return values of public interfaces (public functions without `#[private]` macro in a `#[near_bindgen]` struct). This is because the largest integer that json can support is 2^53-1. Type `I64`, `I128`, `U64`, and `U128` in Near SDK are recommended for developers.	                 | High     |
| `Lack of check for self-transfer`  | Before transferring tokens to the receiver, the contract should check whether the receiver is the sender itself. Otherwise, attackers may mint infinite tokens by abusing this vulnerability.	 | High     |
| `Changes to collections are not saved`            | NEAR SDK provides some map collections which can store key-value mappings. You can use `get` to get a value by its key and insert or overwrite the value by calling `insert` with a specified key. The collections use borsh to serialize and deserialize, when you want to make some changes to a collection, you need to `get` an existing value and make changes to it, then `insert` it into the collection again. Without the `insert` function, the changes will not be saved to the contract.	     | High     |

For full list of vulnerabilities, please refer to [this file](/vulnerabilities/list_vulnerabilities.csv).

2. **Embedding**: The knowledge base entries are converted into vector embeddings using OpenAI's embedding model. These embeddings capture the semantic meaning of each entry

3. **Vector Store**: The embeddings are stored in a FAISS (Facebook AI Similarity Search) vector database

4. **Retrieval**: During the audit process, when analyzing a specific part of the smart contract, we perform a similarity search in the vector store to find the most relevant entries from our knowledge base

5. **Augmented Generation**: The retrieved information is then provided to the language model (e.g., GPT-4) along with the smart contract code being audited.

![RAG Process](/rag.png)

## The Audit Process

1. **File Reading**: The system reads all Rust files in the specified folder

2. **Initialization**: The RAG system is initialized, creating the vector store from the knowledge base

3. **Code Analysis**: For each function or code block in the smart contract:
   - The code is analyzed to determine its purpose and potential vulnerabilities
   - A similarity search is performed in the vector store to retrieve relevant known issues or best practices
   - The code, along with the retrieved information, is sent to the language model for analysis

4. **Report Generation**: The language model generates audit findings, taking into account both the code and the retrieved information

5. **Result Compilation**: All findings are compiled into a report

## Conclusion

The integration of Retrieval Augmented Generation into the Near Smart Contract Auditor enhances the audit process by combining the power of large language models with a curated knowledge base of smart contract security information. This approach leads to more accurate, consistent, and informative audit results, ultimately contributing to the development of more secure Near smart contracts.
