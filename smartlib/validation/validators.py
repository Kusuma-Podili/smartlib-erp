"""
Enterprise field validators (ISBN-10, ISBN-13, Email, Phone, Passwords).
"""

import re
from typing import Optional, Tuple
from smartlib.errors import ValidationError

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_.-]{3,30}$")

def validate_email(email: str) -> str:
    """Validate RFC compliant email string."""
    if not email or not isinstance(email, str):
        raise ValidationError("Email address cannot be empty.", {"email": "Required field."})
    clean = email.strip().lower()
    if not EMAIL_REGEX.match(clean) or len(clean) > 255:
        raise ValidationError(f"Invalid email format: '{email}'.", {"email": "Must be a valid email format."})
    return clean

def validate_phone(phone: Optional[str]) -> Optional[str]:
    """Validate international telephone number format."""
    if not phone:
        return None
    cleaned = re.sub(r"[\s\-()]", "", phone.strip())
    if not PHONE_REGEX.match(cleaned):
        raise ValidationError(f"Invalid phone number format: '{phone}'.", {"phone": "Must contain 7 to 15 digits."})
    return cleaned

def validate_username(username: str) -> str:
    """Validate username alphanumerics and length."""
    if not username or not isinstance(username, str):
        raise ValidationError("Username is required.", {"username": "Required field."})
    clean = username.strip().lower()
    if not USERNAME_REGEX.match(clean):
        raise ValidationError(
            f"Invalid username '{username}'. Must be 3-30 characters (letters, numbers, underscores, dots, dashes).",
            {"username": "3-30 alphanumeric characters only."}
        )
    return clean

def validate_password_complexity(password: str, min_length: int = 8) -> bool:
    """Ensure password satisfies enterprise complexity policy."""
    errors = []
    if len(password) < min_length:
        errors.append(f"Must be at least {min_length} characters long.")
    if not any(c.isupper() for c in password):
        errors.append("Must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        errors.append("Must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in password):
        errors.append("Must contain at least one digit.")
    if not any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password):
        errors.append("Must contain at least one special character.")
    if errors:
        raise ValidationError("Password does not meet complexity requirements.", {"password": " ".join(errors)})
    return True

def validate_isbn(isbn: str) -> str:
    """Validate ISBN-10 or ISBN-13 format with checksum validation."""
    cleaned = re.sub(r"[- ]", "", isbn.strip()).upper()
    if len(cleaned) == 10:
        # ISBN-10 Checksum
        total = 0
        for i in range(9):
            if not cleaned[i].isdigit():
                raise ValidationError("Invalid ISBN-10 format: non-digit characters in body.", {"isbn": "Invalid ISBN-10."})
            total += int(cleaned[i]) * (10 - i)
        last = cleaned[9]
        if last == "X":
            total += 10
        elif last.isdigit():
            total += int(last)
        else:
            raise ValidationError("Invalid ISBN-10 check digit.", {"isbn": "Invalid ISBN-10."})
        if total % 11 != 0:
            raise ValidationError("ISBN-10 checksum validation failed.", {"isbn": "Checksum mismatch."})
        return cleaned

    elif len(cleaned) == 13:
        # ISBN-13 Checksum
        if not cleaned.isdigit():
            raise ValidationError("Invalid ISBN-13 format: must contain only digits.", {"isbn": "Invalid ISBN-13."})
        total = sum(int(cleaned[i]) * (1 if i % 2 == 0 else 3) for i in range(12))
        check_digit = (10 - (total % 10)) % 10
        if int(cleaned[12]) != check_digit:
            raise ValidationError("ISBN-13 checksum validation failed.", {"isbn": "Checksum mismatch."})
        return cleaned
    else:
        raise ValidationError(f"ISBN must be 10 or 13 digits (received {len(cleaned)} digits).", {"isbn": "Must be 10 or 13 digits."})

def validate_positive_number(value: float, field_name: str = "value") -> float:
    """Ensure numeric value is non-negative."""
    if value < 0:
        raise ValidationError(f"{field_name} must be greater than or equal to 0.", {field_name: "Cannot be negative."})
    return value
