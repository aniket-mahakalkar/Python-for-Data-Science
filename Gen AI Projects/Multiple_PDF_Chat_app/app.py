import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.llms import Ollama
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceHub
# from langchain.chains import conversational_retrieval_chain
from langchain.chains import ConversationalRetrievalChain

import os
from htmlTemplates import css, bot_template, user_template


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001" , google_api_key=GOOGLE_API_KEY)


def get_pdf_text(pdf_docs):

    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()

    return text

def get_text_chunk(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len)
    

    chunks = text_splitter.split_text(text)

    return chunks


def get_vector_store(text_chunks):

    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # embeddings = embedding_model.embed_documents(text_chunks)
    vector_store = FAISS.from_texts(text_chunks, embedding_model)

    return vector_store


def get_conversation_chain(vectorstore):
    # Use Ollama to load the locally installed DeepSeek model
    llm = Ollama(model="deepseek-r1")

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    
    response = st.session_state.conversation({'question': user_question})
    
    st.session_state.chat_history = response['chat_history']

    for i, messsage in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", messsage.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", messsage.content), unsafe_allow_html=True)

    # st.write(user_template.replace("{{MSG}}", user_question))
    # st.write(bot_template.replace("{{MSG}}", response))

def main():
    
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDF's", page_icon=":shark:", layout="wide")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDF's")

    user_question = st.text_input("Ask a question about your document")

    if user_question:
        handle_userinput(user_question)

    st.write(user_template.replace("{{MSG}}", "Hello, Bot"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader(" Your Document")

        pdf_docs = st.file_uploader("Upload your Pdf", type=['pdf'],accept_multiple_files= True)
        if st.button("Process"):

            with st.spinner("Processing..."):
                
                #get pdf text

                raw_text = get_pdf_text(pdf_docs)


                # get the text chunks
                text_chunks = get_text_chunk(raw_text)

                # create vector store
                vectore_store = get_vector_store(text_chunks)

                #Create Conversation Chain

                st.session_state.conversation = get_conversation_chain(vectore_store)

                st.success("Processing Done")
                
                
if __name__ == '__main__':
    main()