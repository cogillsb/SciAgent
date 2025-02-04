from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END, START
from sci_agent.utils.nodes import supervisor_node, sop_archivist_node, data_scientist_node, automation_specialist_node
from sci_agent.utils.nodes import sample_manager_node, lab_inventory_manager_node
from my_agent.utils.state import State





builder = StateGraph(State)
builder.add_edge(START, "supervisor")

builder.add_node("supervisor", supervisor_node)
builder.add_node("SOP archivist", sop_archivist_node)
builder.add_node("data scientist", data_scientist_node)
builder.add_node("automation specialist", automation_specialist_node)
builder.add_node("sample manager", ssample_manager_node)
builder.add_node("laboratory inventory manager", lab_inventory_manager_node)

graph = builder.compile()



