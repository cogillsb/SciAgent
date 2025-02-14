from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from sci_agent.utils.tools import get_SOP, find_conc, write_method, upload_samples, order_supplies
from langgraph.prebuilt import ToolNode
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from sci_agent.utils.state import State
from sci_agent.utils import prompts
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

#from langgraph_supervisor import create_supervisor


model = ChatAnthropic(model="claude-3-5-sonnet-latest")

options = prompts.members + ["FINISH"]

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal[*options]

###################################################
#supervisor
####################################################
def supervisor_node(state: State) -> Command[Literal[*prompts.members, "__end__"]]:
    messages = [
        {"role": "system", "content": prompts.supervisor_prompt},
    ] + state["messages"]
    response = model.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END
    return Command(goto=goto, update={"next": goto})

###################################################
#SOP
####################################################
sop_archivist_agent = create_react_agent(
    model, tools=[get_SOP], messages_modifier=prompts.SOP_archivist_prompt
)

def sop_archivist_node(state: State) -> Command[Literal["supervisor"]]:
    result = sop_archivist_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="SOP archivist")
            ]
        },
        goto="supervisor",
    )
###################################################
#Data Scientist
####################################################

data_scientist_agent = create_react_agent(
    model, tools=[find_conc], prompt=prompts.data_scientist_prompt
)

def data_scientist_node(state: State) -> Command[Literal["supervisor"]]:
    result = data_scientist.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="data scientist")
            ]
        },
        goto="supervisor",
    )

###################################################
#Automation specialist
####################################################

automation_specialist_agent = create_react_agent(
    model, tools=[write_method], prompt=prompts.automation_specialist_prompt
)

def automation_specialist_node(state: State) -> Command[Literal["supervisor"]]:
    result = automation_specialist_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="automation specialist")
            ]
        },
        goto="supervisor",
    )

###################################################
#sample manager
####################################################

sample_manager_agent = create_react_agent(
    model, tools=[upload_samples], prompt=prompts.sample_manager_prompt
)

def sample_manager_node(state: State) -> Command[Literal["supervisor"]]:
    result = sample_manager_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="sample manager")
            ]
        },
        goto="supervisor",
    )

###################################################
#lab inventory manager
####################################################

lab_inventory_manager_agent = create_react_agent(
    model, tools=[order_supplies], prompt=prompts.lab_inventory_manager_prompt
)

def lab_inventory_manager_node(state: State) -> Command[Literal["supervisor"]]:
    result = lab_inventory_manager_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="lab inventory manager")
            ]
        },
        goto="supervisor",
    )

   







