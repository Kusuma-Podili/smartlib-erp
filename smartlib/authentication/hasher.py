"""
Cryptographically secure password hashing and verification using PBKDF2-HMAC-SHA256.
Uses self-describing hash format: pbkdf2_sha256$iterations$salt$hash
"""

import hashlib
import os
import secrets
import hmac
from typing import Tuple

class PasswordHasher:
    def __init__(self, iterations: int = 100000, salt_bytes: int = 32):
        self.iterations = iterations
        self.salt_bytes = salt_bytes

    def hash_password(self, plain_password: str) -> Tuple[str, str]:
        """
        Generate a cryptographically random salt and hash the plain text password.
        Returns: (hash_str, salt_hex)
        """
        if not plain_password:
            raise ValueError("Password cannot be empty.")
        salt = secrets.token_bytes(self.salt_bytes)
        derived_key = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt,
            self.iterations
        )
        # Self-describing hash: pbkdf2_sha256$iterations$salt_hex$hash_hex
        formatted_hash = f"pbkdf2_sha256${self.iterations}${salt.hex()}${derived_key.hex()}"
        return formatted_hash, salt.hex()

    def verify_password(self, plain_password: str, stored_hash: str, stored_salt: str = "") -> bool:
        """
        Verify a password against stored PBKDF2 hash using constant-time comparison.
        Supports both self-describing hashes and legacy raw hex hashes.
        """
        if not plain_password or not stored_hash:
            return False
        try:
            if stored_hash.startswith("pbkdf2_sha256$"):
                parts = stored_hash.split("$")
                if len(parts) != 4:
                    return False
                _, iter_str, salt_hex, expected_hex = parts
                iterations = int(iter_str)
                salt_bytes = bytes.fromhex(salt_hex)
                computed_key = hashlib.pbkdf2_hmac(
                    "sha256",
                    plain_password.encode("utf-8"),
                    salt_bytes,
                    iterations
                )
                return hmac.compare_digest(computed_key.hex(), expected_hex)
            else:
                # Raw hex hash fallback
                salt_bytes = bytes.fromhex(stored_salt)
                computed_key = hashlib.pbkdf2_hmac(
                    "sha256",
                    plain_password.encode("utf-8"),
                    salt_bytes,
                    self.iterations
                )
                return hmac.compare_digest(computed_key.hex(), stored_hash)
        except Exception:
            return False
