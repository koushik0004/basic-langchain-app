from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Initialize the LLM
llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    temperature=0.3
)

# Define system prompt as a template
system_prompt = """You are a helpful assistant.
Your role is to answer questions clearly and concisely.
Always be friendly and respectful."""

# Create a chat prompt template combining system and user prompts
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{user_input}")
])

# Create the chain
chain = prompt_template | llm | StrOutputParser()

# Test the app
if __name__ == "__main__":
    print("Chat Assistant (type 'exit' or 'quit' to end)\n")
    while True:
        user_question = input("You: ")

        if user_question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if user_question.strip():
            result = chain.invoke({"user_input": user_question})
            print(f"Assistant: {result}\n")
