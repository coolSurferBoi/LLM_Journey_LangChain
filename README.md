# LLM Journey

**LLM Journey** is an interactive, stateful storytelling web application built with **Flask**, **LangGraph**, and **multi-provider image generation**.  
Users progress through a branching narrative powered by an LLM, make choices via dynamically generated buttons, and optionally generate scene imagery using **OpenAI** or **Hugging Face** image models.

The application demonstrates **graph-based orchestration**, **session-scoped state management**, and **pluggable AI backends** in a clean, extensible architecture.

---

## Key Features

- Graph-driven storytelling using **LangGraph**
- Stateful game sessions via **Flask sessions**
- Human-in-the-loop control with interruptible graph execution
- Multi-provider image generation:
  - OpenAI (`dall-e-3`)
  - Hugging Face (`black-forest-labs/FLUX.1-dev`)
- Dynamic UI options generated from LLM output
- Clean separation of concerns and extensible design

---

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

---

## Game Flow

1. User starts a session → `game_id` is generated
2. A LangGraph state machine is created for that session
3. The graph produces story text and selectable options
4. Options are rendered as buttons
5. Scene image is generated utilising Story Textg
6. User choice is sent back to the graph
7. Loop continues until the story ends

---

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

---

## LangGraph Design

- **Shared State:** `GameState`
- **Nodes:** `init_game`, `next_scenario`, `increment_counter`, `game_end`
- Conditional edges control story continuation or termination
- Checkpointing enabled via `MemorySaver`
- Interrupts before scenario generation for user input

---

## Session & State Management

| Layer | Responsibility |
|------|---------------|
| Flask `session` | Stores `game_id` and UI state |
| `graph_store` | One LangGraph instance per game |
| `api_store` | One image API factory per game |
| Flask `g` | Request-scoped graph & API access |
| `LLMJourneyState` | Button messages and state |

---


## Running the Application

```bash
pip install -r requirements.txt
./.venv/Scripts/Activate.ps1
python app.py
```

Open: http://127.0.0.1:5000

---

## Extensibility

- Add new LLM or image providers
- Persist state to Redis or a database
- Enable streaming responses
- Extend into a full agent-based game engine

---

## Author

**Hoon Kim**  
Data Engineer → AI Engineer  
Focused on LangGraph, RAG systems, and AI-driven applications
