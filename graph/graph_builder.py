from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from .state import GameState
from .nodes import initialize_game,generate_next_scenario,increment_counter,end_game,continue_or_end
from langgraph.checkpoint.memory import MemorySaver

def build_graph():
    """
    Builds and compiles the LangGraph game state machine using GameState as shared state.
    The graph defines the game flow from initialization through scenario generation,
    conditional continuation, and termination, with checkpointing enabled for state persistence.
    """
    # Create the graph with GameState as the shared state
    GameGraph = StateGraph(GameState)

    # Register nodes
    GameGraph.add_node("init_game", initialize_game)
    GameGraph.add_node("next_scenario", generate_next_scenario)
    GameGraph.add_node("IncreaseCount", increment_counter)
    GameGraph.add_node("game_end", end_game)

    # Register Edges
    GameGraph.add_edge(START, "init_game")
    GameGraph.add_edge("init_game", "next_scenario")
    GameGraph.add_conditional_edges("next_scenario", continue_or_end)
    GameGraph.add_edge("IncreaseCount", "next_scenario")
    GameGraph.add_edge("game_end", END)

    memory = MemorySaver()

    # Interrupt BEFORE next_scenario so we can collect human input
    graph = GameGraph.compile(
        interrupt_before=["next_scenario"],
        checkpointer=memory
    )
    return graph
