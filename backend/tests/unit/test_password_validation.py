"""
Test cases for password validation - CHARACTER-based validation.

Password validation is based on CHARACTER count (8-50 chars), not bytes.
bcrypt's 72-byte limit is handled internally by truncation.
"""
import pytest
from pydantic import ValidationError


class TestPasswordCharacterValidation:
    """Test password validation based on characters."""
    
    def test_simple_password_valid(self):
        """Simple password like 'Aa@12345678' should be valid."""
        from src.schemas import CreateUserRequest
        
        password = "Aa@12345678"  # 11 characters
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Test User",
            age=20
        )
        assert user.password == password
        assert len(user.password) == 11
    
    def test_ascii_password_within_limit(self):
        """ASCII password within character limit should be valid."""
        from src.schemas import CreateUserRequest
        
        password = "MyPassword123!"  # 14 characters
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Test User",
            age=20
        )
        assert len(user.password) == 14
    
    def test_unicode_password_valid(self):
        """Unicode password within character limit should be valid."""
        from src.schemas import CreateUserRequest
        
        # Vietnamese password
        password = "mậtkhẩubảomật12"
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Ngọc Phạn",
            age=20
        )
        assert len(user.password) == len(password)
    
    def test_long_unicode_password_valid(self):
        """Long Unicode password (up to 50 chars) should be valid."""
        from src.schemas import CreateUserRequest
        
        # 40 character Vietnamese password
        password = "mậtkhẩu" * 5 + "12345"  # 40 chars
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Test User",
            age=20
        )
        assert len(user.password) == 40
    
    def test_password_hashing_handles_unicode(self):
        """Password hashing should handle Unicode passwords correctly."""
        from src.utils.bcrypt_compat import get_password_hash, verify_password
        
        password = "Aa@12345678"
        
        hashed = get_password_hash(password)
        assert hashed is not None
        assert hashed != password
        assert hashed.startswith("$2")  # bcrypt hash prefix
        
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False
    
    def test_vietnamese_password_hashing(self):
        """Vietnamese password should hash and verify correctly."""
        from src.utils.bcrypt_compat import get_password_hash, verify_password
        
        password = "mậtkhẩubảomật123"
        
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True
    
    def test_long_password_truncation(self):
        """Long passwords should be truncated at 72 bytes internally."""
        from src.utils.bcrypt_compat import get_password_hash, verify_password
        
        # Create password longer than 72 bytes
        password = "a" * 100  # 100 bytes
        
        # Should hash without error
        hashed = get_password_hash(password)
        assert hashed is not None
        
        # Should verify correctly
        assert verify_password(password, hashed) is True
    
    def test_password_min_length(self):
        """Password minimum length should be 8 characters."""
        from src.schemas import CreateUserRequest
        
        with pytest.raises(ValidationError):
            CreateUserRequest(
                email="test@example.com",
                password="1234567",  # 7 chars - too short
                full_name="Test User",
                age=20
            )
    
    def test_password_max_length(self):
        """Password maximum length should be 50 characters."""
        from src.schemas import CreateUserRequest
        
        with pytest.raises(ValidationError):
            CreateUserRequest(
                email="test@example.com",
                password="a" * 51,  # 51 chars - too long
                full_name="Test User",
                age=20
            )
    
    def test_password_exactly_8_chars(self):
        """Password with exactly 8 characters should be valid."""
        from src.schemas import CreateUserRequest
        
        password = "Pass1234"  # Exactly 8 chars
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Test User",
            age=20
        )
        assert len(user.password) == 8
    
    def test_password_exactly_50_chars(self):
        """Password with exactly 50 characters should be valid."""
        from src.schemas import CreateUserRequest
        
        password = "a" * 50  # Exactly 50 chars
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Test User",
            age=20
        )
        assert len(user.password) == 50
    
    def test_emoji_password(self):
        """Emoji password should validate by character count."""
        from src.schemas import CreateUserRequest
        
        password = "🔐🔐🔐pass123"
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Test User",
            age=20
        )
        assert len(user.password) == len(password)
        assert len(user.password) >= 8  # At least 8 chars


class TestPasswordHashingConsistency:
    """Test that password hashing is consistent."""
    
    def test_same_password_verifies_correctly(self):
        """Same password should always verify against its hash."""
        from src.utils.bcrypt_compat import get_password_hash, verify_password
        
        passwords = [
            "Aa@12345678",
            "simple12345",
            "mậtkhẩu12345",
            "パスワード12345",
            "🔐secure🔐123",
            "mixedViệt123",
        ]
        
        for password in passwords:
            hashed = get_password_hash(password)
            assert verify_password(password, hashed), f"Failed for: {password}"
    
    def test_different_passwords_different_hashes(self):
        """Different passwords should produce different hashes."""
        from src.utils.bcrypt_compat import get_password_hash
        
        hash1 = get_password_hash("password123")
        hash2 = get_password_hash("password456")
        
        assert hash1 != hash2
    
    def test_same_password_different_hashes(self):
        """Same password should produce different hashes (due to salt)."""
        from src.utils.bcrypt_compat import get_password_hash
        
        password = "Aa@12345678"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different due to random salt
        assert hash1 != hash2
    
    def test_truncated_passwords_match(self):
        """Passwords truncated at 72 bytes should match."""
        from src.utils.bcrypt_compat import get_password_hash, verify_password
        
        # Create password longer than 72 bytes
        password = "mậtkhẩu" * 20  # ~420 bytes
        
        hashed = get_password_hash(password)
        
        # Original should verify
        assert verify_password(password, hashed)
        
        # Truncated version should also verify
        truncated = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        assert verify_password(truncated, hashed)


class TestValidatePasswordLength:
    """Test validate_password_length function."""
    
    def test_valid_password_length(self):
        """Valid password length should not raise."""
        from src.utils.bcrypt_compat import validate_password_length
        
        # Should not raise
        validate_password_length("Aa@12345678")
        validate_password_length("a" * 50)
        validate_password_length("mậtkhẩu123")
    
    def test_password_too_short(self):
        """Password too short should raise ValueError."""
        from src.utils.bcrypt_compat import validate_password_length
        
        with pytest.raises(ValueError) as exc_info:
            validate_password_length("short")
        
        assert "too short" in str(exc_info.value).lower()
    
    def test_password_too_long(self):
        """Password too long should raise ValueError."""
        from src.utils.bcrypt_compat import validate_password_length
        
        with pytest.raises(ValueError) as exc_info:
            validate_password_length("a" * 51)
        
        assert "too long" in str(exc_info.value).lower()
