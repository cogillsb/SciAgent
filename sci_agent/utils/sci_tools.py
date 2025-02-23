import os
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

SAMPLE_FILE = "sci_agent\data\sample_form.json"
vector_store = SciAgentVectoreStore()

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
                                        'type':'sample_form',
                                        'content':SAMPLE_FILE
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

