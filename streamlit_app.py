import openai
import streamlit as st

# Initialize OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set app title
st.title("Agile Frameworks")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
user_input = st.chat_input("Ask about Agile Frameworks...")

# Define restricted topics (negative prompt filtering)
restricted_keywords = [
    "politics", "sports", "movies", "technology", "history", "science", 
    "celebrities", "finance", "medical", "gaming", "entertainment"
]

def is_off_topic(user_input):
    """Check if user input contains restricted topics."""
    return any(word in user_input.lower() for word in restricted_keywords)

# Function to get OpenAI response with Agile restriction
def get_response(messages):
    system_message = {
        "role": "system",
        "content": (
            "You are an expert on Agile methodologies and Agile Frameworks. "
            "You can only answer questions related to Agile, Scrum, Kanban, SAFe, and similar frameworks. "
            "If a user asks about unrelated topics, politely decline to answer."
        )
    }

    messages_with_system = [system_message] + messages  

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_with_system
    )
    return response["choices"][0]["message"]["content"]

# Process user input
if user_input:
    if is_off_topic(user_input):
        st.warning("⚠️ This chatbot only answers questions about Agile Frameworks. Please ask relevant questions.")
    else:
        # Store and display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get response from OpenAI
        response = get_response(st.session_state.messages)

        # Store and display assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)
