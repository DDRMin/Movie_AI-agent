# AI Agent Setup and Usage Guide

## Prerequisites

1. **Python 3.8+** - Make sure you have Python installed
2. **Groq API Key** - Get from https://console.groq.com/keys
3. **Mem0 API Key** (Optional) - Get from https://mem0.ai

## Quick Setup

### 1. Install Dependencies

```powershell
# Create virtual environment (recommended)
python -m venv ai_agent_env
ai_agent_env\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your API keys:

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional - for persistent memory
MEM0_API_KEY=your_mem0_api_key_here

# Optional - path to documents for knowledge base
DOCUMENTS_PATH=./documents
```

### 3. Run the Agent

```powershell
python agent_.py
```

## Features

### 🧠 **Core Capabilities**
- **Chat Interface**: Natural language conversations
- **Memory System**: Remembers conversation context (with Mem0)
- **Knowledge Base**: Query documents from the `documents` folder
- **Multiple Tools**: Calculator, weather, movie info, memory search

### 🎬 **Movie Features**
- Ask about movie plots, cast, directors, ratings
- Search through movie database
- Get detailed movie information

### 💾 **Memory System**

**With Mem0 (Recommended):**
- Persistent memory across sessions
- Stores conversation history
- Retrieves relevant past conversations

**Without Mem0:**
- Basic session memory
- Resets when you restart the agent

## Example Usage

```
You: Tell me about The Godfather

🤖 Agent: [Uses movie_info tool]
🎬 **The Godfather** (1972)

**Director:** Francis Ford Coppola
**Cast:** Marlon Brando, Al Pacino, James Caan
**Genre:** Crime, Drama
**Rating:** 9.2/10
**Plot:** The aging patriarch of an organized crime dynasty transfers control to his reluctant son.

You: What's 15 * 23?

🤖 Agent: [Uses calculator tool]
Result: 345

You: Search my memory for godfather
🤖 Agent: [Uses memory_search tool]
Found in memory: [Previous conversation about The Godfather]
```

## Troubleshooting

### Common Issues:

1. **Missing API Key Error**
   - Make sure `.env` file exists with your GROQ_API_KEY

2. **Memory Initialization Failed**
   - Mem0 is optional - agent will work without it
   - Check your MEM0_API_KEY if you want persistent memory

3. **Documents Not Loading**
   - Make sure `documents` folder exists
   - Add `.txt`, `.md`, or `.pdf` files to the documents folder

4. **Module Import Errors**
   - Run: `pip install -r requirements.txt`
   - Make sure you're in the correct virtual environment

## API Keys Setup

### Groq API Key (Required)
1. Go to https://console.groq.com/keys
2. Sign up/login
3. Create a new API key
4. Add it to your `.env` file

### Mem0 API Key (Optional - for persistent memory)
1. Go to https://mem0.ai
2. Sign up for an account
3. Get your API key from dashboard
4. Add it to your `.env` file

## Adding Your Own Documents

1. Place text files (`.txt`, `.md`, `.pdf`) in the `documents` folder
2. The agent will automatically create a knowledge base from these files
3. Ask questions about your documents using natural language

## Commands

- `quit` or `exit` - End conversation
- `reset` - Reset conversation history
- Any other text - Chat with the agent
