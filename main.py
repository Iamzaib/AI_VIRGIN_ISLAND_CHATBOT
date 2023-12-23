import streamlit as st
import os
os.environ["OPENAI_API_KEY"] = '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'
os.environ['SERPAPI_API_KEY'] = '38b637beac69ac76de079b545abee733f09ea4dd5d474301293f1ff12e8663a8'

from langchain.chat_models import ChatOpenAI
from langchain.agents import  Tool
from langchain.agents import initialize_agent, AgentType
from langchain.utilities import SerpAPIWrapper

# Initialize Langchain components
llm = ChatOpenAI(model_name='gpt-3.5-turbo')
search = SerpAPIWrapper()

# Set up tools
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    Tool(
        name="Search_island",
        func=search.run,
        description="useful for when you need to answer questions about virgin island. You should ask targeted questions"
    )]

# Initialize Langchain agent
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

def get_bot_response(user_input, chatgpt_instructions):
    # Construct the chatgpt_instruction
    print(user_input)
    chatgpt_instruction = f'You have to follow these instructions.\n {chatgpt_instructions}\nInput:{user_input}'

    # Call Langchain to get the bot response
    bot_response = agent.run(chatgpt_instruction)
    return bot_response

# Streamlit configuration
st.set_page_config(page_title="DOCAI", page_icon="🤖", layout="wide")

st.title("Virgins Island Bot 🤖 ")

chatgpt_instructions = "###Instrcution:You are a helpful assistant who only answers Virgin Islands-related questions. Do not answer general AI questions. Your response must be helpful."

# Add selectable question options
selected_question = st.radio("Select a question:", [
    "Best places to visit in Virgin Islands",
    "How to Spend your day exploring the British Virgin Islands",
    "Best hotels to stay in Virgin Islands",
    "Things to do at Virgin Islands",
])

with st.form("bot_form"):
    user_input = st.text_input("Enter prompt:", key="user_input")

    submit_button = st.form_submit_button("Submit")

bot_response_container = st.empty()

if submit_button:
    with st.spinner("Processing..."):
        # Use the selected question as part of the user input
        if user_input=="":
            user_input = f"{selected_question}"
        bot_response = get_bot_response(user_input, chatgpt_instructions)
        st.success(bot_response)
