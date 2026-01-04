from dotenv import load_dotenv
# Load .env file
load_dotenv()
from services.graph_runner import graph_runner
from flask import Flask, render_template, request, session, redirect, url_for, g
import re
from utils.LLMJourneyState import LLMJourneyState
from utils.APIJourneyUtils import APIJourneyUtils
import uuid

app = Flask(__name__)
app.secret_key = "mysecretkey"
graph_store = {}
api_store = {}


def ensure_session():
    """
    Ensures required session keys exist for a new or returning user.
    Initializes per-session UI state such as button messages and
    selected image generation model when missing.
    """

    if 'game_id' not in session:
        session['button_messages'] = {}
        session['image_gen'] = None  # optional default

@app.before_request
def load_per_request_objects():
    """
    Initializes and loads per-request game resources based on the session game_id.
    Creates and caches a graph runner and API utility instance per game,
    and attaches them to Flask's `g` object for request-scoped access.
    """

    game_id = session.get("game_id")

    if not game_id:
        game_id = str(uuid.uuid4())
        session["game_id"] = game_id

    # graph: create once per game_id
    if game_id not in graph_store:
        graph_store[game_id] = graph_runner(game_id)

    if game_id not in api_store:
        api_store[game_id] = APIJourneyUtils()

    # attach to g for convenience
    g.graph = graph_store[game_id]
    g.api = api_store[game_id]


def process_reply(state: LLMJourneyState, reply_content: str):
    """
    Parses the LLM reply into narrative text and selectable options.
    Updates the journey state with new button messages and resets
    button interaction state for the next turn.
    """

    text = reply_content.split("Option 1")[0]
    raw_options = re.findall(r"Option \d:.*", reply_content)[:3]
    # Remove 'Option N: ' prefix from each option string
    options = [re.sub(r"Option \d:\s*", "", opt) for opt in raw_options]
    
    state.reset_message_states()
    state.setup_button_messages(options)
    state.reset_button_states()
    return text

@app.route('/')
def home():
    """
    Renders the home page where the user selects configuration options
    such as the image generation backend before starting the journey.
    """

    image_gen_options = ["dall-e-3","black-forest-labs/FLUX.1-dev"]
    # Initialize session and local state manager
    return render_template('home.html', image_gen_options=image_gen_options)

@app.route('/journey', methods=['GET', 'POST'])
def journey():
    """
    Main game loop endpoint that advances the LLM-driven journey.
    Handles user choices, executes a graph turn, generates optional
    images, and renders the updated story and available actions.
    """

    title = "LLM Journey"

    # persist image_gen choice 
    if request.args.get('image_gen'):
        session['image_gen'] = request.args['image_gen']
    image_gen = session.get('image_gen')

    if image_gen:
        g.api.setup_ImageGen_connection(image_gen)

    state = LLMJourneyState()
    state.set_button_messages(session.get('button_messages', {}))

    if request.method == 'POST':
        button_name = request.form.get('button_name')
        if not button_name or button_name not in state.get_all_button_messages():
            return redirect(url_for('home'))

        # send the option text, not the button id
        chosen_text = state.get_button_message(button_name)

        result = g.graph.run_graph_turn(user_input=chosen_text)
        print(result)
        text = process_reply(state, result['last_message'])
    else:
        result = g.graph.run_graph_turn()
        text = process_reply(state, result['last_message'])

    image_url = g.api.get_img(image_gen, text) if image_gen else None
    session['button_messages'] = state.get_all_button_messages()

    ending = not bool(state.get_all_button_messages())
    return render_template(
        'journey.html',
        title=title,
        text=text,
        image_url=image_url,
        button_messages=state.get_all_button_messages(),
        button_states=state.get_all_button_states(),
        dropdown1='gpt-4-mini',
        dropdown2=image_gen,
        ending=ending
    )

@app.route("/reset")
def reset_game():
    """
    Resets the current game session and clears all cached state.
    Removes graph and API instances tied to the session game_id
    and redirects the user back to the home screen.
    """

    game_id = session.get("game_id")

    if game_id:
        graph_store.pop(game_id, None)
        api_store.pop(game_id, None)

    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    """
    Entry point for running the Flask development server locally.
    Enables debug mode for rapid iteration during development.
    """
    app.run(debug=True)