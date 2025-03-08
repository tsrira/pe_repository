import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Sriram's Agile Bot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# User input prompt
user_input = st.chat_input("Ask about Agile and Agile Frameworks...")

# Function to check if input is Agile-related
def is_agile_related(text):
    agile_keywords = ["agile", "scrum", "kanban", "lean", "safe", "xp", "extreme programming", "sprint", "backlog", "retrospective"]
    return any(word in text.lower() for word in agile_keywords)

# Function to get OpenAI response with restriction
def get_response(prompt):
    restricted_prompt = (
        "You are an AI assistant that only answers questions related to Agile methodologies and Agile frameworks. "
        "If the user asks anything unrelated to Agile, Scrum, Kanban, SAFe, or Lean, politely refuse to answer and ask them to stay on topic.\n\n"
        f"User: {prompt}\n"
        "Assistant:"
    )

    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an Agile expert. Only answer Agile-related questions."}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": restricted_prompt}]
    )

    return response.choices[0].message.content

# Process input
if user_input:
    if is_agile_related(user_input):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        assistant_response = get_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
    else:
        with st.chat_message("assistant"):
            st.markdown("I only discuss Agile methodologies and frameworks. Please ask something Agile-related.")
