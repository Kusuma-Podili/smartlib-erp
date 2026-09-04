"""Persistent Identifier (Handle / DOI) Service."""

from typing import Optional, Dict


class HandleService:
    """Mints and resolves persistent handles for institutional repository records."""

    def __init__(self, prefix: str = "10.5072/smartlib"):
        self.prefix = prefix
        self.registry: Dict[str, str] = {}

    def mint_handle(self, item_id: str, target_url: str) -> str:
        handle = f"{self.prefix}/{item_id.lower()}"
        self.registry[handle] = target_url
        return handle

    def resolve_handle(self, handle: str) -> Optional[str]:
        return self.registry.get(handle)
