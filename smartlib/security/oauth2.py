"""OAuth2 and OpenID Connect (OIDC) Token Issuer."""

import json
import base64
import hmac
import hashlib
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class JwtPayload:
    sub: str
    name: str
    role: str
    iss: str = "https://smartlib.org/auth"
    exp_seconds: int = 3600


class OAuth2TokenIssuer:
    """Signs and verifies HMAC-SHA256 JWT tokens."""

    def __init__(self, secret_key: str = "SmartLibSecretKeyForJwtSigning"):
        self.secret = secret_key.encode("utf-8")

    def _b64encode(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    def _b64decode(self, s: str) -> bytes:
        rem = len(s) % 4
        if rem > 0:
            s += "=" * (4 - rem)
        return base64.urlsafe_b64decode(s)

    def issue_token(self, payload: JwtPayload) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        now = int(time.time())
        claims = {
            "iss": payload.iss,
            "sub": payload.sub,
            "name": payload.name,
            "role": payload.role,
            "iat": now,
            "exp": now + payload.exp_seconds
        }

        h_bytes = self._b64encode(json.dumps(header).encode("utf-8"))
        c_bytes = self._b64encode(json.dumps(claims).encode("utf-8"))
        msg = f"{h_bytes}.{c_bytes}".encode("utf-8")
        sig = hmac.new(self.secret, msg, hashlib.sha256).digest()
        s_bytes = self._b64encode(sig)

        return f"{h_bytes}.{c_bytes}.{s_bytes}"

    def verify_token(self, token_str: str) -> Optional[Dict[str, Any]]:
        parts = token_str.split(".")
        if len(parts) != 3:
            return None
        h_part, c_part, s_part = parts
        msg = f"{h_part}.{c_part}".encode("utf-8")
        expected_sig = self._b64encode(hmac.new(self.secret, msg, hashlib.sha256).digest())

        if not hmac.compare_digest(expected_sig, s_part):
            return None

        claims = json.loads(self._b64decode(c_part).decode("utf-8"))
        if time.time() > claims.get("exp", 0):
            return None

        return claims
