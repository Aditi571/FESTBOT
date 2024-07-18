<h1>FestBot</h1> <br>
FestBot is a web application built on Streamlit that facilitates information extraction and retrieval based on PDF inputs related to festivals or organizations. The application utilizes Retrieval-Augmented Generation techniques and embeddings for efficient query handling.

<br><br/>
**Features**
- PDF Input Handling: Users can upload PDF files containing information about festivals or organizations.

- Chatbot Integration: A chatbot component processes user queries and retrieves relevant information from the pdf Input.

- Delete Chat History: Previous conversations with the ChatBot can be deleted.


**Workflow**
- Embeddings: Text from uploaded PDFs and user queries is converted into numerical representations called embeddings using natural language processing techniques.
- Vectorstore: These embeddings are stored in a FAISS vectorstore, optimized for fast similarity search.
- Similarity Search: When a user submits a query, FestBot retrieves embeddings of similar content from the vectorstore to generate relevant responses.
- Response Generation: Based on the closest embeddings found, FestBot presents information extracted from the PDFs as answers to the user's queries.<br></br>
  <img width="736" alt="Screenshot 2024-07-18 at 10 08 04 PM" src="https://github.com/user-attachments/assets/fd0b4175-0a92-4c89-b469-48fd8669033d">


**Technology Stack**
- Python: Programming language used for development.

- Streamlit: Framework used for building interactive web applications.

- Langchain: Library utilized for natural language processing tasks, including text extraction and embeddings generation.

<img width="1440" alt="Screenshot 2024-07-18 at 9 57 03 PM" src="https://github.com/user-attachments/assets/53f35065-9bf4-45c7-ac10-7c42f246e38b">


