from langgraph.graph import StateGraph, END
from .state import AgentState
from .node import researcher_node, coder_node, pr_creator_node

def create_agent_graph():
    workflow = StateGraph(AgentState)

    # 1. Register the Nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("pr_creator", pr_creator_node)

    # 2. Define the Edges
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "coder")
    
    # After coder generates the fix, go to PR creator
    workflow.add_edge("coder", "pr_creator")
    
    # End the process after PR is opened
    workflow.add_edge("pr_creator", END)

    return workflow.compile()