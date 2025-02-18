from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from vec_test import SciAgentVectoreStore
from typing import List, Dict

vector_store = SciAgentVectoreStore()
tools = [TavilySearchResults(max_results=1)]

@tool
def query_knowledge_base(query: str)->List[Dict[str, str]]:
    """
    Looks up information in a knowledge base to help with answering customer questions and getting
    information on business processes.

    Args:
        query (str): Question to ask the knowledge base

    Return:
        List[Dict[str, str]]: Potentially relevant question and answer pairs from the knowledge base
    """
    return vector_store.query_faqs(query=query)

@tool 
def search_for_protocol(request: str):
    """
    Retrieve relevant SOPs based on the request from the user for a method or protocol. For example:
    "input: Fetch me the protocol for DNA extraction. Output: List of SOPs relevant to DNA extraction."

    Args:
        request(str): Request to put to the SOP vector store.

    Return:
        List[Dict[str]: Potentially relevant protocols from the SOP vector store

    """
    return vector_store.query_protocols(query=request)

@tool
def write_to_db(dat):
    """Use this to store user-provided data in the database."""
    return "data written"

@tool
def sample_requirements():
    """Use this to check that the user has entered all
     of the necessary detail for adding data to the 
     database."""
    return "sample requirements met"

@tool
def assign_unique_identifier():
    """Use this to look at the files stored in the database, 
    identify an available ID number, and assign that unique 
    identifier number to the data to be entered."""
    return "data assigned identifier X"

@tool
def match_test_results_to_a_sample_group():
    """Use this to match a test result to the sample group
     from which it originated or with which it is associated
     based on similar data elements such as:
     date of collection, location, disposition, or a unique identifier."""
    return "test result matched to parent sample."

@tool
def get_SOP():
    """Use this to fetch sop documents."""
    return "I get the sops"

@tool
def find_conc():
    """Use this to find the concentration of something"""
    return "I find the concentration of things"

@tool
def write_method():
    """Use this for writing an automation method"""
    return "I write methods."

@tool
def upload_samples():
    """Use this to upload samples"""
    return "I upload samples."

@tool
def order_supplies():
    """Use this to order supplies"""
    return "I order supplies."    
