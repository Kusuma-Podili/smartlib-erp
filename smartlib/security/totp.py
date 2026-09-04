"""RFC 6238 Time-Based One-Time Password (TOTP) & RFC 4226 HOTP Engine."""

import hmac
import hashlib
import time
import struct
import base64
import os
from typing import Optional


class HotpEngine:
    """RFC 4226 HMAC-Based One-Time Password (HOTP)."""

    @staticmethod
    def generate_hotp(secret: bytes, counter: int, digits: int = 6) -> str:
        msg = struct.pack(">Q", counter)
        h = hmac.new(secret, msg, hashlib.sha1).digest()
        offset = h[-1] & 0x0F
        binary = struct.unpack(">I", h[offset:offset+4])[0] & 0x7FFFFFFF
        token = binary % (10 ** digits)
        return f"{token:0{digits}d}"


class TotpEngine:
    """RFC 6238 Time-Based One-Time Password (TOTP) with 30s window."""

    @staticmethod
    def generate_secret(length: int = 20) -> str:
        return base64.b32encode(os.urandom(length)).decode("utf-8")

    @classmethod
    def generate_totp(cls, base32_secret: str, time_step: int = 30, digits: int = 6) -> str:
        key = base64.b32decode(base32_secret.upper())
        counter = int(time.time() // time_step)
        return HotpEngine.generate_hotp(key, counter, digits=digits)

    @classmethod
    def verify_totp(cls, base32_secret: str, token: str, tolerance: int = 1, time_step: int = 30) -> bool:
        key = base64.b32decode(base32_secret.upper())
        current_step = int(time.time() // time_step)
        for step_offset in range(-tolerance, tolerance + 1):
            expected = HotpEngine.generate_hotp(key, current_step + step_offset, digits=len(token))
            if hmac.compare_digest(expected, token.strip()):
                return True
        return False

    @classmethod
    def get_provisioning_uri(cls, account_name: str, base32_secret: str, issuer: str = "SmartLib ERP") -> str:
        import urllib.parse
        acc = urllib.parse.quote(account_name)
        iss = urllib.parse.quote(issuer)
        return f"otpauth://totp/{iss}:{acc}?secret={base32_secret}&issuer={iss}&algorithm=SHA1&digits=6&period=30"
