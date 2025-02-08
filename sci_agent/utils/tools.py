from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

tools = [TavilySearchResults(max_results=1)]

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
