import streamlit as st
from utils import prompts



st.set_page_config(layout='wide', page_title='Cedalab', page_icon="sci_agent\lion-head.ico")

if 'message_history' not in st.session_state:
    st.session_state.message_history = [{'content':prompts.cedalab_intro_prompt, 'type':'assistant'}]

team_col, display_col, chat_col = st.columns([1,4,2])

with team_col:
   st.radio('Your team:', prompts.members)
   if st.button('Clear Chat'):
       st.session_state.message_history = []

with chat_col:
    user_input = st.chat_input("Type here...")

    if user_input:
        st.session_state.message_history.append({'content':user_input, 'type': 'user'})
    
    for i in range(len(st.session_state.message_history)-1, -1, -1):
      
        this_message = st.session_state.message_history[i]
        message_box = st.chat_message(this_message['type'])
        message_box.markdown(this_message['content'])

with display_col:
   
    #st.subheader("Display Window")       
    st.image("sci_agent\holder_img.png" )
