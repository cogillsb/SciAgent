from langchain_anthropic import ChatAnthropic
from utils import sci_tools, sci_prompts, states
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import TypedDict, Literal
from langgraph.types import Command
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import ToolInvocation, ToolExecutor

model  = ChatAnthropic(model="claude-3-5-sonnet-latest")
data_analyst_tools = [sci_tools.complete_python_task]
tool_executor = ToolExecutor(data_analyst_tools)
def call_tools(state):
    last_message = state["messages"][-1]
    tool_invocations = []
    if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls'):
        tool_invocations = [
            ToolInvocation(
                tool=tool_call["name"],
                tool_input={**tool_call["args"], "state": state}
            ) for tool_call in last_message.tool_calls
        ]

    responses = tool_executor.batch(tool_invocations, return_exceptions=True)
    print(responses)
    tool_messages = []
    state_updates = {}

    for tc, response in zip(last_message.tool_calls, responses):
        print(response)
        if isinstance(response, Exception):
            raise response
        message, updates = response
        tool_messages.append(ToolMessage(
            content=str(message),
            name=tc["name"],
            tool_call_id=tc["id"]
        ))
        state_updates.update(updates)

    if 'messages' not in state_updates:
        state_updates["messages"] = []

    state_updates["messages"] = tool_messages 
    return state_updates

def create_data_summary(state):
    summary = ""
    variables = []
    for d in state["input_data"]:
        variables.append(d.variable_name)
        summary += f"\n\nVariable: {d.variable_name}\n"
        summary += f"Description: {d.data_description}"
    
    if "current_variables" in state:
        remaining_variables = [v for v in state["current_variables"] if v not in variables]
        for v in remaining_variables:
            summary += f"\n\nVariable: {v}"
    return summary

def route_to_tools(state):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route back to the agent.
    """

    if messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "data analyst tool node"
    return "__end__"

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
sample_manager_tools = [
    sci_tools.check_for_sample_form,
    sci_tools.check_for_test_result_form,
    sci_tools.generate_sample_json,
    sci_tools.generate_validation_json,
    sci_tools.update_submission
    ]

def sample_manager(state):  
    #print(state)
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
#data_analyst_tools = [sci_tools.complete_python_task, sci_tools.show_data]

def data_analyst(state):  
    
    current_data_template  = """The following data is available:\n{data_summary}"""
    current_data_message = HumanMessage(content=current_data_template.format(data_summary=create_data_summary(state)))
  
    state["messages"] = [current_data_message] + state["messages"]
    
    chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', sci_prompts.data_analyst_prompt),
        ('placeholder', "{messages}")
    ]
    )
    chain = chat_template | model.bind_tools(data_analyst_tools)
    
    llm_outputs = chain.invoke(state)   
 

    return {"messages": [llm_outputs], "intermediate_outputs": [current_data_message.content]}

            
 

def data_analyst_conditional_edge(state):    
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'data analyst tool node'
    else:
        return '__end__'
    
#data_analyst_tool_node = ToolNode(data_analyst_tools)

graph.add_node('data analyst', data_analyst)
graph.add_node('data analyst tool node', call_tools)
graph.add_conditional_edges('data analyst', route_to_tools)
graph.add_edge('data analyst tool node', 'data analyst')



#finish graph
graph.set_entry_point('supervisor')
agents = graph.compile()





