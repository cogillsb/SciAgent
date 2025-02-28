import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from utils import sci_prompts
from super import agents
import json, os
from interfaces import db_interface
import sqlite3
import pandas as pd
from utils.states import InputData
import pickle


def delete_files_in_directory(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        try:
            files = os.listdir(directory_path)
            for file in files:
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("All files deleted successfully.")
        except OSError:
            print("Error occurred while deleting files.")

#Set the session state
if 'display' not in st.session_state:
    st.session_state['display'] = {'type':'image', 'content':"sci_agent\images\holder_img.png", "submit": True}
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
        delete_files_in_directory("images/plotly_figures/pickle/")
        input_data_list = []
        for f in os.listdir("sci_agent/uploads/"):
            nm = f"{f.split('.')[0]}"
            path=f"sci_agent/uploads/{f}"
            if nm == "SampleGroups":
                des = "This is the sample information including where and when samples were collected. The rw_id is a foreign key for the Results data"
            elif nm=="Results":
                des = """This is results information. It includes data for the tests run and their cycle threshold values.
                It also includes the date of the analysis, and values for controling and normalizing the data. It also has a sample id key linking it to the Sample
                Groups data.
                """
            
            else:
                des = ""
           
            input_data_list.append(
                InputData(
                variable_name=nm, 
                data_path=path, 
                data_description=des)
            )
             
        st.session_state.message_history.append(HumanMessage(content = user_input))
        response = agents.invoke({
                  "messages": st.session_state.message_history,
                  "input_data": input_data_list
            })     
        
        #Update the session state
        st.session_state.message_history = response['messages']
        if 'data' in response.keys():
            for k, v in response['data'].items():
                if k in st.session_state.keys():
                    st.session_state[k] = v
        if os.listdir("images/plotly_figures/pickle/"):
            st.session_state['display']['type'] = 'graph'
            
    #Display chat
    with st.container(height=570): 
        for i in range(len(st.session_state.message_history)-1, -1, -1):      
            this_message = st.session_state.message_history[i]
            if isinstance(this_message, AIMessage):
                message_box = st.chat_message('assistant')
                if type(this_message.content) == list:
                    try:
                        message_box.markdown(this_message.content[0]['text'])
                    except:
                        print(this_message)
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
    
    #Show graph  
    if st.session_state['display']['type'] == 'graph':
        im_folder = "images/plotly_figures/pickle/"
        for image_path in os.listdir(im_folder):
            with open(f"{im_folder}{image_path}", "rb") as f:
                fig = pickle.load(f)
                st.plotly_chart(fig, use_container_width=True)

        st.image( st.session_state['display']['content'])
       
        
    #Show message
    if st.session_state['display']['type'] == 'message':
        st.write( st.session_state['display']['content'])
    
    #Show data
    if st.session_state['display']['type'] == 'data':   
        con = sqlite3.connect("sci_agent\data\databases\Sample.db")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for tb in [x[0] for x in cursor.fetchall()]:
            df = pd.read_sql_query(f"select * from {tb};", con)
            st.dataframe(df)
        con.close()
        
    if st.session_state['display']['type'] == 'message':
        st.write( st.session_state['display']['content'])
    

    #Show document
    elif st.session_state['display']['type'] == 'markdown':
        with open(st.session_state['display']['content'], "r", encoding="utf-8") as f:
            markdown_text = f.read()     
        with st.container(height=625):          
            st.markdown(markdown_text) 
    
    #Show form
    elif st.session_state['display']['type'] =='sample_form':        
        #Get the fields
        with open(st.session_state['display']['content']['sample_form'], 'r') as f:
            fields = json.load(f)  
        with st.container(height=625): 
            #Populate the display window with elements
            with st.form(key='myform'):             
                for field  in fields:
                    if field['type'] == 'text_input':
                        value = st.text_input(label=field['label'], key=field['key'])
                    if field['type'] == 'number':
                        value = st.number_input(label=field['label'], key=field['key'],  step=1, format="%d")
                    if field['type'] == 'date_input':
                        value = st.date_input(label=field['label'], key=field['key'])
                    if field['type'] == 'selectbox':
                        value = st.selectbox(label=field['label'], options=field['options'], key=field['key'])
                    if field['type'] == 'text_area':
                        value = st.text_area(field['label'], height=100, key=field['key'])   
                
               
                if 'validation' in st.session_state['display']['content'].keys():
                    st.write("Rules for  results upload:")
                    with open(st.session_state['display']['content']['validation'], 'r') as f:
                        rules = json.load(f)
                    for rule in rules:
                        st.write(f"- {rule['description']}")  

                #Only use when ready  
                if 'validation' in st.session_state['display']['content'].keys():            
                    uploaded_files = st.file_uploader("Upload results here", accept_multiple_files=True)
                else: 
                    uploaded_files = []
                submit_button = st.form_submit_button(label='submit')
                
                if submit_button:
                    if st.session_state['display']['submit']:                      
                        form_data = {field['key']: st.session_state[field['key']] for field in fields} 
                        
                        #run the checks
                        msgs = []
                        msgs += db_interface.check_form_entry(form_data)
                        if uploaded_files:
                            msgs += db_interface.file_check(uploaded_files)
                        if msgs:
                            for msg in msgs: 
                                st.markdown(f":red[**{msg}**]") 
                        else:
                            rw_id = db_interface.upload_sample_group(form_data)
                            if uploaded_files:
                                db_interface.upload_results(uploaded_files, rw_id)
                            st.session_state['display'] = {'type':'message', 'content':"Successfully Uploaded!", "submit": True} 
                            
                            #create tables in uploads
                            con = sqlite3.connect("sci_agent\data\databases\Sample.db")
                            cursor = con.cursor()
                            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                            for tb in [x[0] for x in cursor.fetchall()]:
                                df = pd.read_sql_query(f"select * from {tb};", con)
                                df.to_csv(f"sci_agent/uploads/{tb}.csv")
                            con.close()
                            
                            st.rerun()
                                                  
                    else:
                        st.write("Currently deactivated")
                
                
            
                
                

