# Import necessary modules and classes from llama_index, llama_parse, and pydantic libraries
# llama_index.llms.ollama - for handling language model instances
from llama_index.llms.ollama import Ollama

# llama_parse - for parsing document results
from llama_parse import LlamaParse

# llama_index.core - for core functionalities like vector indexing and reading directories
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate

# llama_index.core.embeddings - for resolving embedding models
from llama_index.core.embeddings import resolve_embed_model

# llama_index.core.tools - for creating query engine tools and their metadata
from llama_index.core.tools import QueryEngineTool, ToolMetadata

# llama_index.core.agent - for creating agents to handle complex queries
from llama_index.core.agent import ReActAgent

# pydantic - for defining structured data models
from pydantic import BaseModel

# llama_index.core.output_parsers - for parsing the output based on a Pydantic model
from llama_index.core.output_parsers import PydanticOutputParser

# llama_index.core.query_pipeline - for setting up a pipeline to handle query processing
from llama_index.core.query_pipeline import QueryPipeline

# Custom prompts and templates for context and code parsing
from prompts import context, code_parser_template

# Custom code reader tool
from code_reader import code_reader

# dotenv - for loading environment variables from a .env file
from dotenv import load_dotenv

# os - for interacting with the operating system, e.g., file handling
import os

# ast - for safely evaluating strings containing Python expressions
import ast

# First we wikk load environment variables from a .env file
load_dotenv()

# Initialize the Ollama LLM (Language Model) with the "mistral" model and set a request timeout, we cant put 3600 for the timeout as well if your machine doesnt work as it will take around 10 mins to finish.
llm = Ollama(model="mistral", request_timeout=30.0)

# Initialize a parser to convert results to markdown format
parser = LlamaParse(result_type="markdown")

# Set up a file extractor to use the parser for .pdf files and read documents from the ./data directory
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()

# Resolve the embedding model for local embeddings and create a VectorStoreIndex from the documents
embed_model = resolve_embed_model("local:BAAI/bge-m3")
vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

# Create a query engine from the vector index using the previously initialized LLM
query_engine = vector_index.as_query_engine(llm=llm)

# Define a set of tools for the ReActAgent, including the query engine and a code reader
tools = {
    QueryEngineTool(
      query_engine=query_engine,
      metadata=ToolMetadata(
        name="api_documentation",
        description="This gives documentation about code for an API. Use this for reading API documentation."
      ),
    ),
    code_reader,
}

# Initialize another Ollama model specifically for code-related tasks
code_llm = Ollama(model="codellama")

# Create a ReActAgent with the defined tools, using the code-specific LLM and setting verbosity and context
agent = ReActAgent.from_tools(tools, llm=code_llm, verbose=True, context="context")

# Define a Pydantic model for the output schema
class CodeOutput(BaseModel):
  code : str
  description : str
  filename : str

# Create an output parser using the Pydantic model
parser = PydanticOutputParser(CodeOutput)

# Format the code parser template with the output parser
json_prompt_str = parser.format(code_parser_template)
json_prompt_tmpl = PromptTemplate(json_prompt_str)

# Define a query pipeline with the JSON prompt template and the LLM
output_pipeline = QueryPipeline(chain = [json_prompt_tmpl, llm])

# Main loop to continuously prompt the user for input
while (prompt := input("Enter a prompt (q to quit): ")) != "q":
  retries = 0

# Retry mechanism for processing the prompt
  while retries < 3:
    try:
        # Query the agent with the user prompt
        result = agent.query(prompt)

        # Run the output pipeline with the agent's response
        next_result = output_pipeline.run(response = result)

        # Clean the JSON output by removing "assistant:" prefix
        cleaned_json = ast.literal_eval(next_result).replace("assistant:", "")
    except Exception as e:
       retries += 1
       print(f"Error occured, retry #{retries}:", e)

# If maximum retries reached, inform the user and continue to the next iteration
  if retries >= 3:
    print("Unable to process request, try again")
    continue

# Print the generated code and its description
  print('Code generated')
  print(cleaned_json["code"])
  print("\n\nDescritpion:", cleaned_json["description"])

 # Retrieve the filename from the cleaned JSON
  filename = cleaned_json["filename"]

# Attempt to save the generated code to the specified file
  try:
    with open(os.path.join("output", filename), "w") as f:
      f.write(cleaned_json["code"])
    print("Saved file", filename)
  except:
    print("Unable to save file")