import streamlit as st
import time
from config.session_config import CONVERSATION_HISTORY_SESSION_STATE


user_emoji = "🙋‍♂️" #config_data["emojis"]["user_emoji"]
chatbot_emoji = "🤖" #config_data["emojis"]["chatbot_emoji"]


user_message_style = """
    background-color: #575757;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    display: flex;
    align-items: right;
    justify-content: flex-end;
    font-size: 18px; 
    color: white;
"""
##E5E8E8
chatbot_message_style = """
    background-color: #E5E8E8;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    display: flex;
    align-items: left;
    font-size: 18px; 
    color: black;
    justify-content: flex-start;
"""
summary_style = """
    background-color: #E5E8E8;
    text-align: left;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    display: flex;
    align-items: left;
    font-size: 18px; 
    color: black;
    justify-content: flex-start;
"""

def clear_conversation(_gettext):
    """Clear the conversation history."""
    button_name = _gettext("Clear conversation")
    if (
        
        st.button("🧹 "+ button_name, use_container_width=True)
        or "conversation_history" not in st.session_state
    ):
        st.session_state[CONVERSATION_HISTORY_SESSION_STATE]= []
        st.session_state.total_cost = 0
        st.session_state.text_value = ''



def display_ai_message(message):
    return st.markdown(
                f'<div style="{chatbot_message_style}">{chatbot_emoji} {message}</div>',
                unsafe_allow_html=True
                    )
    
def display_user_message(message, ui=None):
    if ui is not None:
        return ui.markdown(
                    f'<div style="{user_message_style}">{user_emoji} {message}</div>',
                    unsafe_allow_html=True
                        )
    return st.markdown(
            f'<div style="{user_message_style}">{user_emoji} {message}</div>',
            unsafe_allow_html=True
                )

def display_conversation(conversation_history:list):
    """Display the conversation history in reverse chronology."""

    for idx, item in enumerate(reversed(conversation_history)):
        # Display the messages on the frontend
        
        message = item.data["content"]
        
        if item.type == "ai":
            # display ai message
            display_ai_message(message)

        elif item.type == "human":
            display_user_message(message)
      
def display_streaming_summary(assistant_response: str):
    """    
    Arg:        
        assistant_reponse(str): langchain response
    """    
    message_placeholder = st.empty()
    full_response = ""
    for chunk in assistant_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(
            f'<div style="{chatbot_message_style}">{chatbot_emoji} {full_response}</div>',
            unsafe_allow_html=True
                )     
           