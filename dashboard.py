import os
import streamlit as st 
from langchain.callbacks import get_openai_callback

from chat.chat_ui_utils import clear_conversation, display_conversation, display_user_message
from chat.chat_history_utils import add_to_session_chat_history
from model.insurance_faq_langchain_agent import setup_insurance_agent_llama
from config.session_config import CONVERSATION_HISTORY_SESSION_STATE
import base64
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@st.cache_data
def displayPDF(file,width=700,height=750):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width=100% height="{height}" style="padding: 10px; border: 3px solid #5e5eff;" type="application/pdf">'
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

class Dashboard:
    def __init__(self):
        self.insurance_agent = None

    def demo_dashboard(self,_gettext):
        """Demo Dashboard for Langchain Agent
        """
        if CONVERSATION_HISTORY_SESSION_STATE not in st.session_state:
            # create a new session state
            st.session_state[CONVERSATION_HISTORY_SESSION_STATE] = []

        st.success(_gettext("Experience our application with Llama 2 model."))
    
        with st.container():     
            # content_column, chatbot_column  =  st.columns((0.46,0.54))
            _,upload,_  =  st.columns((1,1,1))
            #--------content column------------------------- 
            # with content_column:
            with upload:
                st.session_state.uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
                if st.session_state.uploaded_file is not None:
                    st.session_state.file_apth = f"{os.getcwd()}/data/{st.session_state.uploaded_file.name}"

            document_column, chat_column  =  st.columns((0.46,0.54))
            with document_column:
                if st.session_state.uploaded_file is not None:
                    if st.session_state.encoding_ == True:
                        try:
                            with open(st.session_state.file_apth, "wb") as f:
                                f.write(st.session_state.uploaded_file.getvalue())
                            print("LLAMA 2 Model Activated")
                            self.insurance_agent=setup_insurance_agent_llama(st.session_state.file_apth)
                        except Exception as e:
                            log.error(f"OpenAI request failed with exception - {e}")                
                        st.session_state.encoding_ = False       
                st.markdown(f"<div class='section-headings'><b>Uploaded Document</b></div>", unsafe_allow_html=True)
                st.write('')
                try:
                    displayPDF(st.session_state.file_apth)
                except:
                    pass

            #--------Chatbot column-------------------------
            with chat_column:
                chat_heading = _gettext('Ask your Insurance Queries here!!')
                st.markdown(f"<div class='section-headings'><b>{chat_heading}</b></div>", unsafe_allow_html=True)
                st.write('')   

                clear_conversation(_gettext)

                def update():
                        st.session_state.text = st.session_state.text_value

                # User intput section
                with st.form(key='my_form', clear_on_submit=False):
                    input_text = st.text_area(_gettext('Try your questions for information from document.'), 
                                            value="", key='text_value', 
                                            help=_gettext('Ask Questions related to your document'))
                    submit = st.form_submit_button(label=_gettext('Click me to get Answer!!'), on_click=update)  
                
                if submit:
                    # st.session_state['first_submit_status'] = True
                    assistant_response = None
                    if input_text != '':
                        ui = st.empty()
                        display_user_message(input_text, ui)
                        # add user input to chat history
                        add_to_session_chat_history(chat_text= input_text,response_by='human')
                        
                        with st.spinner(_gettext('Generating your answer ✨')):
                            try:
                                with get_openai_callback() as total_cost:
                                    print('insurance_agent  -------- ', self.insurance_agent)
                                    assistant_response = self.insurance_agent({"query" : input_text})['result']
                                    assistant_response = assistant_response.replace('\n', ' ')
                                    print('-------------------------------------------Assistant Response-------------------------------')
                                    print(assistant_response)
                                    print('--------------------------------------------------------------------------------------')
                                response = {'message':assistant_response}
                                log.info(f"API usage cost - {total_cost} ")
                            except Exception as e:
                                log.error(f"OpenAI request failed with exception - {e}")
                                response = {'message':_gettext('Something went wrong! Not able to find anything OR there is a issue with API.')}
                        log.info(f"Generated answer - {response['message']}")
                        # add llm response to session chat history
                        add_to_session_chat_history(chat_text= response['message'],response_by='ai')
                        ui.empty()
                        display_conversation(st.session_state[CONVERSATION_HISTORY_SESSION_STATE])

        st.markdown("___")