from langchain_anthropic import ChatAnthropic
from utils import sci_tools, sci_prompts, states
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import TypedDict, Literal
from langgraph.types import Command
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage

model  = ChatAnthropic(model="claude-3-5-sonnet-latest")

#Supervisor
class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal['sample manager', 'sop archivist', 'data analyst', 'FINISH']

def supervisor_node(state):    
    state['query'] = state["messages"][-1].content 
    chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', sci_prompts.supervisor_prompt),
        ('placeholder', "{messages}")
    ]
    )
    chain = chat_template | model.with_structured_output(Router)
    response = chain.invoke(state)
    goto = response["next"]
    if goto == "FINISH":
        goto = END
    return Command(goto=goto, update={"next": goto})

graph = StateGraph(states.SciState)
graph.add_node('supervisor', supervisor_node)


#SOP archivist
SOP_archivist_tools = [sci_tools.retrieve_protocols, sci_tools.analyze_relevance]

def SOP_archivist(state):          
    state['query'] = state["messages"][-1].content  
    chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', sci_prompts.SOP_archivist_prompt),
        ('placeholder', "{messages}")
    ]
    )
    chain = chat_template | model.bind_tools(SOP_archivist_tools)
    result = chain.invoke(state)   
    state['messages'].append(result)

    return state

def sop_archivist_conditional_edge(state):    
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'sop archivist tool node'
    else:
        return '__end__'
    
SOP_archivist_tool_node = ToolNode(SOP_archivist_tools)

graph.add_node('sop archivist', SOP_archivist)
graph.add_node('sop archivist tool node', SOP_archivist_tool_node)
graph.add_conditional_edges('sop archivist', sop_archivist_conditional_edge)
graph.add_edge('sop archivist tool node', 'sop archivist')


#sample manager
sample_manager_tools = [sci_tools.check_for_sample_form, sci_tools.check_for_test_result_form]

def sample_manager(state):  
    state['query'] = state["messages"][-1].content  
    chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', sci_prompts.sample_manager_prompt),
        ('placeholder', "{messages}")
    ]
    )
    chain = chat_template | model.bind_tools(sample_manager_tools)
    result = chain.invoke(state)   
    state['messages'].append(result)
    
    return state

def sample_manager_conditional_edge(state):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
       
        return 'sample manager tool node'
    else:
        return '__end__'

sample_manager_tool_node = ToolNode(sample_manager_tools)

graph.add_node('sample manager', sample_manager)
graph.add_node('sample manager tool node', sample_manager_tool_node)
graph.add_conditional_edges('sample manager', sample_manager_conditional_edge) 
graph.add_edge('sample manager tool node', 'sample manager')

#data analyst
data_analyst_tools = [sci_tools.data_importer, sci_tools.data_describer, sci_tools.data_exporter, sci_tools.data_visualizer]

def data_analyst(state):          
    state['query'] = state["messages"][-1].content  
    chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', sci_prompts.data_analyst_prompt),
        ('placeholder', "{messages}")
    ]
    )
    chain = chat_template | model.bind_tools(data_analyst_tools)
    result = chain.invoke(state)   
    state['messages'].append(result)

    return state

def data_analyst_conditional_edge(state):    
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'data analyst tool node'
    else:
        return '__end__'
    
data_analyst_tool_node = ToolNode(data_analyst_tools)

graph.add_node('data analyst', data_analyst)
graph.add_node('data analyst tool node', data_analyst_tool_node)
graph.add_conditional_edges('data analyst', data_analyst_conditional_edge)
graph.add_edge('data analyst tool node', 'data analyst')


#finish graph
graph.set_entry_point('supervisor')
agents = graph.compile()





