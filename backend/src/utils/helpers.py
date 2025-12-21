"""
Utility functions for MyWay Career Assessment System.
"""
import re
from typing import List, Dict, Any
from datetime import datetime, timedelta

# Import bcrypt functions from compatibility module
from .bcrypt_compat import (
    BCRYPT_MAX_BYTES,
    validate_password_length as validate_password_bytes,
    get_password_hash,
    verify_password,
)


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> bool:
    """Validate password strength.
    
    Password must be 8-24 characters and contain at least one letter and one number.
    Max 24 chars ensures Unicode passwords stay within bcrypt's 72-byte limit.
    """
    if len(password) < 8:
        return False
    
    if len(password) > 24:
        return False
    
    # Check for at least one letter and one number
    has_letter = re.search(r'[a-zA-Z]', password)
    has_number = re.search(r'\d', password)
    
    return has_letter is not None and has_number is not None


def normalize_score(score: float, min_val: float = 0, max_val: float = 100) -> float:
    """Normalize score to 0-100 range."""
    return max(min_val, min(max_val, score))


def calculate_percentage(value: float, total: float) -> float:
    """Calculate percentage with proper handling of zero division."""
    if total == 0:
        return 0.0
    return (value / total) * 100


def format_datetime(dt: datetime) -> str:
    """Format datetime for API responses."""
    return dt.isoformat()


def parse_datetime(dt_str: str) -> datetime:
    """Parse datetime string from API requests."""
    return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))


def generate_uuid() -> str:
    """Generate a UUID string."""
    import uuid
    return str(uuid.uuid4())


def sanitize_string(text: str) -> str:
    """Sanitize string input."""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', text)
    return text.strip()


def validate_age(age: int) -> bool:
    """Validate age is within acceptable range."""
    return 16 <= age <= 25


def calculate_age_from_birthdate(birthdate: datetime) -> int:
    """Calculate age from birthdate."""
    today = datetime.now()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries."""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with default."""
    return dictionary.get(key, default)


def is_valid_uuid(uuid_string: str) -> bool:
    """Check if string is a valid UUID."""
    try:
        import uuid
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def truncate_string(text: str, max_length: int) -> str:
    """Truncate string to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_score(score: float, decimals: int = 2) -> str:
    """Format score with specified decimal places."""
    return f"{score:.{decimals}f}"


def calculate_improvement(current: float, previous: float) -> float:
    """Calculate improvement percentage."""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def get_facet_display_name(facet: str) -> str:
    """Get display name for facet code."""
    facet_names = {
        'iq_lr': 'Logical Reasoning',
        'iq_nr': 'Numerical Reasoning',
        'iq_vr': 'Verbal Reasoning',
        'iq_sr': 'Spatial Reasoning',
        'eq_empathy': 'Empathy',
        'eq_social': 'Social Skills',
        'eq_self_awareness': 'Self-Awareness',
        'eq_self_regulation': 'Self-Regulation',
        'dq_info_literacy': 'Information Literacy',
        'dq_creativity': 'Creativity',
        'dq_safety': 'Safety',
        'dq_collaboration': 'Collaboration',
        'aq_control': 'Control',
        'aq_ownership': 'Ownership',
        'aq_reach': 'Reach',
        'aq_endurance': 'Endurance'
    }
    return facet_names.get(facet, facet)


def get_category_display_name(category: str) -> str:
    """Get display name for category."""
    category_names = {
        'IQ': 'Intelligence Quotient',
        'EQ': 'Emotional Quotient',
        'DQ': 'Digital Quotient',
        'AQ': 'Adversity Quotient'
    }
    return category_names.get(category, category)


# Re-export bcrypt functions for backward compatibility
# These are imported from bcrypt_compat module
__all__ = [
    'validate_email',
    'validate_password',
    'validate_password_bytes',
    'get_password_hash',
    'verify_password',
    'normalize_score',
    'calculate_percentage',
    'format_datetime',
    'parse_datetime',
    'generate_uuid',
    'sanitize_string',
    'validate_age',
    'calculate_age_from_birthdate',
    'chunk_list',
    'merge_dicts',
    'safe_get',
    'is_valid_uuid',
    'truncate_string',
    'format_score',
    'calculate_improvement',
    'get_facet_display_name',
    'get_category_display_name',
]