import streamlit as st
from PyPDF2 import PdfReader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma  # for the vectorization part
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Dummy user credentials
USER_CREDENTIALS = {
    "admin": "password123"
}

def login():
    st.title("Admin Login")
    with st.form("my_form"):
        st.write("Inside the form")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.form_submit_button('Submit my picks')


   
    if authenticate(username, password):
        st.success("Logged in successfully!")
        return True
    else:
        st.error("Invalid username or password.")
        return False

def authenticate(username, password):
    """Check if the provided username and password match the stored credentials."""
    return USER_CREDENTIALS.get(username) == password

def main():
    #if login():
        pdf = st.file_uploader("Upload your pdf", type='pdf', key="pdf_uploader")
        
        if pdf is not None:
            loader = PdfReader(pdf)
            text = ""
            for page in loader.pages:
                text += page.extract_text()
            

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_text(text=text)

            model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            db = Chroma.from_texts(splits, model, persist_directory="./FESTBOT_db")

            query = "What is ignus"
            docs = db.similarity_search(query)
            st.write(docs[0].page_content)
        

if __name__ == '__main__':
    main()
