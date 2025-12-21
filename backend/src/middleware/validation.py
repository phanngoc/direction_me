"""
Input Validation Middleware
"""

from fastapi import Request, HTTPException, status
from pydantic import BaseModel, validator, ValidationError
from typing import Optional, Tuple
import re


class EmailValidator:
    """Email validation"""

    @staticmethod
    def is_valid(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


class PasswordValidator:
    """Password validation"""

    @staticmethod
    def is_valid(password: str) -> Tuple[bool, str]:
        """
        Validate password strength

        Returns:
            Tuple of (is_valid, message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if len(password) > 50:
            return False, "Password must not exceed 50 characters"

        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"

        return True, "Password is valid"


class InputSanitizer:
    """Sanitize user inputs to prevent injection attacks"""

    @staticmethod
    def sanitize_string(value: str) -> str:
        """Remove potentially dangerous characters"""
        # Remove null bytes
        value = value.replace('\x00', '')

        # Trim whitespace
        value = value.strip()

        return value

    @staticmethod
    def sanitize_sql(value: str) -> str:
        """Escape SQL special characters"""
        # This is a basic example - use proper ORM/parameterized queries in production
        dangerous_chars = ["'", '"', ';', '--', '/*', '*/']
        for char in dangerous_chars:
            value = value.replace(char, '')
        return value


async def validate_request_size(request: Request, call_next):
    """Middleware to validate request size"""
    max_size = 10 * 1024 * 1024  # 10MB

    content_length = request.headers.get('content-length')

    if content_length and int(content_length) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Request body too large. Maximum size is {max_size} bytes"
        )

    return await call_next(request)


# Validation schemas
class UserRegistrationValidation(BaseModel):
    """User registration validation schema"""
    email: str
    password: str
    full_name: str
    age: int

    @validator('email')
    def validate_email(cls, v):
        if not EmailValidator.is_valid(v):
            raise ValueError('Invalid email address')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        is_valid, message = PasswordValidator.is_valid(v)
        if not is_valid:
            raise ValueError(message)
        return v

    @validator('full_name')
    def validate_full_name(cls, v):
        v = InputSanitizer.sanitize_string(v)
        if len(v) < 2:
            raise ValueError('Full name must be at least 2 characters')
        if len(v) > 100:
            raise ValueError('Full name must not exceed 100 characters')
        return v

    @validator('age')
    def validate_age(cls, v):
        if v < 16 or v > 25:
            raise ValueError('Age must be between 16 and 25')
        return v


class AssessmentAnswerValidation(BaseModel):
    """Assessment answer validation schema"""
    question_id: str
    answer: int

    @validator('answer')
    def validate_answer(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Answer must be between 1 and 5 (Likert scale)')
        return v


def validate_uuid(uuid_string: str) -> bool:
    """Validate UUID format"""
    uuid_pattern = re.compile(
        r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$',
        re.IGNORECASE
    )
    return bool(uuid_pattern.match(uuid_string))
