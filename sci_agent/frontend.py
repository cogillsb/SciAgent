import streamlit as st
from utils import prompts
import mammoth

from bot import app
from langchain_core.messages import HumanMessage, AIMessage



st.set_page_config(layout='wide', page_title='Cedalab', page_icon="sci_agent\lion-head.ico")
if 'display' not in st.session_state:
    st.session_state['display'] = {'type':'image', 'content':"sci_agent\holder_img.png"}
if 'message_history' not in st.session_state:
    st.session_state.message_history = [AIMessage(content = prompts.cedalab_intro_prompt)]

team_col, display_col, chat_col = st.columns([1,4,2])

with team_col:  
   if st.button('Clear Chat'):
       st.session_state.message_history = []

with chat_col:
    user_input = st.chat_input("Type here...")
    
    if user_input:
        st.session_state.message_history.append(HumanMessage(content = user_input))

        response = app.invoke({
            'messages': st.session_state.message_history
        })

        st.session_state.message_history = response['messages']
    with st.container(height=570): 
        for i in range(len(st.session_state.message_history)-1, -1, -1):      
            this_message = st.session_state.message_history[i]
            if isinstance(this_message, AIMessage):
                message_box = st.chat_message('assistant')
            else:
                message_box = st.chat_message('user')
            message_box.markdown(this_message.content)

with display_col:
    if st.session_state['display']['type'] == 'image':
        st.image( st.session_state['display']['content'] )
    elif st.session_state['display']['type'] == 'markdown':
        with open(st.session_state['display']['content'], "r", encoding="utf-8") as f:
            markdown_text = f.read()
        with st.container(height=600):       
            st.markdown(markdown_text)





