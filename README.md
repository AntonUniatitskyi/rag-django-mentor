# Django Mentor Bot

A Telegram bot that mentors students learning Django — powered by Retrieval-Augmented Generation (RAG) over the official Django documentation.

Unlike a typical "write my code" assistant, this bot is designed to **teach, not solve**: it refuses to hand over working code, points students to the relevant Django classes/methods, and only shows abstract examples pulled from the docs (never matching the student's own domain, so it can't be copy-pasted as a solution).

## Features

- **RAG over Django docs** — answers are grounded in the official documentation, not the model's general knowledge. If the answer isn't in the indexed docs, the bot says so instead of guessing.
- **Refuses to write code for the student** — even under direct pressure ("just show me on my example", "it's for research purposes"), the system prompt is designed to hold the line and redirect to concepts, relevant Django APIs, and abstract examples instead.
- **Answers in the student's language** — responds in whatever language the question was asked in.
- **Conversation memory** — follow-up questions ("what about for a required field?") are understood in context via a question-condensing step before retrieval.
- **Resilient LLM backend** — uses [litellm](https://github.com/BerriAI/litellm) with a multi-model fallback chain across providers (Groq, Gemini), so a single provider outage or model deprecation doesn't take the bot down.
- **Telegram-safe formatting** — answers are sanitized to Telegram's supported HTML subset before sending, with a plain-text fallback if anything still slips through.
- **`/new` command** — students can reset their conversation context at any time.

**Flow of a question:**

1. Student sends a message → bot shows a "typing" indicator.
2. The question is condensed into a standalone query using recent chat history.
3. The standalone query is embedded and searched against the Chroma vector store (`similarity_search`).
4. Retrieved doc chunks + the system prompt + conversation history are sent to the LLM via litellm.
5. The LLM's answer is sanitized to Telegram-safe HTML and sent, followed by a "Sources" message listing which doc files were used.

## Tech stack

- **[aiogram 3.x](https://docs.aiogram.dev/)** — Telegram bot framework
- **[LangChain](https://python.langchain.com/) + [Chroma](https://www.trychroma.com/)** — vector store for retrieval
- **HuggingFace `sentence-transformers/all-MiniLM-L6-v2`** — local, CPU-only embeddings (no API key required)
- **[litellm](https://github.com/BerriAI/litellm)** — unified LLM client with automatic provider fallback (Groq → Gemini)
- **[xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf)** — HTML → PDF for daily reports

## Setup

### 1. Environment variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the Django documentation

Place the Django docs (plain `.txt` files) under `django/docs/` in the project root, matching the folder structure Django's own doc source uses (e.g. `intro/`, `topics/db/`, `ref/class-based-views/`, etc.).

### 4. Build the vector database

```bash
python build_db.py
```

This reads the docs, chunks them, embeds them locally, and persists the result to `chroma_db/`. Only needs to be re-run when the docs change.

### 5. Run the bot

```bash
python -m bot.main
```

## Running with Docker

The vector database is built locally (embedding generation is CPU-light for search but the initial build over the full docs set can be slow on a weak server) and shipped alongside the code rather than rebuilt in the container.

```bash
docker compose up --build -d
```

`chroma_db/` and `bot_logs.db` are mounted as volumes, so they persist across container rebuilds and don't need to be baked into the image.

## Bot commands

| Command | Description |
|---|---|
| `/start` | Greeting and short intro |
| `/new` | Clears the current conversation history and starts fresh |

## Notes

- The LLM model list in `config.py` (`PRIMARY_MODEL` / `FALLBACK_MODELS`) may need occasional updates — free-tier providers periodically deprecate models. Check the relevant provider's docs if you start seeing `NotFoundError` / `model_not_found` errors.
- `OPENAI_API_KEY` in `config.py` is currently unused (embeddings are local; generation goes through Groq/Gemini via litellm) and can be removed if you don't plan to add an OpenAI-backed model to the fallback chain.