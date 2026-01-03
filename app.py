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


def init_session_state():
    session['button_messages'] = {}
    session['game_id'] = str(uuid.uuid4())
    app.config['graph_runner'] = graph_runner(session['game_id'])
    app.config['api_obj'] = APIJourneyUtils()

def process_reply(state: LLMJourneyState, reply_content: str):
    """Extracts story and options from reply and updates the button state."""
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
    init_session_state()
    image_gen_options = ["dall-e-3","black-forest-labs/FLUX.1-dev"]
    # Initialize session and local state manager
    return render_template('home.html', image_gen_options=image_gen_options)

@app.route('/journey', methods=['GET', 'POST'])
def journey():
    title = "LLM Journey"
    message = None

    image_gen = request.args.get('image_gen')
    app.config['api_obj'].setup_ImageGen_connection(image_gen)
    
    state = LLMJourneyState()
    state.set_button_messages(session.get('button_messages', {}))
    state.reset_button_states()
    print(request.method)
    # Handle POST (button clicked)
    if request.method == 'POST':
        button_name = request.form.get('button_name')
        if not button_name or button_name not in state.get_all_button_messages():
            return redirect(url_for('home'))

        state.setup_button_state(button_name)
        message = state.get_button_message(button_name)

        result = app.config['graph_runner'].run_graph_turn(user_input = button_name)
        print(result)
        text = process_reply(state, result['last_message'])
        
    # Handle GET (initial load)
    else:
        result = app.config['graph_runner'].run_graph_turn()
        text = process_reply(state, result['last_message'])
    image_url = app.config['api_obj'].get_img(image_gen,text)
    session['button_messages'] = state.get_all_button_messages()
    if not state.get_all_button_messages():
        return render_template(
            'journey.html',
            title=title,
            text=text,
            image_url=image_url,
            button_messages=state.get_all_button_messages(),
            button_states=state.get_all_button_states(),
            message=message,
            dropdown1 = 'gpt-4-mini',
            dropdown2 = image_gen,
            ending = True
        )
    else:
        return render_template(
            'journey.html',
            title=title,
            text=text,
            image_url=image_url,
            button_messages=state.get_all_button_messages(),
            button_states=state.get_all_button_states(),
            message=message,
            dropdown1 = 'gpt-4-mini',
            dropdown2 = image_gen
        )

@app.route('/reset')
def reset_game():
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)