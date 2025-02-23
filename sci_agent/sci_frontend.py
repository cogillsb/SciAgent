import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from utils import sci_prompts
from super import agents
import json

#Set the session state
if 'display' not in st.session_state:
    st.session_state['display'] = {'type':'image', 'content':"sci_agent\images\holder_img.png"}
if 'message_history' not in st.session_state:
    st.session_state.message_history = [AIMessage(content = sci_prompts.cedalab_intro_prompt)]

#Set the page configuration
st.set_page_config(layout='wide', page_title='Cedalab', page_icon="sci_agent\images\lion-head.ico")
display_col, chat_col = st.columns([4,2])

#Chat column
with chat_col:
    user_input = st.chat_input("Type here...")

    #Invoke agent
    if user_input:
        st.session_state.message_history.append(HumanMessage(content = user_input))
        response = agents.invoke({
                  "messages": st.session_state.message_history
            })     
        
        #Update the session state
        st.session_state.message_history = response['messages']
        if 'data' in response.keys():
            for k, v in response['data'].items():
                if k in st.session_state.keys():
                    st.session_state[k] = v
    
    #Display chat
    with st.container(height=570): 
        for i in range(len(st.session_state.message_history)-1, -1, -1):      
            this_message = st.session_state.message_history[i]
            if isinstance(this_message, AIMessage):
                message_box = st.chat_message('assistant')
                if type(this_message.content) == list:
                    message_box.markdown(this_message.content[0]['text'])
                else:
                    message_box.markdown(this_message.content)                
               
            elif isinstance(this_message, HumanMessage):
                message_box = st.chat_message('user')
                message_box.markdown(this_message.content)


#Display column
with display_col:
   
    #Show image
    if st.session_state['display']['type'] == 'image':
        st.image( st.session_state['display']['content'])

    #Show document
    elif st.session_state['display']['type'] == 'markdown':
        with open(st.session_state['display']['content'], "r", encoding="utf-8") as f:
            markdown_text = f.read()     
        with st.container(height=625):          
            st.markdown(markdown_text) 
    
    #Show form
    elif st.session_state['display']['type'] =='sample_form':        
        #Get the fields
        with open(st.session_state['display']['content'], 'r') as f:
            fields = json.load(f)  
        with st.container(height=625): 
            #Populate the display window with elements
            with st.form(key='myform'):
                for i, field in enumerate(fields):
                    if field['type'] == 'text_input':
                        value = st.text_input(label=field['label'], key=f'input_{i}')
                    if field['type'] == 'number_input':
                        value = st.number_input(label=field['label'], key=f'input_{i}')
                    if field['type'] == 'date_input':
                        value = st.date_input(label=field['label'], key=f'input_{i}')
                    if field['type'] == 'selectbox':
                        value = st.selectbox(label=field['label'], options=field['options'], key=f'input_{i}')
                    if field['type'] == 'text_area':
                        value = st.text_area(field['label'], height=100, key=f'input_{i}')   
            
                submit_button = st.form_submit_button(label='Submit')
                if submit_button:
                    st.write(st.session_state["input_0"])  
            
                
                

