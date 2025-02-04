from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=1)]

@tools
def write_to_db(dat):
    """This is a function to output data to the datbase"""
    print('hw')

def ask_user_for_a_file():
    """This is a function to let the agent ask the user for a file"""
    return

def assign_unique_identifier():
    """This is a function to let the agent look at the files in storage,
    identify an available ID number,
    and tag the data to be entered"""

