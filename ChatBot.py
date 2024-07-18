from langchain_community.vectorstores import FAISS # for the vectorization part
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from sentence_transformers import SentenceTransformer
import warnings
from urllib3.exceptions import InsecureRequestWarning
import streamlit as st
from dotenv import load_dotenv
from os import getenv
import shelve
from langchain.chains.question_answering import load_qa_chain
import config as config
from langchain_openai import ChatOpenAI

api_key = config.OPENAI_API_KEY

# Explicitly pass the API key when creating the OpenAI client instance
client = ChatOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
  model="mistralai/mistral-7b-instruct:free"
)


warnings.filterwarnings("ignore", category=InsecureRequestWarning)


load_dotenv()

st.title("FESTBOT")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"


# Initialize Sentence Transformer model
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

# Function to generate embeddings for input text
def embeddings(input):
    query_embedding = model.encode(input)
    return query_embedding
 


# TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(api_base="http://localhost:1234/v1")'
# openai.api_base="http://localhost:1234/v1"
# TODO: The 'openai.ap' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(ap="NULL")'
# openai.ap="NULL"


def db_output(prompt):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db3 = FAISS.load_local("./FESTBOT_db", embedding_function, allow_dangerous_deserialization=True)
    docs = db3.similarity_search(prompt)
    llm = client
    chain =load_qa_chain(llm=llm,chain_type="stuff")
    response =chain.run(input_documents=docs,question=prompt)
    return (response)

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])
    
# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages
    
# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()
if st.session_state.messages:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"{USER_AVATAR} User: {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"{BOT_AVATAR} Assistant: {message['content']}")

with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response=db_output(prompt)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_chat_history(st.session_state.messages)
