from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=1)]

@tool
def write_to_db(dat):
    """This is a function to output data to the datbase"""
    print('hw')

@tool
def ask_user_for_a_file():
    """This is a function to let the agent ask the user for a file"""
    return

@tool
def assign_unique_identifier():
    """This is a function to let the agent look at the files in storage,
    identify an available ID number,
    and tag the data to be entered"""

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
    """Use this for writing ann automation method"""
    return "I write methods."

 @tool
def upload_samples():
    """Use this to upload samples"""
    return "I upload samples."

 @tool
def order_supplies():
    """Use this to order supplies"""
    return "I order supplies."



    
