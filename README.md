# basic-langchain-app
playing around small ML apps, agents, langchain etc

## Setup

### 1. Enable Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the App

### Console Output

```bash
python app.py
```

This will start an interactive chat assistant in your console. Type your questions and the assistant will respond. Type `exit` or `quit` to end the conversation.

**Note:** Make sure to set your `ANTHROPIC_API_KEY` in a `.env` file before running the app.
