from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=1)]

@tools
def write_to_db(dat):
    """This is a function to output data to the datbase"""
    print('hw')
