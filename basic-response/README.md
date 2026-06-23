py# LLM CLI Chat

An interactive command-line chat interface that streams responses from OpenAI's GPT models (or compatible local models).

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key (or access to a compatible local model)

## Setup

### 1. Create a Python Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your API Key

Set the `OPENAI_API_KEY` environment variable:

**macOS/Linux:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Windows:**
```bash
set OPENAI_API_KEY=your-api-key-here
```

Or create a `.env` file in the project directory and load it before running the script.

## Running the Script

```bash
python chat.py
```

The script will initialize and prompt you to start chatting. Type your messages and the AI will stream responses in real-time. Type `exit` or `quit` to end the conversation.

## Configuration

- **Model**: To change the model, edit the `model_name` variable in `chat.py` (default: `gpt-4o-mini`)
- **Local Models**: To use a local model with Ollama, uncomment and set the `base_url` parameter:
  ```python
  client = OpenAI(base_url="http://localhost:11434/v1")
  ```
