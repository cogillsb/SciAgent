import os, json
from langchain_core.tools import tool
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from typing_extensions import Annotated
from langchain_core.tools.base import InjectedToolCallId
from langgraph.prebuilt import InjectedState
from utils.vec_test import SciAgentVectoreStore
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from utils import sci_prompts
from langchain_core.output_parsers import  PydanticOutputParser
from utils import states
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
import traceback
import sqlite3
from langchain_experimental.utilities import PythonREPL
import pandas as pd
from io import StringIO
import sys
import markdown
import tempfile
import webbrowser


SAMPLE_FILE = "sci_agent\data\sample_form.json"
VALIDATION_FILE = "sci_agent\data\\validation.json"
EXAMPLE_FORM = "sci_agent\data\exmple_form.json"
EXAMPLE_VALIDATION = "sci_agent\data\exmple_validation.json"
TEST_RESULT_FILE = "sci_agent\data\test_result_form.json"
vector_store = SciAgentVectoreStore()


@tool 
def update_submission(state: Annotated[dict, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Use this function after the user has approved the sample form and rules to save changes."""
    print("In update submission")
    try:
        #Read in the fields
        with open(EXAMPLE_FORM, 'r') as f:
                fields = json.load(f) 
        
        
        if os.path.exists(SAMPLE_FILE):
            os.remove(SAMPLE_FILE)
        os.rename(EXAMPLE_FORM, SAMPLE_FILE)

        if os.path.exists(VALIDATION_FILE):
            os.remove(VALIDATION_FILE)
        os.rename(EXAMPLE_VALIDATION, VALIDATION_FILE)
        
        
        #create a table in db
        # Establish connection to SQLite database
        con = sqlite3.connect("sci_agent\data\databases\Sample.db")
        cursor = con.cursor()
        cursor.execute("DROP TABLE IF EXISTS SampleGroups")
        cursor.execute("DROP TABLE IF EXISTS Results")

 

        #Convert streamlit fields to sql readables
        form_to_sql = {
                'text_input' : 'TEXT',
                'number': 'INTEGER',
                'date_input': 'DATE',
                'selectbox': 'TEXT', 
                'text_area': 'TEXT'
            }

        sql_fields_add = []
        for f in fields:
            sql_fields_add.append(f"{f['key']} {form_to_sql[f['type']]}")
        sql_fields_add = ", \n".join(sql_fields_add)    
        sql_tbl_build = f"""
        CREATE TABLE IF NOT EXISTS SampleGroups ({sql_fields_add});
        """
        cursor.execute(sql_tbl_build)
        con.commit()
        con.close()
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
    
    

    return Command(
        update={
            "data": {
                'display':
                    {
                        'submit': True,
                        'type': 'sample_form',
                        'content': 
                            {
                                'sample_form': SAMPLE_FILE,
                                'validation': VALIDATION_FILE
                            }
                    }
            },          
            "messages": [ToolMessage(content="The sample form has been updated..", tool_call_id=tool_call_id)]
        }
    )

@tool
def generate_sample_json(state: Annotated[dict, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Generate json based on the form description"""
    print('in sample form generator')
 
    model = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0)

    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            form_description = msg.content
            break


    prompt = PromptTemplate(
        input_variables=["form_description"],
        template=sci_prompts.sample_form_generator
    )
    chain = prompt | model
    result = chain.invoke({"form_description": form_description})

    with open(EXAMPLE_FORM, 'w') as json_file:
        json.dump(json.loads(result.content), json_file, indent=4)

    return Command(
        update={
            "data": {
                'display':
                    {
                        'submit': False,
                        'type': 'sample_form',
                        'content': 
                            {
                                'sample_form': EXAMPLE_FORM
                            }
                    }
            },          
            "messages": [ToolMessage(content="The form description has been translated to json.", tool_call_id=tool_call_id)]
        }
    )

@tool
def generate_validation_json(state: Annotated[dict, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Use this tool after the user has entered in a description for the validation of csv files.
    This function generates a validation rule json """
    print('in validation generator')
    try:
        model = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0)

        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                validation_description = msg.content
                break

        prompt = PromptTemplate(
            input_variables=["validation_description"],
            template=sci_prompts.sample_validation_generator
        )
        chain = prompt | model
        result = chain.invoke({"validation_description": validation_description})
     
        with open(EXAMPLE_VALIDATION, 'w') as json_file:
            json.dump(json.loads(result.content), json_file, indent=4)
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
    

    return Command(
        update={
            "data": {
                'display':
                    {
                        'submit': False,
                        'type': 'sample_form',
                        'content': 
                            {
                                'sample_form': EXAMPLE_FORM,
                                'validation': EXAMPLE_VALIDATION
                            }
                    }
            },          
            "messages": [ToolMessage(content="The validation rules have been set. Now showing the sample form.", tool_call_id=tool_call_id)]
        })

@tool
def check_for_sample_form(tool_call_id: Annotated[str, InjectedToolCallId]):
    """
    When a user wants to check in a sample group, use this method to check if there is an existing sample form.
    """   

    if  os.path.exists(SAMPLE_FILE):
        return Command(
            update={
                "data": {
                            'display':
                                {
                                    'submit': True,
                                    'type':'sample_form',
                                    'content':
                                        {
                                            'sample_form': SAMPLE_FILE,
                                            'validation': VALIDATION_FILE
                                        }
                            },
                },          
                "messages": [ToolMessage(content="The form exists and now displaying the form", tool_call_id=tool_call_id)]
            }
        )
    
@tool
def check_for_test_result_form(tool_call_id: Annotated[str, InjectedToolCallId]):
    """
    When a user wants to check in a test result, use this method to check if there is an existing test result form.
    """   

    if  os.path.exists(TEST_RESULT_FILE):
        return Command(
            update={
                "data": {
                                'display':
                                    {
                                        'type':'test_result_form',
                                        'content':TEST_RESULT_FILE
                                    }
                                },          
                "messages": [ToolMessage(content="The form exists and now displaying the form", tool_call_id=tool_call_id)]
            }
        )
    
@tool
def retrieve_protocols(state: Annotated[dict, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Node for finding protocols in a vector store."""  
    documents = vector_store.query_protocols(query=state['query'])
       
    return Command(
                update={
                    "documents": documents,          
                    "messages": [ToolMessage(content="I have found matching documents in the vector store", tool_call_id=tool_call_id)]
                }
    )

@tool
def analyze_relevance(state: Annotated[dict, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Analyze the relevance of retrieved documents to the query."""
    
    model = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0)
    documents = state['documents']

    prompt = PromptTemplate(
        input_variables=["query", "documents"],
        template=sci_prompts.protocol_relevance_prompt
    )
        
    parser = PydanticOutputParser(pydantic_object=states.RelevanceAnalysis)
    chain = prompt | model | parser

    #Compile chunks into string for model
    def convert_docstring(documents):
        """Function for converting a returned query into a docstring"""
        docs = {}   
        for i, doc in enumerate(documents['documents'][0]):        
            key = documents['ids'][0][i].rsplit('_', 1)[0]
            if key in docs.keys():
                docs[key].append(doc)
            else:
                docs[key] = [doc]
        docstring = ""
        i = 0
        for k, v in docs.items():
            docstring += f" Document {i}:\n{k}\n{';'.join(v)}\n\n"   
            i+=1 

        return docstring
    
    result = chain.invoke({
        "query": state['query'],
        "documents": convert_docstring(documents) 
    })
        
    idx = int(result.best_document_index)
    path = documents['metadatas'][0][idx]['path']
    
    #print out
    #Open the file
    with open(path, "r", encoding="utf-8") as f:
        md_content = f.read()
 
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)
    

    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=True, encoding="utf-8") as temp_file:
        temp_file.write(html_content)
        temp_filepath = f"sci_agent\cache\{temp_file.name}"
        
    # Specify the path to the Chrome executable
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

    # Create a Chrome browser controller
    chrome_browser = webbrowser.get(chrome_path)

    # Open the HTML file in the default web browser
    #webbrowser.open_new_tab(f"file://{temp_filepath}")
    set_path = "file:///C:/Users/grace/Documents/biz/cedalion/sci_agent/cache/temp.html"
    chrome_browser.open_new_tab(set_path)

    return Command(      
        update={
                "data": {
                    'display':
                        {
                            'type':'markdown',
                            'content': path
                        }, 
                    'protocol_path': path
                    },          
                "messages": [ToolMessage(content="The relevant document was found.", tool_call_id=tool_call_id)]
            }
    )

@tool 
def data_importer(state: Annotated[dict, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Node for importing samples or tests from vector store database."""  
    database = vector_store.query_database(query=state['query'])
       
    return Command(
                update={
                    "database": database,          
                    "messages": [ToolMessage(content="I have found matching data in the database", tool_call_id=tool_call_id)]
                }
    )

@tool 
def data_describer(state: Annotated[dict, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Node for describing data."""  
    return()

@tool     
def data_exporter(state: Annotated[dict, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Node for exporting data into a convenient format."""  
    return()

@tool 
def data_visualizer(state: Annotated[dict, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Node for visualizing raw or processed data."""  
    return()

@tool 
def show_data(state: Annotated[dict, InjectedState]):
    """Use this function to display the data in the database."""  
    print("in show data")
    return Command(
                update={
                    "data": {
                    'display':
                        {
                            'type':'data',
                            'content': "sci_agent\data\databases\Sample.db"
                        }, 
                    },        
                    "messages": [AIMessage(content="Now showing data")]
                }
    )
    
repl = PythonREPL()

persistent_vars = {}
plotly_saving_code = """import pickle
import uuid
import plotly

for figure in plotly_figures:
    pickle_filename = f"images/plotly_figures/pickle/{uuid.uuid4()}.pickle"
    with open(pickle_filename, 'wb') as f:
        pickle.dump(figure, f)
"""

@tool(parse_docstring=True)
def complete_python_task(state: Annotated[dict, InjectedState], thought: str, python_code: str):
    """Completes a python task

    Args:
        thought: Internal thought about the next action to be taken, and the reasoning behind it. This should be formatted in MARKDOWN and be high quality.
        python_code: Python code to be executed to perform analyses, create a new dataset or create a visualization.
    """
    print('in complete python')
    if "current_variables" in state:
        current_variables = state["current_variables"]
    else:
        current_variables = {}
    
    for input_dataset in state["input_data"]:        
        if input_dataset.variable_name not in current_variables:
            current_variables[input_dataset.variable_name] = pd.read_csv(input_dataset.data_path)
        
    if not os.path.exists("images/plotly_figures/pickle"):
        os.makedirs("images/plotly_figures/pickle")

    current_image_pickle_files = os.listdir("images/plotly_figures/pickle")
    
    try:
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Execute the code and capture the result
        exec_globals = globals().copy()
        exec_globals.update(persistent_vars)
        exec_globals.update(current_variables)
        exec_globals.update({"plotly_figures": []})


        exec(python_code, exec_globals)
        persistent_vars.update({k: v for k, v in exec_globals.items() if k not in globals()})

        # Get the captured stdout
        output = sys.stdout.getvalue()

        # Restore stdout
        sys.stdout = old_stdout

        updated_state = {
            "intermediate_outputs": [{"thought": thought, "code": python_code, "output": output}],
            "current_variables": persistent_vars
        }

        if 'plotly_figures' in exec_globals:
            exec(plotly_saving_code, exec_globals)
            # Check if any images were created
            new_image_folder_contents = os.listdir("images/plotly_figures/pickle")
            new_image_files = [file for file in new_image_folder_contents if file not in current_image_pickle_files]
            if new_image_files:
                updated_state["output_image_paths"] = new_image_files
                updated_state["display"] = {"type": "graph", "content": "figs"}                
            persistent_vars["plotly_figures"] = []
       
        return output, updated_state   
    
    
  
    except Exception as e:
        return str(e), {"intermediate_outputs": [{"thought": thought, "code": python_code, "output": str(e)}]}
