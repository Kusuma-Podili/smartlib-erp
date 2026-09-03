"""
String sanitization, slug generation, and security masking utilities.
"""

import re
import html
from typing import Optional

def sanitize_input(text: Optional[str]) -> str:
    """Strip trailing spaces and escape harmful HTML entities."""
    if text is None:
        return ""
    stripped = text.strip()
    return html.escape(stripped, quote=True)

def slugify(text: str) -> str:
    """Convert text into a URL-friendly slug."""
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "-", text)

def mask_email(email: str) -> str:
    """Mask an email address for public display (e.g., j***e@domain.com)."""
    if "@" not in email:
        return email
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        masked_local = local[0] + "*"
    else:
        masked_local = local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{masked_local}@{domain}"

def mask_phone(phone: str) -> str:
    """Mask phone digits except last 4 digits."""
    cleaned = re.sub(r"\D", "", phone)
    if len(cleaned) <= 4:
        return phone
    masked = "*" * (len(cleaned) - 4) + cleaned[-4:]
    return masked

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate long text gracefully at word boundaries."""
    if not text or len(text) <= max_length:
        return text or ""
    return text[:max_length - len(suffix)].rsplit(" ", 1)[0] + suffix
