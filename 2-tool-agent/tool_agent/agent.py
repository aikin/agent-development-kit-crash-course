from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search

def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

def simple_search(query: str) -> dict:
    """
    Perform a simple search simulation (replace this with actual search logic if needed)
    Returns search results for the given query
    """
    return {
        "query": query,
        "status": "success", 
        "message": f"Search completed for: {query}",
        "note": "This is a custom search tool simulation. For real web search, use the built-in google_search tool in a separate agent."
    }

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent with custom tools",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - get_current_time: Get the current date and time
    - simple_search: Perform basic search operations
    
    When users ask for the time, use get_current_time.
    When users want to search for something, use simple_search.
    """,
    tools=[get_current_time, simple_search],
    # tools=[google_search],
)