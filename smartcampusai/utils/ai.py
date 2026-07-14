"""
AI Integration Module for SmartCampusAIA.
Manages communication with OpenAI-compatible API endpoints.
Provides fallback mock responses for testing and trial runs if no API key is configured.
"""

import os
import time
import logging
from typing import Generator, List, Dict, Tuple, Union
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Ensure environment is loaded
load_dotenv()

logger = logging.getLogger(__name__)


def get_api_credentials() -> Tuple[str, str, str]:
    """
    Retrieves the active API credentials.
    Priority:
    1. Custom settings in streamlit session state.
    2. Environment variables from loaded .env.
    """
    # Look for API settings in session state overrides
    api_key = st.session_state.get("custom_api_key")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY", "")
        
    model_name = st.session_state.get("custom_model_name")
    if not model_name:
        model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
        
    api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    return api_key, model_name, api_base


def test_api_connection(api_key: str, model_name: str, api_base: str) -> Tuple[bool, str]:
    """
    Tests the API key by sending a minimal completion request.
    """
    if not api_key:
        return False, "API Key is empty."
    try:
        client = OpenAI(api_key=api_key, base_url=api_base)
        # Fast cheap verification check
        client.models.list()
        return True, "Connection successful."
    except Exception as e:
        logger.error(f"API testing error: {e}")
        return False, str(e)


def generate_mock_stream(prompt: str) -> Generator[str, None, None]:
    """
    Generates streaming responses based on campus databases to simulate AI functionality
    when an API key is not configured.
    """
    prompt_lower = prompt.lower()
    
    # Context-aware mock responses based on local campus database
    if "student" in prompt_lower or "gpa" in prompt_lower:
        response = (
            "🤖 **[SmartCampus Mock AI]**\n\n"
            "Currently, there are **5 registered students** in our database.\n\n"
            "Here is a summary of our top students:\n"
            "- **Diana Prince**: GPA 4.0 (Archaeology)\n"
            "- **Sarah Connor**: GPA 3.9 (Cybernetics)\n"
            "- **Alex Mercer**: GPA 3.8 (Computer Science)\n\n"
            "Feel free to check the **Students** menu for the detailed list or to add a new record."
        )
    elif "faculty" in prompt_lower or "professor" in prompt_lower or "teacher" in prompt_lower:
        response = (
            "🤖 **[SmartCampus Mock AI]**\n\n"
            "Our academy consists of **4 distinguished faculty members**:\n"
            "- **Dr. Alan Turing** (Professor & Head of Computer Science, Office: Room 401)\n"
            "- **Dr. Ada Lovelace** (Associate Professor of Mathematics, Office: Room 302)\n"
            "- **Dr. Richard Feynman** (Professor of Physics, Office: Room 105)\n"
            "- **Dr. Marie Curie** (Professor of Chemistry, Office: Room 204)\n\n"
            "You can manage faculty info in the **Faculty** directory tab."
        )
    elif "attendance" in prompt_lower or "present" in prompt_lower or "absent" in prompt_lower:
        response = (
            "🤖 **[SmartCampus Mock AI]**\n\n"
            "According to the attendance records for today (2026-07-14):\n"
            "- **Present**: 438 students\n"
            "- **Absent**: 14 students\n"
            "- **Late**: 8 arrivals\n\n"
            "This gives us an overall attendance rate of **95.2%**. Head over to the **Attendance** panel to view trends."
        )
    elif "hello" in prompt_lower or "hi" in prompt_lower or "hey" in prompt_lower:
        response = (
            "👋 Hello! Welcome to the **SmartCampus AI Assistant**.\n\n"
            "I can help you monitor student enrollment, faculty office assignments, and class attendance statistics.\n\n"
            "*Notice: Since no OpenAI API Key was detected in settings, I am running in local mock database search mode. "
            "Please configure your OpenAI API Key in the **Settings** page to connect to GPT!*"
        )
    else:
        response = (
            "🤖 **[SmartCampus Mock AI]**\n\n"
            "I received your request: *\"" + prompt + "\"*\n\n"
            "To unlock fully conversational chat and cognitive reasoning, please supply a valid **OpenAI API Key** in the **Settings** or the `.env` file.\n\n"
            "Meanwhile, you can ask me about: **students**, **faculty**, or **attendance** data!"
        )

    # Simulate streaming letter-by-letter / word-by-word
    words = response.split(" ")
    for word in words:
        yield word + " "
        time.sleep(0.04)


def get_ai_chat_response(messages: List[Dict[str, str]], stream: bool = True) -> Union[Generator[str, None, None], str]:
    """
    Sends the conversation history to OpenAI and streams or returns the string response.
    Falls back to generate_mock_stream if no valid API key is present.
    """
    api_key, model_name, api_base = get_api_credentials()
    
    if not api_key:
        last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return generate_mock_stream(last_user_message)
        
    try:
        client = OpenAI(api_key=api_key, base_url=api_base)
        
        # Inject system instruction to ground the AI as a campus assistant
        system_instruction = {
            "role": "system",
            "content": (
                "You are SmartCampusAIA, a premium, intelligent campus management assistant. "
                "You answer questions regarding students, faculty, timetables, and analytics. "
                "Keep responses professional, concise, structured (use markdown tables if summarizing data), "
                "and user-friendly."
            )
        }
        
        payload_messages = [system_instruction] + messages
        
        if stream:
            # Return a streaming generator
            def stream_generator():
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=payload_messages,
                        stream=True
                    )
                    for chunk in response:
                        content = chunk.choices[0].delta.content
                        if content is not None:
                            yield content
                except Exception as stream_err:
                    logger.error(f"Error during OpenAI stream response: {stream_err}")
                    yield f"\n\n**Error during streaming:** {stream_err}. Reverting to local search."
            return stream_generator()
        else:
            response = client.chat.completions.create(
                model=model_name,
                messages=payload_messages,
                stream=False
            )
            return response.choices[0].message.content or ""
            
    except Exception as e:
        logger.error(f"OpenAI completion request failed: {e}")
        # Fallback to mock streaming
        last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return generate_mock_stream(f"[API Error: {e}] {last_user_message}")
