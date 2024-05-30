import streamlit as st
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
# from dashboard import Dashboard_ #demo_dashboard
from dashboard import Dashboard

import gettext
_gettext = gettext.gettext

if 'CONVERSATION_HISTORY_SESSION_STATE' not in st.session_state:
    st.session_state['CONVERSATION_HISTORY_SESSION_STATE'] = []
    
if 'text_value' not in st.session_state:
    st.session_state.text_value = ''

if 'encoding_' not in st.session_state:
    st.session_state.encoding_ = True

if 'file_apth' not in st.session_state:
     st.session_state.file_apth = None

if 'uploaded_file' not in st.session_state:
     st.session_state.uploaded_file = None

# Page Configuraion
st.set_page_config(page_title=_gettext("Dcument RAG"),
                   layout="wide",
                    )

with open('css/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
dash = Dashboard()
dash.demo_dashboard(_gettext)