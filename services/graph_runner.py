from langchain_core.messages import HumanMessage
from graph.graph_builder import build_graph

class graph_runner:
    def __init__(self,thread_id):
        self.graph = build_graph()
        self.thread_id = thread_id

    def run_graph_turn(
        self,
        user_input: str | None = None
    ):
        thread = {"configurable": {"thread_id": self.thread_id}}

        # If this is a new user turn: inject the message first
        if user_input is not None:
            self.graph.update_state(
                thread,
                {"messages": HumanMessage(content=user_input)},
            )
            # After injecting a new message, we need to process it → use None
            input_for_stream = None
        else:
            # No new user input (e.g. first call to resume after interrupt) → just resume
            input_for_stream = {}

        # Run one turn
        events = list(self.graph.stream(input_for_stream, thread, stream_mode="values"))

        if not events:
            return {
                "last_message": None,
                "game_over": True
            }

        last_event = events[-1]
        last_message = last_event["messages"][-1]

        # Get current state for response count
        state = self.graph.get_state(thread)
        response_count = state.values.get("response_count", 0)

        return {
            "last_message": last_message.content,
            "response_count": response_count,
            "game_over": response_count >= 5
        }