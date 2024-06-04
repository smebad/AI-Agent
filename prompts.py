context = """Purpose: The primary role of this agents is to assist users by analyzing code. It should be able to generate
code and answer questions related to that code. The primary purpose of this agent is to help users understand. """

code_parser_template = """ Parse the response from a previous LLM into a description and a string of valid code, also come up with a valid file name this could be saved as that doesnt contain special characters.
Here is the response: {response}. You should parse this in the following JSON Format:"""