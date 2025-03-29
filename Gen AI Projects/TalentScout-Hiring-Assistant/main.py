import streamlit as st
import os
from dotenv import load_dotenv
import base64
from langchain.chat_models import ChatOpenAI
from langchain.schema import  HumanMessage
from langchain.prompts import ChatPromptTemplate
load_dotenv()
# Load API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

# Clear chat history on rerun if not explicitly retained
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "candidate_details" not in st.session_state:
    st.session_state.candidate_details = ""

def encrypt_data(data):
    """Basic encoding for sensitive data."""
    return base64.b64encode(data.encode()).decode()

def decrypt_data(data):
    """Basic decoding for sensitive data."""
    return base64.b64decode(data.encode()).decode()

def create_technical_questions(tech_stack):
    """Generate 3-5 technical questions based on the candidate's tech stack."""
    prompt = f"Generate 3-5 technical questions for evaluating expertise in: {tech_stack}."
    response = llm([HumanMessage(content=prompt)])
    return response.content

def chatbot_response(chat_history, candidate_details, user_message=None):
    """Generate responses while maintaining conversation context."""
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an AI hiring assistant, responsible for gathering candidate details and conducting technical assessments. Stay on-topic and professional."),
        ("human", "{candidate_details}"),
        ("human", "{chat_history}"),
        ("human", "{user_message}")
    ])
    
    formatted_chat_history = "\n".join([f"{role}: {message}" for role, message in chat_history])
    prompt = prompt_template.format(candidate_details=candidate_details, chat_history=formatted_chat_history, user_message=user_message or "")
    response = llm([HumanMessage(content=prompt)])
    
    if not response.content.strip():
        return "I'm sorry, I couldn't process your request. Please try again with relevant details."
    return response.content

# Streamlit UI
st.title("TalentScout Hiring Assistant")

# Welcome Message
st.write("Welcome to TalentScout! I will guide you through the screening process by collecting your details and evaluating your technical skills.")

# Exit Instructions
st.info("To exit the chat, simply type 'exit', 'quit', 'goodbye', or 'end'.")

# Sidebar for Candidate Information
st.sidebar.header("Candidate Information")
name = st.sidebar.text_input("Full Name")
email = encrypt_data(st.sidebar.text_input("Email"))
phone = encrypt_data(st.sidebar.text_input("Phone Number"))
experience = st.sidebar.slider("Years of Experience", 0, 20, 1)
position = st.sidebar.text_input("Desired Position(s)")
location = st.sidebar.text_input("Current Location")
tech_stack = st.sidebar.text_area("Enter your tech stack (e.g., Python, Django, React, AWS)")

if st.sidebar.button("Start Assessment"):
    st.session_state.chat_history = []  # Reset chat history when starting a new assessment
    st.session_state.candidate_details = (f"Candidate Details:\nName: {name}\nEmail: [PROTECTED]\nPhone: [PROTECTED]\nExperience: {experience} years\n"
                                          f"Position: {position}\nLocation: {location}\nTech Stack: {tech_stack}.")
    
    technical_questions = create_technical_questions(tech_stack)
    st.session_state.chat_history.insert(0, ("AI", "Here are some technical questions for you based on your tech stack:\n" + technical_questions))
    initial_response = chatbot_response(st.session_state.chat_history, st.session_state.candidate_details)
    st.session_state.chat_history.insert(0, ("AI", initial_response))

# Chatbot Interaction
st.subheader("Chat with the AI")
chat_input = st.chat_input("Type your message...")
if chat_input:
    if chat_input.lower() in ["exit", "quit", "goodbye", "end"]:
        st.session_state.chat_history.insert(0, ("AI", "Thank you for your time! We will review your responses and get back to you soon."))
        st.session_state.candidate_details = ""  # Clear candidate details after exit
    else:
        if "candidate_details" in st.session_state and st.session_state.candidate_details:
            ai_response = chatbot_response(st.session_state.chat_history, st.session_state.candidate_details, chat_input)
            st.session_state.chat_history.insert(0, ("User", chat_input))
            st.session_state.chat_history.insert(0, ("AI", ai_response))
        else:
            st.session_state.chat_history.insert(0, ("AI", "Please start the assessment first by entering your details."))

# Display Chat History
for role, message in reversed(st.session_state.get("chat_history", [])):
    with st.chat_message(role):
        st.write(message)
