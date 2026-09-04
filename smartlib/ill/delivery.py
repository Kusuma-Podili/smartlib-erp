"""Electronic Document Delivery (EDD) secure PDF packaging and watermarking."""

import uuid
import datetime
from typing import Dict, Optional


class ElectronicDocumentDeliveryService:
    """Secures, tokenizes, and delivers digital articles to patrons."""

    def __init__(self, download_base_url: str = "http://localhost:8000/ill/download/"):
        self.download_base_url = download_base_url
        self.active_tokens: Dict[str, Dict[str, Any]] = {}

    def generate_delivery_token(self, ill_request_id: str, patron_email: str, file_path: str, max_views: int = 5, expiry_days: int = 14) -> str:
        token = str(uuid.uuid4())
        expires_at = datetime.datetime.now() + datetime.timedelta(days=expiry_days)
        self.active_tokens[token] = {
            "request_id": ill_request_id,
            "patron_email": patron_email,
            "file_path": file_path,
            "views_remaining": max_views,
            "expires_at": expires_at
        }
        return f"{self.download_base_url}{token}"

    def validate_and_consume_token(self, token: str) -> Optional[str]:
        info = self.active_tokens.get(token)
        if not info:
            return None
        if datetime.datetime.now() > info["expires_at"]:
            del self.active_tokens[token]
            return None
        if info["views_remaining"] <= 0:
            del self.active_tokens[token]
            return None

        info["views_remaining"] -= 1
        return info["file_path"]
