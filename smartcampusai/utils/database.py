"""
Database Utility Module for SmartCampusAIA.
Handles atomic reads/writes for JSON files, user registration, authentication,
profile updates, and campus activity logs.
"""

import os
import json
import uuid
import logging
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")

# Ensure database directory exists
os.makedirs(DB_DIR, exist_ok=True)

# File Paths
USERS_FILE = os.path.join(DB_DIR, "users.json")
ACTIVITY_FILE = os.path.join(DB_DIR, "activity.json")
SETTINGS_FILE = os.path.join(DB_DIR, "settings.json")


def load_json(file_path: str, default_data: Any = None) -> Any:
    """
    Safely load a JSON file. If it doesn't exist or is corrupted,
    it returns the default data and attempts to create/restore the file.
    """
    if default_data is None:
        default_data = {}

    if not os.path.exists(file_path):
        logger.info(f"File {file_path} does not exist. Creating with default data.")
        save_json(file_path, default_data)
        return default_data

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"JSON corruption detected in {file_path}: {e}")
        # Perform corruption recovery: Rename corrupted file to .corrupted and write default
        backup_path = file_path + ".corrupted"
        try:
            if os.path.exists(file_path):
                os.replace(file_path, backup_path)
                logger.info(f"Backup of corrupted file saved to {backup_path}")
        except Exception as replace_err:
            logger.error(f"Failed to backup corrupted file: {replace_err}")
        
        save_json(file_path, default_data)
        return default_data
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return default_data


def save_json(file_path: str, data: Any) -> bool:
    """
    Saves data to a JSON file atomically using a temporary file.
    This prevents corruption during sudden execution terminations.
    """
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    try:
        # Write to temporary file first
        with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            temp_name = f.name
        
        # Replace original file atomically
        os.replace(temp_name, file_path)
        return True
    except Exception as e:
        logger.error(f"Atomic write failed for {file_path}: {e}")
        # Clean up temp file if it still exists
        if "temp_name" in locals() and os.path.exists(temp_name):
            try:
                os.remove(temp_name)
            except Exception as clean_err:
                logger.error(f"Failed to clean up temp file: {clean_err}")
        return False


# --- Activity Log Utilities ---

def log_activity(username: str, action: str, details: str) -> None:
    """Logs user actions and campus events to activity.json."""
    data = load_json(ACTIVITY_FILE, {"activities": []})
    new_activity = {
        "id": str(uuid.uuid4()),
        "username": username,
        "action": action,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    data["activities"].insert(0, new_activity)  # Keep recent activities first
    # Cap at 100 entries to prevent files from growing too large
    data["activities"] = data["activities"][:100]
    save_json(ACTIVITY_FILE, data)


# --- Initialize Default Mock Data ---

def initialize_database() -> None:
    """Initializes database files with default structural templates and mock campus data."""
    # Initialize Users
    load_json(USERS_FILE, {"users": []})
    
    # Initialize Activities
    load_json(ACTIVITY_FILE, {"activities": []})

    # Initialize Campus Data & Settings
    default_settings = {
        "system": {
            "theme": "dark",
            "openai_model": "gpt-4o-mini",
            "campus_name": "Smart Campus Institute of AI"
        },
        "students": [
            {
                "id": "STU001",
                "name": "Alex Mercer",
                "email": "alex@smartcampus.edu",
                "department": "Computer Science",
                "gpa": 3.8,
                "status": "Active"
            },
            {
                "id": "STU002",
                "name": "Sarah Connor",
                "email": "sarah@smartcampus.edu",
                "department": "Cybernetics",
                "gpa": 3.9,
                "status": "Active"
            },
            {
                "id": "STU003",
                "name": "Bruce Wayne",
                "email": "bruce@smartcampus.edu",
                "department": "Business & Engineering",
                "gpa": 3.5,
                "status": "On Leave"
            },
            {
                "id": "STU004",
                "name": "Diana Prince",
                "email": "diana@smartcampus.edu",
                "department": "Archaeology",
                "gpa": 4.0,
                "status": "Active"
            },
            {
                "id": "STU005",
                "name": "Barry Allen",
                "email": "barry@smartcampus.edu",
                "department": "Chemistry & Forensics",
                "gpa": 3.2,
                "status": "Active"
            }
        ],
        "faculty": [
            {
                "id": "FAC001",
                "name": "Dr. Alan Turing",
                "email": "turing@smartcampus.edu",
                "department": "Computer Science",
                "designation": "Professor & Head",
                "office": "Room 401"
            },
            {
                "id": "FAC002",
                "name": "Dr. Ada Lovelace",
                "email": "lovelace@smartcampus.edu",
                "department": "Mathematics",
                "designation": "Associate Professor",
                "office": "Room 302"
            },
            {
                "id": "FAC003",
                "name": "Dr. Richard Feynman",
                "email": "feynman@smartcampus.edu",
                "department": "Physics",
                "designation": "Professor",
                "office": "Room 105"
            },
            {
                "id": "FAC004",
                "name": "Dr. Marie Curie",
                "email": "curie@smartcampus.edu",
                "department": "Chemistry",
                "designation": "Professor",
                "office": "Room 204"
            }
        ],
        "attendance": [
            {"date": "2026-07-10", "present": 420, "absent": 30, "late": 10},
            {"date": "2026-07-11", "present": 415, "absent": 32, "late": 13},
            {"date": "2026-07-12", "present": 435, "absent": 15, "late": 10},
            {"date": "2026-07-13", "present": 440, "absent": 12, "late": 8},
            {"date": "2026-07-14", "present": 438, "absent": 14, "late": 8}
        ]
    }
    load_json(SETTINGS_FILE, default_settings)


# Initialize databases immediately
initialize_database()
