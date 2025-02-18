from langgraph.graph import StateGraph, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import ToolNode
from utils.tools import query_knowledge_base, search_for_protocol


prompt = """
You are a digital assistant for biotechnology. You can help your user achieve the goals listed below.

#Goals

1. Anser questions the user might have relting to services offered.
2. Fetch relevant protocols based on queries.

#Tone

Helpul and friendly. Use science based language.
"""

model = ChatAnthropic(model="claude-3-5-sonnet-latest")

chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', prompt),
        ('placeholder', "{messages}")
    ]
)

tools = [query_knowledge_base, search_for_protocol]
llm_with_prompt = chat_template | model.bind_tools(tools)


def call_agent(message_state: MessagesState):
    response = llm_with_prompt.invoke(message_state)
    return{
        'messages':[response]
    }

def is_there_tool_calls(state:MessagesState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'tool_node'
    else:
        return '__end__'


graph = StateGraph(MessagesState)

tool_node = ToolNode(tools)
graph.add_node('agent', call_agent)
graph.add_node('tool_node', tool_node)
graph.add_conditional_edges("agent", is_there_tool_calls)
graph.set_entry_point('agent')
graph.add_edge('tool_node', 'agent')
app = graph.compile()

