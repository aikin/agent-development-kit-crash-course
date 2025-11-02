import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# https://docs.litellm.ai/docs/providers/openrouter
model = LiteLlm(
    model="openrouter/deepseek/deepseek-chat-v3.1:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def get_dad_joke(style: str = "classic", audience: str = "family") -> dict:
    """
    Get a dad joke based on style and audience preferences.
    
    Use this tool when users ask for jokes, want to lighten the mood, or request humor.
    This function provides context-appropriate dad jokes for different situations.
    
    Args:
        style: Type of joke style (classic, wordplay, oneliners, silly)
        audience: Target audience (family, kids, adults, workplace)
    """
    print(f"--- Tool: get_dad_joke called with style='{style}', audience='{audience}' ---")
    
    # Organize jokes by actual categories that match parameters
    joke_categories = {
        "classic": [
            "Why did the chicken cross the road? To get to the other side!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a factory that makes okay products? A satisfactory!"
        ],
        "wordplay": [
            "What do you call a belt made of watches? A waist of time.",
            "What do you call fake spaghetti? An impasta!",
            "I wondered why the baseball kept getting bigger. Then it hit me.",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!"
        ],
        "oneliners": [
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "I used to hate facial hair, but then it grew on me."
        ],
        "silly": [
            "What do you call a sleeping bull? A bulldozer!",
            "Why do fish live in salt water? Because pepper makes them sneeze!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
    }
    
    # Select jokes based on style, fallback to classic if unknown style
    available_jokes = joke_categories.get(style.lower(), joke_categories["classic"])
    selected_joke = random.choice(available_jokes)
    
    print(f"--- Tool: get_dad_joke returning joke from '{style}' category for '{audience}' audience ---")
    
    return {
        "joke": selected_joke,
        "style": style,
        "audience": audience,
        "status": "success",
        "category": style.lower(),
        "source": "dad_joke_collection"
    }


root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Dad joke agent",
    instruction="""
    You are a helpful assistant that specializes in telling dad jokes to brighten conversations.
    
    Use the get_dad_joke tool when:
    - Users explicitly request jokes or humor
    - You want to lighten the mood in conversation
    - Users seem stressed and could use a laugh
    - Conversation needs a fun, light-hearted element
    
    The get_dad_joke tool accepts two parameters:
    - style: Choose from "classic", "wordplay", "oneliners", or "silly" based on user preference or context
    - audience: Choose from "family", "kids", "adults", or "workplace" to match the appropriate audience
    
    When users don't specify preferences, default to style="classic" and audience="family".
    
    Always deliver jokes with enthusiasm and consider asking if they'd like another joke or a different style.
    You can suggest different joke styles if users want variety.
    """,
    tools=[get_dad_joke],
)
