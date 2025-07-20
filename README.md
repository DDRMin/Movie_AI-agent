# AI Agent with LlamaIndex and Groq for a Event Management Project

A comprehensive AI agent built with LlamaIndex, featuring Groq LLM, memory capabilities, and various tools.

## Features

- **Groq LLM Integration**: Fast and efficient language model
- **Memory System**: Conversation memory using Mem0
- **Knowledge Base**: Document-based Q&A using vector embeddings
- **Built-in Tools**:
  - Calculator for mathematical operations
  - Weather information (mock implementation)
  - Knowledge base querying
  - Memory search
- **Interactive Chat**: Command-line interface for conversations

## Setup

### 1. Clone and Navigate
```bash
cd "d:\Codes\AI Agent"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows with bash
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 5. Optional: Add Documents
Create a `documents` folder and add text files for the knowledge base:
```bash
mkdir documents
# Add your .txt, .pdf, .docx files to this folder
```

## Usage

### Run the Agent
```bash
python agent_.py
```

### Environment Variable Setup
You can set the GROQ API key directly in your terminal:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
python agent_.py
```

### Interactive Commands
- Type your questions or requests
- Type `reset` to clear conversation history
- Type `quit` or `exit` to end the session

## Example Interactions

```
You: Calculate 15 * 23 + 100
🤖 Agent: I'll calculate that for you.
Result: 445

You: What's the weather in New York?
🤖 Agent: Weather in New York: Sunny, 22°C. This is a mock response.

You: Search my memory for previous calculations
🤖 Agent: Found in memory: [previous conversation results]
```

## Configuration

### Groq Models
You can change the model in `agent_.py`:
```python
self.llm = Groq(
    model="llama3-70b-8192",  # or "mixtral-8x7b-32768", "gemma-7b-it"
    api_key=self.groq_api_key,
    temperature=0.1
)
```

### Adding Custom Tools
Add new tools in the `_setup_tools` method:
```python
def your_custom_tool(param: str) -> str:
    """Your custom tool description."""
    # Your implementation
    return "result"

custom_tool = FunctionTool.from_defaults(
    fn=your_custom_tool,
    name="custom_tool",
    description="Description of what your tool does"
)
self.tools.append(custom_tool)
```

## API Keys

### Groq API Key
1. Visit [Groq Console](https://console.groq.com/keys)
2. Create an account if you don't have one
3. Generate a new API key
4. Copy the key and add it to your `.env` file

### Mem0 API Key (Optional)
1. Visit [Mem0](https://mem0.ai) if you want enhanced memory features
2. Get your API key and add it to the `.env` file

## Troubleshooting

### Common Issues

1. **ImportError**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Error**: Ensure your Groq API key is set correctly
   ```bash
   echo $GROQ_API_KEY  # Should show your key
   ```

3. **Memory Issues**: Mem0 memory is optional. The agent will work without it.

4. **Document Loading**: Ensure documents are in supported formats (.txt, .pdf, .docx)

### Performance Tips

- Use smaller document chunks for faster processing
- Adjust temperature for more creative or deterministic responses
- Consider using different Groq models based on your needs

## License

This project is open source. Feel free to modify and distribute.
