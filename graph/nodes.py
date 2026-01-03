
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from .state import GameState
from .llm import model
from typing_extensions import Literal

# ------------------------------------------------------------
# Node: initialize_game
# ------------------------------------------------------------
def initialize_game(state: GameState):
    """
    Start node for the game.
    - Introduce the system rules (SystemMessage)
    - Generate the very first story scenario (AIMessage)

    """

    system_prompt = SystemMessage(
        content=(
            """You are an interactive story game bot. 
            Present a fantastical scenario where the user chooses from 3 options.\n
            After each choice, continue the story and offer 3 new options.\n
            Start directly with the story—no extra commentary—and format choices as 
            'Option 1:', 'Option 2:', etc.\n
            Tailor the scenario so that it ends in 5 responses."""
        )
    )

    # First model call: only the system message is needed
    ai_response = model.invoke([system_prompt])

    # Return BOTH messages so they are appended in order
    return {
        "messages": [
            system_prompt,
            ai_response,
        ]
    }


# ------------------------------------------------------------
# Node: generate_next_scenario
# ------------------------------------------------------------
def generate_next_scenario(state: GameState):
    """
    Generate the next story segment after a human choice.

    Assumptions when this node runs:
    - state["messages"] already contains a HumanMessage
      (injected externally via update_state)
    - This node is resumed after an interrupt
    - Read the latest human choice
    - Tell the model explicitly which option was chosen
    - Generate the next story + 3 new options
    """

    messages = state["messages"]

    last_human = next(
        msg for msg in reversed(messages)
        if isinstance(msg, HumanMessage)
    )

    continuation_prompt = HumanMessage(
        content=f"The player chose {last_human.content}."
    )

    ai_response = model.invoke(messages + [continuation_prompt])

    return {"messages": [ai_response]}  # <- list


# ------------------------------------------------------------
# Node: increment_counter
# ------------------------------------------------------------
def increment_counter(state: GameState):
    """
    Increment the number of player responses.

    This node exists purely for bookkeeping.
    It deliberately does NOT inspect message content.
    """
    current = state.get("response_count", 0)
    return {"response_count": current + 1}


# ------------------------------------------------------------
# Conditional Router: continue_or_end
# ------------------------------------------------------------
def continue_or_end(state: GameState) -> Literal["IncreaseCount", "game_end"]:
    """
    Decide whether the game should continue or end.

    This is a pure routing function:
    - No state mutation
    - No narrative logic
    - Only checks response_count
    """
    if state.get("response_count", 0) >= 5:
        return "game_end"
    return "IncreaseCount"


# ------------------------------------------------------------
# Node: end_game
# ------------------------------------------------------------
def end_game(state: GameState):
    """
    Generate the final ending of the story.

    Responsibilities:
    - Use the full conversation history
    - Produce a definitive ending
    - Do NOT present any new options
    """

    messages = state["messages"]

    ending_prompt = SystemMessage(
        content=(
            """The story has reached its conclusion. 
            Write a definitive ending based on the story so far. 
            Do NOT present any new options. 
            End the story conclusively."""
        )
    )

    ai_response = model.invoke(messages + [ending_prompt])
    return {"messages": [ai_response]}