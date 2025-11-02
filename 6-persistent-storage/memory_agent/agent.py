from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types


def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Add a new reminder to the user's reminder list.
    
    This tool accepts ANY reminder text, including time specifications.
    Examples: "buy milk", "call mom at 6PM tomorrow", "meeting next Tuesday 2PM"

    Args:
        reminder: The complete reminder text including any time information
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: add_reminder called for '{reminder}' ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Add the new reminder exactly as provided
    reminders.append(reminder)

    # Update state with the new list of reminders
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Added reminder: {reminder}",
    }


def view_reminders(tool_context: ToolContext) -> dict:
    """View all current reminders.

    Args:
        tool_context: Context for accessing session state

    Returns:
        The list of reminders
    """
    print("--- Tool: view_reminders called ---")

    # Get reminders from state
    reminders = tool_context.state.get("reminders", [])

    return {"action": "view_reminders", "reminders": reminders, "count": len(reminders)}


def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    """Update an existing reminder.

    Args:
        index: The 1-based index of the reminder to update
        updated_text: The new text for the reminder
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(
        f"--- Tool: update_reminder called for index {index} with '{updated_text}' ---"
    )

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "update_reminder",
            "status": "error",
            "message": f"Could not find reminder at position {index}. Currently there are {len(reminders)} reminders.",
        }

    # Update the reminder (adjusting for 0-based indices)
    old_reminder = reminders[index - 1]
    reminders[index - 1] = updated_text

    # Update state with the modified list
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "index": index,
        "old_text": old_reminder,
        "updated_text": updated_text,
        "message": f"Updated reminder {index} from '{old_reminder}' to '{updated_text}'",
    }


def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """Delete a reminder.

    Args:
        index: The 1-based index of the reminder to delete
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: delete_reminder called for index {index} ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": f"Could not find reminder at position {index}. Currently there are {len(reminders)} reminders.",
        }

    # Remove the reminder (adjusting for 0-based indices)
    deleted_reminder = reminders.pop(index - 1)

    # Update state with the modified list
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "index": index,
        "deleted_reminder": deleted_reminder,
        "message": f"Deleted reminder {index}: '{deleted_reminder}'",
    }


def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """Update the user's name.

    Args:
        name: The new name for the user
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: update_user_name called with '{name}' ---")

    # Get current name from state
    old_name = tool_context.state.get("user_name", "")

    # Update the name in state
    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": name,
        "message": f"Updated your name to: {name}",
    }


# Create a simple persistent agent
memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.0-flash",
    description="A smart reminder agent with persistent memory that can handle any reminder text including times and dates",
    instruction="""
    You are a helpful reminder assistant that remembers information across conversations.
    
    CRITICAL: You are NOT a calendar or scheduling system. You simply store reminder TEXT that users provide.
    You MUST accept and store ANY reminder text, including those with times and dates.
    
    When users say things like:
    - "add meeting with John at 2PM Friday" → use add_reminder("meeting with John at 2PM Friday")
    - "set reminder for dentist appointment tomorrow 9am" → use add_reminder("dentist appointment tomorrow 9am")  
    - "remind me to call mom next Tuesday at 7:30pm" → use add_reminder("call mom next Tuesday at 7:30pm")
    
    You are NOT setting actual alarms or calendar events - you're just storing text reminders.
    NEVER refuse to add a reminder because it contains time information.
    
    Current user state:
    - User's name: {user_name}
    - Reminders: {reminders}
    
    Guidelines:
    1. For adding: Always use add_reminder with the complete text including any time/date info
    2. For viewing: Use view_reminders and format as numbered list  
    3. For updates/deletes: Match user intent to reminder indices using your best judgment
    4. Be friendly and use the user's name when known
    5. Normalize abbreviations (tmr→tomorrow, etc.) but keep all time information
    
    Remember: You store TEXT reminders, not actual scheduled events. Time information is just part of the text.
    """,
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Lower temperature for more consistent behavior
        max_output_tokens=1000,
    ),
)
