
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from typing import List
import operator
from dataclasses import dataclass

@dataclass
class InputData:
    variable_name: str
    data_path: str
    data_description: str

class SciState(TypedDict):
    query: str
    messages: Annotated[list[HumanMessage | AIMessage | ToolMessage], add_messages]
    data: dict
    documents: List[Document]
    input_data: Annotated[List[InputData], operator.add]
    intermediate_outputs: Annotated[List[dict], operator.add]
    current_variables: dict
    output_image_paths: Annotated[List[str], operator.add]
    next:str
    
    

class RelevanceAnalysis(BaseModel):
    best_document_index: int = Field(description="Index of the most relevant document")
    reasoning: str = Field(description="Explanation of why this document was selected")
