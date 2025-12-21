"""
bcrypt compatibility module.

This module uses bcrypt directly instead of passlib to avoid compatibility issues
with bcrypt >= 4.x. Passlib has issues with newer bcrypt versions.

Password validation is based on CHARACTER count (not bytes) for better UX.
bcrypt's 72-byte limit is handled internally by truncation.
"""
import bcrypt

# Password validation limits (CHARACTER-based, not bytes)
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 50  # Character limit for UX

# bcrypt internal limit (bytes) - handled by truncation
BCRYPT_MAX_BYTES = 72

# For backward compatibility
pwd_context = None  # Not used anymore


def validate_password_length(password: str) -> None:
    """Validate password length by CHARACTER count.
    
    This validates the password meets minimum/maximum character requirements.
    bcrypt's 72-byte limit is handled internally by truncation, not validation.
    
    Args:
        password: The password to validate.
        
    Raises:
        ValueError: If password doesn't meet character length requirements.
    """
    char_count = len(password)
    
    if char_count < PASSWORD_MIN_LENGTH:
        raise ValueError(
            f"Password too short: {char_count} characters (min {PASSWORD_MIN_LENGTH} characters)."
        )
    
    if char_count > PASSWORD_MAX_LENGTH:
        raise ValueError(
            f"Password too long: {char_count} characters (max {PASSWORD_MAX_LENGTH} characters)."
        )


def _truncate_password(password: str) -> bytes:
    """Truncate password to 72 bytes for bcrypt compatibility.
    
    bcrypt has a hard 72-byte limit. This function handles truncation
    internally so users don't need to worry about byte limits.
    
    Args:
        password: The password string.
        
    Returns:
        Password bytes truncated to 72 bytes max.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > BCRYPT_MAX_BYTES:
        password_bytes = password_bytes[:BCRYPT_MAX_BYTES]
    return password_bytes


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt.
    
    Handles bcrypt's 72-byte limit internally by truncation.
    
    Args:
        password: The password to hash.
        
    Returns:
        The bcrypt hash of the password.
    """
    password_bytes = _truncate_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.
    
    Handles bcrypt's 72-byte limit internally by truncation.
    
    Args:
        plain_password: The plain text password to verify.
        hashed_password: The bcrypt hash to verify against.
        
    Returns:
        True if the password matches, False otherwise.
    """
    password_bytes = _truncate_password(plain_password)
    hashed_bytes = hashed_password.encode('utf-8')
    
    try:
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False
