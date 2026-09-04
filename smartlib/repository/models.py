"""Institutional Repository data models."""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import datetime


class AccessType(Enum):
    OPEN_ACCESS = "open_access"
    RESTRICTED = "restricted"
    EMBARGOED = "embargoed"


class LicenseType(Enum):
    CC_BY = "CC-BY-4.0"
    CC_BY_SA = "CC-BY-SA-4.0"
    CC_BY_NC = "CC-BY-NC-4.0"
    CC0 = "CC0-1.0"
    ALL_RIGHTS_RESERVED = "All Rights Reserved"


@dataclass
class ChecksumAuditRecord:
    id: str
    bitstream_id: str
    algorithm: str
    expected_hash: str
    actual_hash: str
    is_valid: bool
    audited_at: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass
class Bitstream:
    id: str
    repository_item_id: str
    filename: str
    mime_type: str
    size_bytes: int
    sha256_checksum: str
    storage_path: str
    access_type: AccessType = AccessType.OPEN_ACCESS
    embargo_until: Optional[datetime.date] = None


@dataclass
class RepositoryItem:
    id: str
    collection_id: str
    title: str
    authors: List[str] = field(default_factory=list)
    abstract: Optional[str] = None
    publication_date: Optional[datetime.date] = None
    handle_doi: Optional[str] = None
    license: LicenseType = LicenseType.CC_BY
    bitstreams: List[Bitstream] = field(default_factory=list)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass
class Collection:
    id: str
    community_id: str
    name: str
    description: str = ""


@dataclass
class Community:
    id: str
    name: str
    description: str = ""
