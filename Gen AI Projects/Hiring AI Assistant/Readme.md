# TalentScout Hiring Assistant

## Project Overview
TalentScout Hiring Assistant is an AI-powered chatbot designed to assist in the initial screening of candidates for technology-related roles. This chatbot gathers essential information from candidates, asks technical questions based on their tech stack, and ensures a smooth conversational experience. It utilizes **LangChain** for natural language processing and **Streamlit** for a user-friendly interface.

## Installation Instructions
Follow these steps to set up and run the application locally:

### Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/TalentScout-Hiring-Assistant.git
cd TalentScout-Hiring-Assistant
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key for OpenAI
Create a **.env** file in the root directory and add your OpenAI API key:
```plaintext
OPENAI_API_KEY=your_api_key_here
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

## Usage Guide
1. Enter your details in the sidebar (Name, Email, Experience, Tech Stack, etc.).
2. Click **Start Assessment** to generate technical questions based on your tech stack.
3. Use the chatbox to answer questions or ask queries.
4. Type **exit**, **quit**, **goodbye**, or **end** to terminate the chat session.

## Technical Details
- **Frontend**: Streamlit (for UI and chat interface)
- **Backend**: LangChain (for conversational AI and prompt management)
- **API**: OpenAI (for generating responses and technical questions)
- **Security**: Sensitive candidate details (email, phone) are encoded before storage

## Prompt Design
To ensure relevant responses and coherent conversations, the chatbot uses **LangChain's ChatPromptTemplate**, which:
- Greets candidates and explains its purpose.
- Asks structured questions to collect essential details.
- Generates **3-5 technical questions** tailored to the declared tech stack.
- Maintains context and ensures meaningful responses.
- Implements a fallback mechanism for unexpected inputs.

## Challenges & Solutions
### 1. **Context Handling in Conversations**
- **Issue**: Ensuring a continuous and relevant conversation while maintaining user data.
- **Solution**: Used **session state management** in Streamlit to retain chat history and candidate details.

### 2. **Technical Question Generation**
- **Issue**: Generating relevant technical questions based on different tech stacks.
- **Solution**: Used OpenAI's LLM with a structured prompt to generate **3-5 questions dynamically**.

### 3. **Chat History Display & Reset**
- **Issue**: Old chat history persisted even after restarting the app.
- **Solution**: Implemented a **reset mechanism** when a new assessment begins.

### 4. **Security of Sensitive Information**
- **Issue**: Candidate emails and phone numbers should not be stored in plaintext.
- **Solution**: Used **Base64 encoding** before storing sensitive information.


