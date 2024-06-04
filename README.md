# AI-Agent
This project features an AI-powered agent designed to read, understand, and generate code documentation.
Utilizing advanced language models and a robust query processing pipeline, this agent can:

* Parse and Index Documents: Reads and processes documents from a specified directory, including PDF files, and converts them into a searchable vector index using local embedding models.
* Answer API Documentation Queries: Provides detailed documentation about code APIs, making it easier to understand and utilize API functionalities.
* Generate and Describe Code: Generates code snippets based on user prompts and provides detailed descriptions and suggested filenames for the generated code.
* Handle Complex Queries: Uses a sophisticated ReActAgent framework to manage complex queries and integrate multiple tools for an enhanced response.
* Retry Mechanism for Robustness: Incorporates a retry mechanism to handle errors gracefully and ensure successful query processing.
* Save Generated Code: Automatically saves the generated code snippets to specified files, making it convenient to integrate the code into your projects.
  
# Key Technologies and Libraries
llama_index: Core functionalities including vector indexing, reading directories, and creating prompt templates.
llama_parse: Parsing document results into markdown format.
pydantic: Defining structured data models for clean and consistent output.
dotenv: Loading environment variables from a .env file for configuration.
os: Interacting with the operating system for file handling.
ast: Safely evaluating strings containing Python expressions.
