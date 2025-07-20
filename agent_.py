
import os
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings
from llama_index.core.tools import QueryEngineTool
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.memory.mem0 import Mem0Memory
from llama_index.core.chat_engine import SimpleChatEngine
from typing import List, Dict, Any
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAgent:
    """A comprehensive AI Agent using LlamaIndex with Groq LLM, memory, and tools."""
    
    def __init__(self, groq_api_key: str, documents_path: str = None):
        """
        Initialize the AI Agent.
        
        Args:
            groq_api_key: API key for Groq
            documents_path: Path to documents for knowledge base (optional)
        """
        self.groq_api_key = groq_api_key
        self.documents_path = documents_path
        
        # Initialize components
        self._setup_llm()
        self._setup_embeddings()
        self._setup_memory()
        self._setup_knowledge_base()
        self._setup_tools()
        self._setup_agent()
    
    def _setup_llm(self):
        """Set up the Groq LLM."""
        self.llm = Groq(
            model="llama3-70b-8192",
            api_key=self.groq_api_key,
            temperature=0.1
        )
        Settings.llm = self.llm
        logger.info("Groq LLM initialized successfully")
    
    def _setup_embeddings(self):
        """Set up HuggingFace embeddings."""
        self.embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        Settings.embed_model = self.embed_model
        logger.info("HuggingFace embeddings initialized successfully")
    
    def _setup_memory(self):
        """Set up memory system with enhanced Mem0 integration."""
        try:
            # Check if Mem0 API key is available
            mem0_api_key = os.getenv("MEM0_API_KEY")
            
            if mem0_api_key and mem0_api_key != "your_mem0_api_key_here":
                # Initialize Mem0 with enhanced configuration
                import uuid
                from datetime import datetime
                
                # Generate or use existing user session ID
                session_id = os.getenv("USER_SESSION_ID", str(uuid.uuid4())[:8])
                
                self.memory = Mem0Memory(
                    config={
                        "api_key": mem0_api_key,
                        "user_id": f"ai_agent_user_{session_id}",
                        "app_id": "ai_agent_app",
                        "version": "v1.0"
                    }
                )
                
                # Store session info
                self.session_id = session_id
                self.session_start = datetime.now().isoformat()
                
                logger.info(f"Mem0 memory initialized successfully with session: {session_id}")
                
                # Add initial session context to memory if this is a new session
                try:
                    self.memory.add(
                        messages=[{
                            "role": "system", 
                            "content": f"New AI Agent session started at {self.session_start}. Session ID: {session_id}. This is a comprehensive AI assistant with capabilities including movie information, calculations, weather, and knowledge base queries."
                        }]
                    )
                except Exception as mem_error:
                    logger.warning(f"Could not add session context to memory: {mem_error}")
                    
            else:
                # Use basic memory without Mem0 cloud service
                logger.info("No Mem0 API key found. Using basic memory.")
                logger.info("For persistent memory across sessions, set up your Mem0 API key from: https://mem0.ai")
                self.memory = None
                self.session_id = None
                self.session_start = None
                
        except Exception as e:
            logger.warning(f"Failed to initialize Mem0 memory: {e}")
            logger.info("Continuing without persistent memory")
            self.memory = None
            self.session_id = None
            self.session_start = None
    
    def _setup_knowledge_base(self):
        """Set up knowledge base from documents."""
        self.query_engine = None
        if self.documents_path and os.path.exists(self.documents_path):
            try:
                # Load documents
                documents = SimpleDirectoryReader(self.documents_path).load_data()
                
                # Create node parser
                node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
                
                # Create vector store index
                index = VectorStoreIndex.from_documents(
                    documents, 
                    node_parser=node_parser,
                    embed_model=self.embed_model
                )
                
                # Create query engine
                self.query_engine = index.as_query_engine(llm=self.llm)
                logger.info(f"Knowledge base created from {len(documents)} documents")
            except Exception as e:
                logger.error(f"Failed to create knowledge base: {e}")
    
    def _setup_tools(self):
        """Set up tools for the agent."""
        self.tools = []
        
        # Calculator tool
        def calculator(expression: str) -> str:
            """Calculate mathematical expressions safely."""
            try:
                # Basic safety check
                allowed_chars = set('0123456789+-*/().% ')
                if not all(c in allowed_chars for c in expression):
                    return "Error: Invalid characters in expression"
                
                result = eval(expression)
                return f"Result: {result}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        calculator_tool = FunctionTool.from_defaults(
            fn=calculator,
            name="calculator",
            description="Calculate mathematical expressions"
        )
        self.tools.append(calculator_tool)
        
        # Weather tool (mock implementation)
        def get_weather(location: str) -> str:
            """Get weather information for a location."""
            # This is a mock implementation
            return f"Weather in {location}: Sunny, 22°C. This is a mock response."
        
        weather_tool = FunctionTool.from_defaults(
            fn=get_weather,
            name="weather",
            description="Get weather information for a specific location"
        )
        self.tools.append(weather_tool)
        
        # Movie information tool
        def get_movie_info(movie_title: str) -> str:
            """Get information about movies including plot, cast, ratings, and more."""
            # This is a comprehensive movie information function
            # In a real implementation, you would integrate with APIs like TMDB, OMDB, etc.
            
            # Mock movie database for demonstration
            movies_db = {
                "the godfather": {
                    "title": "The Godfather",
                    "year": 1972,
                    "director": "Francis Ford Coppola",
                    "cast": ["Marlon Brando", "Al Pacino", "James Caan", "Robert Duvall", "Diane Keaton"],
                    "genre": "Crime, Drama",
                    "rating": "9.2/10",
                    "plot": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son."
                },
                "inception": {
                    "title": "Inception",
                    "year": 2010,
                    "director": "Christopher Nolan",
                    "cast": ["Leonardo DiCaprio", "Marion Cotillard", "Tom Hardy", "Ellen Page", "Ken Watanabe"],
                    "genre": "Action, Sci-Fi, Thriller",
                    "rating": "8.8/10",
                    "plot": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea."
                },
                "pulp fiction": {
                    "title": "Pulp Fiction",
                    "year": 1994,
                    "director": "Quentin Tarantino",
                    "cast": ["John Travolta", "Uma Thurman", "Samuel L. Jackson", "Bruce Willis", "Harvey Keitel"],
                    "genre": "Crime, Drama",
                    "rating": "8.9/10",
                    "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption."
                },
                "the dark knight": {
                    "title": "The Dark Knight",
                    "year": 2008,
                    "director": "Christopher Nolan",
                    "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart", "Michael Caine", "Gary Oldman"],
                    "genre": "Action, Crime, Drama",
                    "rating": "9.0/10",
                    "plot": "Batman faces the Joker, a criminal mastermind who wants to plunge Gotham City into anarchy."
                },
                "forrest gump": {
                    "title": "Forrest Gump",
                    "year": 1994,
                    "director": "Robert Zemeckis",
                    "cast": ["Tom Hanks", "Robin Wright", "Gary Sinise", "Mykelti Williamson", "Sally Field"],
                    "genre": "Drama, Romance",
                    "rating": "8.8/10",
                    "plot": "The story of a man with low IQ who accomplishes great things and influences many historical events."
                },
                "the shawshank redemption": {
                    "title": "The Shawshank Redemption",
                    "year": 1994,
                    "director": "Frank Darabont",
                    "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler", "Clancy Brown"],
                    "genre": "Drama",
                    "rating": "9.3/10",
                    "plot": "Two imprisoned men bond over years, finding solace and eventual redemption through acts of common decency."
                },
                "goodfellas": {
                    "title": "Goodfellas",
                    "year": 1990,
                    "director": "Martin Scorsese",
                    "cast": ["Robert De Niro", "Ray Liotta", "Joe Pesci", "Lorraine Bracco", "Paul Sorvino"],
                    "genre": "Biography, Crime, Drama",
                    "rating": "8.7/10",
                    "plot": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners."
                },
                "titanic": {
                    "title": "Titanic",
                    "year": 1997,
                    "director": "James Cameron",
                    "cast": ["Leonardo DiCaprio", "Kate Winslet", "Billy Zane", "Gloria Stuart", "Frances Fisher"],
                    "genre": "Drama, Romance",
                    "rating": "7.8/10",
                    "plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."
                },
                "casablanca": {
                    "title": "Casablanca",
                    "year": 1942,
                    "director": "Michael Curtiz",
                    "cast": ["Humphrey Bogart", "Ingrid Bergman", "Paul Henreid", "Claude Rains", "Conrad Veidt"],
                    "genre": "Drama, Romance, War",
                    "rating": "8.5/10",
                    "plot": "A cynical expatriate American cafe owner struggles to decide whether to help his former lover and her fugitive husband escape the Nazis in French Morocco."
                },
                "star wars": {
                    "title": "Star Wars: Episode IV - A New Hope",
                    "year": 1977,
                    "director": "George Lucas",
                    "cast": ["Mark Hamill", "Harrison Ford", "Carrie Fisher", "Peter Cushing", "Alec Guinness"],
                    "genre": "Action, Adventure, Fantasy, Sci-Fi",
                    "rating": "8.6/10",
                    "plot": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station."
                },
                "the matrix": {
                    "title": "The Matrix",
                    "year": 1999,
                    "director": "The Wachowski Sisters",
                    "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss", "Hugo Weaving", "Gloria Foster"],
                    "genre": "Action, Sci-Fi",
                    "rating": "8.7/10",
                    "plot": "A computer programmer is led to fight an underground war against powerful computers who have constructed his entire reality with a system called the Matrix."
                },
                "schindler's list": {
                    "title": "Schindler's List",
                    "year": 1993,
                    "director": "Steven Spielberg",
                    "cast": ["Liam Neeson", "Ralph Fiennes", "Ben Kingsley", "Caroline Goodall", "Jonathan Sagall"],
                    "genre": "Biography, Drama, History",
                    "rating": "9.0/10",
                    "plot": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis."
                },
                "citizen kane": {
                    "title": "Citizen Kane",
                    "year": 1941,
                    "director": "Orson Welles",
                    "cast": ["Orson Welles", "Joseph Cotten", "Dorothy Comingore", "Agnes Moorehead", "Ruth Warrick"],
                    "genre": "Drama, Mystery",
                    "rating": "8.3/10",
                    "plot": "Following the death of publishing tycoon Charles Foster Kane, reporters scramble to uncover the meaning of his final utterance: 'Rosebud'."
                },
                "vertigo": {
                    "title": "Vertigo",
                    "year": 1958,
                    "director": "Alfred Hitchcock",
                    "cast": ["James Stewart", "Kim Novak", "Barbara Bel Geddes", "Tom Helmore", "Henry Jones"],
                    "genre": "Mystery, Romance, Thriller",
                    "rating": "8.3/10",
                    "plot": "A former police detective juggles wrestling with his personal demons and becoming obsessed with a beautiful woman."
                },
                "apocalypse now": {
                    "title": "Apocalypse Now",
                    "year": 1979,
                    "director": "Francis Ford Coppola",
                    "cast": ["Martin Sheen", "Marlon Brando", "Robert Duvall", "Dennis Hopper", "Frederic Forrest"],
                    "genre": "Drama, Mystery, War",
                    "rating": "8.4/10",
                    "plot": "A U.S. Army officer serving in Vietnam is tasked with assassinating a renegade Special Forces Colonel who sees himself as a god."
                }
            }
            
            # Search for the movie (case-insensitive)
            movie_key = movie_title.lower().strip()
            
            if movie_key in movies_db:
                movie = movies_db[movie_key]
                return f"""🎬 **{movie['title']}** ({movie['year']})
                
**Director:** {movie['director']}
**Cast:** {', '.join(movie['cast'])}
**Genre:** {movie['genre']}
**Rating:** {movie['rating']}
**Plot:** {movie['plot']}
                
This is sample data. In a real implementation, this would connect to movie databases like TMDB or OMDB API."""
            else:
                # Provide suggestions for partial matches
                suggestions = [title for title in movies_db.keys() if movie_key in title]
                if suggestions:
                    return f"Movie '{movie_title}' not found in database. Did you mean: {', '.join(suggestions)}?"
                else:
                    return f"Movie '{movie_title}' not found in database. Available movies include: The Godfather, Inception, Pulp Fiction, The Dark Knight, Forrest Gump, The Shawshank Redemption, Goodfellas, Titanic, Casablanca, Star Wars, The Matrix, Schindler's List, Citizen Kane, Vertigo, and Apocalypse Now."
        
        movie_tool = FunctionTool.from_defaults(
            fn=get_movie_info,
            name="movie_info",
            description="Get detailed information about movies including plot, cast, director, rating, and genre. Provide the movie title to search for."
        )
        self.tools.append(movie_tool)
        
        # Knowledge base query tool
        if self.query_engine:
            kb_tool = QueryEngineTool.from_defaults(
                query_engine=self.query_engine,
                name="knowledge_base",
                description="Query the knowledge base for information from documents"
            )
            self.tools.append(kb_tool)
        
        # Enhanced Memory search tool
        def search_memory(query: str) -> str:
            """Search through conversation memory and retrieve relevant past interactions."""
            if self.memory:
                try:
                    results = self.memory.search(query)
                    if results:
                        # Format the results for better readability
                        if isinstance(results, list):
                            formatted_results = []
                            for i, result in enumerate(results[:5], 1):  # Limit to top 5 results
                                if isinstance(result, dict):
                                    content = result.get('content', str(result))
                                else:
                                    content = str(result)
                                formatted_results.append(f"{i}. {content}")
                            return f"🧠 **Memory Search Results:**\n" + "\n".join(formatted_results)
                        else:
                            return f"🧠 **Found in memory:** {results}"
                    else:
                        return f"🔍 No relevant information found in memory for '{query}'. Try rephrasing your search or ask about recent conversations."
                except Exception as e:
                    logger.error(f"Memory search error: {e}")
                    return f"❌ Memory search error: {str(e)}"
            return "💭 Memory system not available. For persistent memory across sessions, configure your Mem0 API key."
        
        memory_tool = FunctionTool.from_defaults(
            fn=search_memory,
            name="memory_search",
            description="Search through conversation history and memory to find relevant past interactions, topics discussed, or information shared"
        )
        self.tools.append(memory_tool)
        
        # Add a memory summary tool
        def get_memory_summary() -> str:
            """Get a summary of recent conversations and key topics."""
            if self.memory:
                try:
                    # Try to get recent memories
                    recent_search = self.memory.search("conversation summary recent topics")
                    if recent_search:
                        return f"📋 **Recent Memory Summary:**\n{recent_search}"
                    else:
                        return "📝 No recent conversation summary available. Start chatting to build memory!"
                except Exception as e:
                    return f"❌ Error retrieving memory summary: {str(e)}"
            return "💭 Memory system not available for summaries."
        
        summary_tool = FunctionTool.from_defaults(
            fn=get_memory_summary,
            name="memory_summary",
            description="Get a summary of recent conversations and key topics discussed"
        )
        self.tools.append(summary_tool)
        
        logger.info(f"Initialized {len(self.tools)} tools")
    
    def _setup_agent(self):
        """Set up the ReAct agent."""
        self.agent = ReActAgent.from_tools(
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            memory=self.memory
        )
        logger.info("ReAct agent initialized successfully")
    
    def chat(self, message: str) -> str:
        """
        Chat with the AI agent with enhanced memory management.
        
        Args:
            message: User's message
            
        Returns:
            Agent's response
        """
        try:
            # Get response from agent
            response = self.agent.chat(message)
            
            # Enhanced memory storage with metadata
            if self.memory:
                try:
                    from datetime import datetime
                    
                    # Create enriched memory entry
                    memory_entry = {
                        "messages": [
                            {"role": "user", "content": message},
                            {"role": "assistant", "content": str(response)}
                        ],
                        "metadata": {
                            "timestamp": datetime.now().isoformat(),
                            "session_id": getattr(self, 'session_id', 'unknown'),
                            "message_type": self._classify_message(message)
                        }
                    }
                    
                    self.memory.add(**memory_entry)
                    logger.debug("Successfully stored conversation in memory")
                    
                except Exception as e:
                    logger.warning(f"Failed to store in memory: {e}")
            
            return str(response)
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _classify_message(self, message: str) -> str:
        """Classify the type of message for better memory organization."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['movie', 'film', 'cinema', 'actor', 'director']):
            return 'movie_query'
        elif any(word in message_lower for word in ['calculate', 'math', '+', '-', '*', '/', 'equation']):
            return 'calculation'
        elif any(word in message_lower for word in ['weather', 'temperature', 'climate']):
            return 'weather_query'
        elif any(word in message_lower for word in ['remember', 'recall', 'memory', 'previous', 'earlier']):
            return 'memory_search'
        elif '?' in message:
            return 'question'
        else:
            return 'general_conversation'
    
    def reset_conversation(self):
        """Reset the conversation history."""
        try:
            if hasattr(self.agent, 'reset'):
                self.agent.reset()
            logger.info("Conversation reset successfully")
        except Exception as e:
            logger.warning(f"Failed to reset conversation: {e}")


def main():
    """Main function to run the AI agent."""
    # Get API key from environment variable
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("Please set the GROQ_API_KEY environment variable")
        print("You can get your API key from: https://console.groq.com/keys")
        return
    
    # Optional: Set path to documents for knowledge base
    documents_path = os.getenv("DOCUMENTS_PATH", "./documents")
    
    # Initialize the agent
    try:
        agent = AIAgent(groq_api_key, documents_path)
        print("🤖 AI Agent initialized successfully!")
        print("\n📋 Available Features:")
        print("  • 🎬 Enhanced Movie Database: 15+ classic and modern films")
        print("  • 🧮 Mathematical Calculator: Perform calculations")
        print("  • 🌤️  Weather Information: Get weather data (mock)")
        print("  • 📚 Knowledge Base: AI, Programming, Technology, Science, Space")
        print("  • 🧠 Persistent Memory: Mem0 integration for session memory")
        print("  • 🔍 Memory Search: Search past conversations and topics")
        
        # Display memory status
        if hasattr(agent, 'memory') and agent.memory:
            session_info = f" (Session: {getattr(agent, 'session_id', 'unknown')})" if hasattr(agent, 'session_id') else ""
            print(f"  • ✅ Mem0 Memory: Active{session_info}")
        else:
            print("  • ⚠️  Mem0 Memory: Not configured (add MEM0_API_KEY for persistence)")
        
        print("\n💬 Commands:")
        print("  • Type 'quit' or 'exit' to end the conversation")
        print("  • Type 'reset' to reset the conversation history")
        print("  • Type 'help' for feature examples")
        print("  • Ask about movies, calculations, AI, programming, science, or anything!")
        print("-" * 70)
        
        # Interactive chat loop
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye! 👋")
                break
            elif user_input.lower() == 'reset':
                agent.reset_conversation()
                print("🔄 Conversation reset!")
                continue
            elif user_input.lower() == 'help':
                print("\n📋 Feature Examples:")
                print("  🎬 Movies: 'Tell me about The Matrix' or 'What's Inception about?'")
                print("  🧮 Math: 'Calculate 15 * 24 + 10' or 'What's 25% of 80?'")
                print("  🌤️  Weather: 'What's the weather in London?'")
                print("  🤖 AI: 'What is machine learning?' or 'Explain neural networks'")
                print("  💻 Programming: 'Tell me about Python' or 'What is JavaScript used for?'")
                print("  🔬 Science: 'What are the latest space missions?' or 'Explain quantum physics'")
                print("  🧠 Memory: 'What did we discuss earlier?' or 'Search memory for movies'")
                print("  📊 Summary: Use the memory_summary tool to see recent conversations")
                continue
            elif not user_input:
                continue
            
            print("\n🤖 Agent:", end=" ")
            response = agent.chat(user_input)
            print(response)
            
    except Exception as e:
        print(f"Failed to initialize AI agent: {e}")


if __name__ == "__main__":
    main()