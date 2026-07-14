"""
Authentication & Authorization Module for SmartCampusAIA.
Implements secure password hashing with bcrypt, strong password validation,
registration, user authentication, and profile updates.
"""

import re
import uuid
import bcrypt
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

from utils.database import load_json, save_json, USERS_FILE, log_activity


def hash_password(password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a stored bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validates password strength:
    - Min 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
        
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
        
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
        
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
        
    return True, "Strong password."


def register_user(name: str, email: str, username: str, password: str, confirm_password: str) -> Tuple[bool, str]:
    """
    Registers a new user inside the JSON database with validation.
    """
    # Empty field checks
    name = name.strip()
    email = email.strip().lower()
    username = username.strip().lower()
    
    if not name or not email or not username or not password or not confirm_password:
        return False, "All fields are required."
        
    if password != confirm_password:
        return False, "Passwords do not match."

    # Validate email format
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return False, "Invalid email format."

    # Validate username format (alphanumeric and underscores)
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."

    # Validate password strength
    is_strong, strength_msg = validate_password_strength(password)
    if not is_strong:
        return False, strength_msg

    # Load users db
    data = load_json(USERS_FILE, {"users": []})
    users = data.get("users", [])

    # Check for duplicates
    for u in users:
        if u["username"] == username:
            return False, "Username is already taken."
        if u["email"] == email:
            return False, "Email is already registered."

    # Create new user
    hashed = hash_password(password)
    new_user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "username": username,
        "password": hashed,
        "created_at": datetime.now().isoformat()
    }
    
    users.append(new_user)
    data["users"] = users
    
    if save_json(USERS_FILE, data):
        log_activity(username, "Register", f"User {username} successfully registered.")
        return True, "Registration successful! You can now log in."
    else:
        return False, "Failed to save user details. Please try again."


def authenticate_user(username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticates a user by username or email and verifies password.
    Returns the user data (excluding password hash) on success, None on failure.
    """
    username_or_email = username_or_email.strip().lower()
    if not username_or_email or not password:
        return None

    data = load_json(USERS_FILE, {"users": []})
    users = data.get("users", [])

    for u in users:
        if u["username"] == username_or_email or u["email"] == username_or_email:
            if check_password(password, u["password"]):
                # Log success
                log_activity(u["username"], "Login Success", f"User logged in successfully.")
                # Return user data without password hash
                user_copy = u.copy()
                del user_copy["password"]
                return user_copy
            else:
                log_activity(username_or_email, "Login Failure", "Incorrect password attempt.")
                return None
                
    log_activity(username_or_email, "Login Failure", "User not found.")
    return None


def update_profile(user_id: str, name: str, email: str, password: Optional[str] = None) -> Tuple[bool, str]:
    """
    Updates user details. If password is provided, verifies, hashes, and updates it.
    """
    name = name.strip()
    email = email.strip().lower()
    
    if not name or not email:
        return False, "Name and Email cannot be empty."

    data = load_json(USERS_FILE, {"users": []})
    users = data.get("users", [])

    # Find the user
    user_idx = -1
    for i, u in enumerate(users):
        if u["id"] == user_id:
            user_idx = i
            break

    if user_idx == -1:
        return False, "User not found."

    # Check for duplicate email in other accounts
    for i, u in enumerate(users):
        if i != user_idx and u["email"] == email:
            return False, "Email is already taken by another account."

    current_user = users[user_idx]
    current_user["name"] = name
    current_user["email"] = email

    if password:
        is_strong, strength_msg = validate_password_strength(password)
        if not is_strong:
            return False, strength_msg
        current_user["password"] = hash_password(password)

    users[user_idx] = current_user
    data["users"] = users

    if save_json(USERS_FILE, data):
        log_activity(current_user["username"], "Profile Update", "Updated user profile details.")
        return True, "Profile updated successfully."
    return False, "Failed to save profile changes."


def delete_user(user_id: str) -> bool:
    """
    Permanently deletes a user record from the database.
    """
    data = load_json(USERS_FILE, {"users": []})
    users = data.get("users", [])
    
    original_len = len(users)
    updated_users = [u for u in users if u["id"] != user_id]
    
    if len(updated_users) == original_len:
        return False
        
    data["users"] = updated_users
    if save_json(USERS_FILE, data):
        # We don't have the username handy unless we search, but logging it as System/ID delete is fine
        log_activity("system", "User Delete", f"Deleted user ID: {user_id}")
        return True
    return False
