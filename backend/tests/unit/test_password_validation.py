"""
Test cases for password validation - character-based vs byte-based.

Issue: bcrypt has a 72-byte limit, but validation should be based on 
character count, not byte count. Unicode characters (like Vietnamese) 
can take 2-4 bytes per character.

Solution: Limit password to 24 characters max, which ensures even
3-byte Unicode characters stay within 72 bytes (24 * 3 = 72).
"""
import pytest
from pydantic import ValidationError


class TestPasswordCharacterValidation:
    """Test password validation based on characters, not bytes."""
    
    def test_ascii_password_within_limit(self):
        """ASCII password within character limit should be valid."""
        from src.schemas import CreateUserRequest
        
        # 24 ASCII characters = 24 bytes (within both limits)
        password = "a" * 16 + "12345678"  # 24 chars with letters and numbers
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Test User",
            age=20
        )
        assert len(user.password) == 24
    
    def test_unicode_password_within_character_limit(self):
        """Unicode password within character limit should be valid.
        
        This is the key test case - Vietnamese characters take 3 bytes each.
        A 24-character Vietnamese password = 72 bytes (at bcrypt limit).
        """
        from src.schemas import CreateUserRequest
        
        # 16 Vietnamese chars + 8 ASCII = 24 chars total
        # Vietnamese: ~48 bytes, ASCII: 8 bytes = ~56 bytes (within limit)
        password = "mậtkhẩu12345678"  # Mix of Vietnamese and ASCII
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Ngọc Phạn",
            age=20
        )
        # Should validate based on character count, not bytes
        assert len(user.password) <= 24  # Character limit
    
    def test_vietnamese_password_within_new_limit(self):
        """Vietnamese password within 24 char limit should work.
        
        24 Vietnamese chars * 3 bytes = 72 bytes = exactly at bcrypt limit.
        """
        from src.schemas import CreateUserRequest
        
        # Vietnamese password: each char is ~3 bytes
        password = "mậtkhẩubảomật12"  # 15 chars, mix of Vietnamese and numbers
        byte_count = len(password.encode('utf-8'))
        char_count = len(password)
        
        print(f"Password: {password}")
        print(f"Character count: {char_count}")
        print(f"Byte count: {byte_count}")
        
        # This should NOT fail validation
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Ngọc Phạn",
            age=20
        )
        assert char_count <= 24  # Within character limit
    
    def test_password_hashing_handles_unicode(self):
        """Password hashing should handle Unicode passwords correctly."""
        from src.middleware.auth import get_password_hash, verify_password
        
        # Vietnamese password
        password = "mậtkhẩubảomật12"
        
        # Should hash without error
        hashed = get_password_hash(password)
        assert hashed is not None
        assert hashed != password
        
        # Should verify correctly
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False
    
    def test_long_unicode_password_truncation(self):
        """Long Unicode passwords should be truncated at byte level for bcrypt.
        
        bcrypt limit is 72 bytes, so we truncate at byte level.
        But validation should still be at character level.
        """
        from src.middleware.auth import get_password_hash, verify_password
        
        # Create a password that's 30 Vietnamese chars = ~90 bytes
        password = "mậtkhẩu" * 5  # 35 chars, ~105 bytes
        byte_count = len(password.encode('utf-8'))
        
        print(f"Original password bytes: {byte_count}")
        
        # Should hash without error (truncates internally)
        hashed = get_password_hash(password)
        assert hashed is not None
        
        # Should verify the truncated version
        assert verify_password(password, hashed) is True
    
    def test_password_min_length_characters(self):
        """Password minimum length should be based on characters."""
        from src.schemas import CreateUserRequest
        
        # 7 characters - should fail (min is 8)
        with pytest.raises(ValidationError) as exc_info:
            CreateUserRequest(
                email="test@example.com",
                password="1234567",  # 7 chars
                full_name="Test User",
                age=20
            )
        assert "min_length" in str(exc_info.value).lower() or "at least 8" in str(exc_info.value).lower()
    
    def test_password_max_length_characters(self):
        """Password maximum length should be based on characters (24 max)."""
        from src.schemas import CreateUserRequest
        
        # 25 characters - should fail (max is 24)
        with pytest.raises(ValidationError):
            CreateUserRequest(
                email="test@example.com",
                password="a" * 25,  # 25 chars
                full_name="Test User",
                age=20
            )
    
    def test_emoji_password(self):
        """Emoji password (4 bytes per char) should validate by character count."""
        from src.schemas import CreateUserRequest
        
        # Emojis are 4 bytes each
        # 5 emojis + 7 chars = 12 chars total (within 24 limit)
        password = "🔐" * 3 + "pass1234"  # 11 chars total
        byte_count = len(password.encode('utf-8'))
        char_count = len(password)
        
        print(f"Emoji password bytes: {byte_count}, chars: {char_count}")
        
        user = CreateUserRequest(
            email="test@example.com",
            password=password,
            full_name="Test User",
            age=20
        )
        assert len(user.password) == char_count


class TestPasswordHashingConsistency:
    """Test that password hashing is consistent for Unicode."""
    
    def test_same_password_verifies_correctly(self):
        """Same password should always verify against its hash."""
        from src.middleware.auth import get_password_hash, verify_password
        
        passwords = [
            "simple12345",
            "mậtkhẩu12345",
            "パスワード12345",
            "🔐secure🔐1",
            "mixedViệt123",
        ]
        
        for password in passwords:
            hashed = get_password_hash(password)
            assert verify_password(password, hashed), f"Failed for: {password}"
    
    def test_truncated_passwords_match(self):
        """Passwords truncated at 72 bytes should match."""
        from src.middleware.auth import get_password_hash, verify_password
        
        # Create password longer than 72 bytes
        base = "mậtkhẩu"  # 7 chars, 21 bytes
        password = base * 10  # 70 chars, 210 bytes
        
        hashed = get_password_hash(password)
        
        # Original should verify
        assert verify_password(password, hashed)
        
        # Truncated version should also verify (same first 72 bytes)
        truncated = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        assert verify_password(truncated, hashed)
