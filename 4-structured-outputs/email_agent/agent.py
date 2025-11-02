from typing import Literal, List
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


# --- Tools ---
def get_current_time() -> dict:
    from datetime import datetime
    return {"current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


# --- Output Schema ---
class EmailContent(BaseModel):
    subject: str = Field(min_length=5, max_length=120)
    body: str = Field(min_length=50)
    tone: Literal["formal", "neutral", "friendly"] = "neutral"
    priority: Literal["low", "normal", "high"] = "normal"
    attachments: List[str] = Field(default_factory=list)


root_agent = LlmAgent(
    name="email_agent",
    model="gemini-2.0-flash",
    description="Generates professional emails with structured subject, body, tone, priority, and attachments.",
    instruction="""
        You are an Email Generation Assistant.

        Return ONLY valid JSON for the following schema:
        {
          "subject": "...",
          "body": "...",
          "tone": "formal|neutral|friendly",
          "priority": "low|normal|high",
          "attachments": ["..."]
        }

        Guidelines:
        - Subject: concise, informative.
        - Body: greeting, concise content, closing, signature.
        - Tone: match the user's request (default neutral).
        - Priority: infer from urgency cues; use "normal" by default.
        - Attachments: suggest filenames if relevant, else an empty list.

        Do not include any explanations, markdown, or code blocks—JSON only.
    """,
    output_schema=EmailContent,
    output_key="email",
)
