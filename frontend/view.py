import requests
import streamlit as st

def send_message_to_chatbot(message):
    response = requests.post('http://127.0.0.1:8000/chatbot', json={"message": message})
    return response.json()
    
# Set page config
st.set_page_config(page_title="Calendly ChatBot", page_icon="📅")

st.title("Calendly Chatbot")

# Initialize conversation history in Streamlit session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

user_input = st.text_input("You:")

if st.button("Send"):
    response = send_message_to_chatbot(user_input)
    bot_response = response['response']['content']
    st.session_state.conversation_history.append({"user": user_input, "bot": bot_response})

if st.button("Clear Conversation"):
    st.session_state.conversation_history = []

# Display conversation history
st.text_area("Conversation History:", "\n".join([f"You: {item['user']}\nBot: {item['bot']}\n" for item in st.session_state.conversation_history]), height=800)


