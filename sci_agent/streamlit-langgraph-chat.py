import streamlit as st
from typing import Dict, List, Tuple
from dataclasses import dataclass
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage

# Define the state schema
@dataclass
class State:
    messages: List[BaseMessage]
    current_message: str = ""
    display_content: str = ""

# Initialize agents/tools
def process_message(state: State) -> Dict:
    """Process the current message and update state."""
    # Here you would typically:
    # 1. Call your LLM
    # 2. Process the response
    # 3. Update display content if needed
    
    # This is a placeholder implementation
    response = f"Echo: {state.current_message}"
    state.messages.append(AIMessage(content=response))
    state.display_content = f"Last processed message: {state.current_message}"
    return {"messages": state.messages, "display_content": state.display_content}

# Configure the graph
def create_graph() -> StateGraph:
    workflow = StateGraph(State)
    
    # Add the main processing node
    workflow.add_node("process", process_message)
    
    # Define edges
    workflow.set_entry_point("process")
    workflow.add_edge("process", END)
    
    return workflow.compile()

# Streamlit UI
def main():
    st.title("LangGraph Chat Interface")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "graph" not in st.session_state:
        st.session_state.graph = create_graph()
    if "display_content" not in st.session_state:
        st.session_state.display_content = ""

    # Create two columns: chat and display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Chat")
        # Display chat messages
        for message in st.session_state.messages:
            if isinstance(message, HumanMessage):
                st.write("You:", message.content)
            else:
                st.write("Assistant:", message.content)
        
        # Chat input
        user_input = st.text_input("Type your message:", key="user_input")
        if st.button("Send"):
            if user_input:
                # Add user message to state
                st.session_state.messages.append(HumanMessage(content=user_input))
                
                # Create initial state
                state = State(
                    messages=st.session_state.messages,
                    current_message=user_input,
                    display_content=st.session_state.display_content
                )
                
                # Run the graph
                result = st.session_state.graph.invoke(state)
                
                # Update session state
                st.session_state.messages = result["messages"]
                st.session_state.display_content = result["display_content"]
                
                # Clear input
                st.session_state.user_input = ""
                st.rerun()

    with col2:
        st.subheader("Display Window")
        st.write(st.session_state.display_content)

if __name__ == "__main__":
    main()
