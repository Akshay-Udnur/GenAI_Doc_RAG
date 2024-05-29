
import streamlit as st
from typing import Literal

from chat.chat_formats import Conversation, ConversationHistory

from config.session_config import CONVERSATION_HISTORY_SESSION_STATE



def get_session_chat_history()->ConversationHistory:
    """function to return the chat history stored in session state
    Format : Stored in compatible format required for backend api calls
    session state variable : 'converstaion_history'
    
    """
    if CONVERSATION_HISTORY_SESSION_STATE not in st.session_state:
        
        # create a new session state
        st.session_state[CONVERSATION_HISTORY_SESSION_STATE] = []
        
    else:
        chat_history = ConversationHistory(history=st.session_state[CONVERSATION_HISTORY_SESSION_STATE])
        #chat_history = {"history": st.session_state[CONVERSATION_HISTORY_SESSION_STATE]}
        
    return chat_history




def add_to_session_chat_history(chat_text:str, response_by:Literal['human', 'ai']):
    """function to add user/ai chat to streamlit session history

    Args:
        chat_text (str): text response from ai/human
        response_by (Literal[&#39;human&#39;, &#39;ai&#39;]): select the response type 
    """
   
    if CONVERSATION_HISTORY_SESSION_STATE not in st.session_state:
    
        # create a new session state
        st.session_state[CONVERSATION_HISTORY_SESSION_STATE] = []
        
       
    conversation = Conversation(type=response_by,data={'content':chat_text})
        
    # add the converstion
    st.session_state[CONVERSATION_HISTORY_SESSION_STATE].append(conversation)
                
        
        
        
        
        
        
      
        
#----------------old sample code-----------------------
def openai_llm_response(user_input):
    """Send the user input to the LLM API and return the response."""
    # Append user question to the conversation history
     
    st.session_state.conversation_history.append(
        {"type": "human", "data":{"content": user_input}}
    )
    payload = {"history": st.session_state.conversation_history}

    # Send the entire conversation history to the backend
    #st.write(payload)
    
    #response = requests.post(app_url, json=payload).json()
    response = {'message':'this is ai message place holder'}

    # Add the generated response and cost to the session state
    st.session_state.conversation_history.append({"type": "ai", "data":{"content": response['message']}})
    #st.session_state.total_cost += utils.calc_cost(response["token_usage"])