# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

# Loads environment variables from the .env file.
# Example:
# GOOGLE_API_KEY=your_api_key
from dotenv import load_dotenv

# Provides the Gemini chat model that we will use.
from langchain_google_genai import ChatGoogleGenerativeAI

# Used to create structured prompts with variables
# such as {language} and {query}.
from langchain_core.prompts import ChatPromptTemplate

# Converts the LLM's AIMessage response into a plain Python string.
from langchain_core.output_parsers import StrOutputParser


# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

# load_dotenv() searches for a .env file and loads the
# environment variables into the current Python environment.
#
# It returns True if the .env file was found and loaded.
if load_dotenv():
    print(True)
else:
    print("NOT FOUND")


# ============================================================
# 3. CREATE THE OUTPUT PARSER
# ============================================================

# StrOutputParser extracts the actual text from the
# AIMessage returned by the LLM.
#
# Without the parser:
#     LLM → AIMessage
#
# With the parser:
#     LLM → AIMessage → String
formatted_output = StrOutputParser()


# ============================================================
# 4. CREATE / INITIALIZE THE LLM
# ============================================================

# Create an instance of Google's Gemini model.
#
# This object represents the LLM that will receive our
# formatted prompt and generate a response.
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

# ============================================================
# 5. CREATE THE PROMPT TEMPLATE
# ============================================================

# ChatPromptTemplate allows us to create a reusable prompt.
#
# {language} and {query} are placeholders.
# Their actual values will be provided when we call:
#
#     chain.invoke({...})
#
prompt = ChatPromptTemplate.from_messages([
    { "role": "system", "content": "You are translator which just translates into {language}, and dont respond to it."},
    { "role": "user", "content": "{query}"}
])


# ============================================================
# 6. CREATE THE LANGCHAIN EXECUTION CHAIN
# ============================================================

# The | operator connects the components together.
#
# Data flows from LEFT → RIGHT:
#
# Input
#   ↓
# Prompt
#   ↓
# Gemini LLM
#   ↓
# StrOutputParser
#   ↓
# Final String
#
# In other words:
#
# prompt → llm → parser
#
chain = prompt | llm | formatted_output


# ============================================================
# 7. EXECUTE THE CHAIN
# ============================================================

# Pass values for the placeholders in our prompt:
#
# {language} → Gujarati
# {query}    → "My name is Pankaj..."
#
# The chain will:
#
# 1. Fill the prompt with these values.
# 2. Send the resulting prompt to Gemini.
# 3. Parse Gemini's response into a plain string.
response = chain.invoke({
    "language": "Gujarati",
    "query": "My name is Pankaj and my brother name is Abhishek."
})


# ============================================================
# 8. DISPLAY THE FINAL RESPONSE
# ============================================================

# Print the final string returned by StrOutputParser.
print(response)

### Quick reference

# Keep this mental model in mind:

# ```text
#               chain
#                 │
#                 ▼
#         ┌───────────────┐
#         │     Prompt    │
#         │ {language}    │
#         │ {query}       │
#         └───────┬───────┘
#                 │
#                 ▼
#         ┌───────────────┐
#         │      LLM      │
#         │    Gemini     │
#         └───────┬───────┘
#                 │
#                 ▼
#         ┌───────────────┐
#         │ StrOutputParser│
#         └───────┬───────┘
#                 │
#                 ▼
#           Python String
# ```

# The most important line to remember is:

# ```python
# chain = prompt | llm | formatted_output
# ```

# Read it as:

# **"Create the prompt → send it to Gemini → convert Gemini's response into a string."**
