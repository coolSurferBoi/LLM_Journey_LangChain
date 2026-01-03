from langgraph.graph import MessagesState

class GameState(MessagesState):
    """
    GameState extends LangGraph's MessagesState.

    Args:
    - response_count: tracks how many player choices have been made
      (used purely for control flow, not narrative logic)
    """
    response_count: int = 0