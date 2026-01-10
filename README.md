# LLM Journey

**LLM Journey** is an interactive, stateful storytelling web application built with **Flask**, **LangGraph**, and **multi-provider image generation**.  
Users progress through a branching narrative powered by an LLM, make choices via dynamically generated buttons, and optionally generate scene imagery using **OpenAI** or **Hugging Face** image models.

The application demonstrates **graph-based orchestration**, **session-scoped state management**, and **pluggable AI backends** in a clean, extensible architecture.



## Key Features

- Graph-driven storytelling using **LangGraph**
- Stateful game sessions via **Flask sessions**
- Human-in-the-loop control with interruptible graph execution
- Multi-provider image generation:
  - OpenAI (`dall-e-3`)
  - Hugging Face (`black-forest-labs/FLUX.1-dev`)
- Dynamic UI options generated from LLM output
- Clean separation of concerns and extensible design



## High-Level Architecture

```text
Browser
  ↓
Flask App
  ├─ Session (game_id)
  ├─ Graph Runner (LangGraph)
  ├─ APIJourneyUtils
  │    ├─ OpenAiJourneyUtils
  │    └─ HuggingFaceJourneysUtils
  ↓
LLM + Image Providers
```


## Game Flow

1. User starts a session → `game_id` is generated
2. A LangGraph state machine is created for that session
3. The graph produces story text and selectable options
4. Options are rendered as buttons
5. Scene image is generated utilising Story Textg
6. User choice is sent back to the graph
7. Loop continues until the story ends



## Project Structure

```text
.
├── app.py
├── services/
│   └── graph_runner.py
├── graph/
│   ├── graph_builder.py
│   ├── llm.py
│   ├── nodes.py
│   └── state.py
├── utils/
│   ├── LLMJourneyState.py
│   ├── APIJourneyUtils.py
│   ├── OpenAiJourneyUtils.py
│   └── HuggingFaceJourneysUtils.py
├── static/
│   └── HuggingFaceImages/
│       └── generated/
├── templates/
│   ├── home.html
│   └── journey.html
├── .env
├── requirements.txt
└── README.md
```



## LangGraph Design

- **Shared State:** `GameState`
- **Nodes:** `init_game`, `next_scenario`, `increment_counter`, `game_end`
- Conditional edges control story continuation or termination
- Checkpointing enabled via `MemorySaver`
- Interrupts before scenario generation for user input



## Session & State Management

| Layer | Responsibility |
|-------|----------------|
| Flask `session` | Stores `game_id` and UI state |
| `graph_store` | One LangGraph instance per game |
| `api_store` | One image API factory per game |
| Flask `g` | Request-scoped graph & API access |
| `LLMJourneyState` | Button messages and state |





## Running the Application

```bash
pip install -r requirements.txt
./.venv/Scripts/Activate.ps1
python app.py
```

Open: http://127.0.0.1:5000



## Extensibility

#### Support additional LLM and image providers
- Extend the system to support alternative LLMs (beyond GPT-4o) and image generation providers (e.g. DALL·E, FLUX.1-dev) via a provider abstraction layer.
- Explore how output creativity and wording change when adjusting generation parameters such as temperature and top-p.

#### Reduce token usage and cost
- Currently, all messages in the LangChain graph are appended and sent to the LLM on each invocation, increasing token usage and cost.
- This can be optimized by:
  - passing only the most recent messages, or
  - introducing a summarization step to condense earlier conversation history.

#### Persist application and graph state using Redis or a database
- By default, state is stored in memory and is lost when the application restarts.
- Persisting state in Redis or a database enables durability, multi-user support, and horizontal scaling.
- For example:
  - The LangGraph checkpointer can be backed by Redis instead of in-memory storage, allowing users to pause and resume game sessions across requests and processes.
  - In the Flask app, in-memory stores such as `graph_store` and `api_store` can be externalized to Redis or a database, with the `thread_id` used as a stable session key.

#### Expose `graph_runner` as an API
- The `graph_runner` class can be exposed via an API endpoint, enabling modular integration with other services, clients, or agents.




## Author

**Hoon Kim**  the Data Specialist 😎
