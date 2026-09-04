"""Content-Addressable Bitstream Storage and Fixity Auditing Service."""

import hashlib
import os
from typing import Optional, List
from .models import Bitstream, ChecksumAuditRecord


class BitstreamStorageService:
    """Stores files and performs cryptographic checksum verification."""

    def __init__(self, base_storage_dir: str = "data/repository/bitstreams"):
        self.base_storage_dir = base_storage_dir
        os.makedirs(self.base_storage_dir, exist_ok=True)
        self.audit_log: List[ChecksumAuditRecord] = []

    def compute_sha256(self, file_content: bytes) -> str:
        return hashlib.sha256(file_content).hexdigest()

    def store_bitstream(self, item_id: str, filename: str, content: bytes, mime_type: str) -> Bitstream:
        checksum = self.compute_sha256(content)
        # Content addressable subdirectories based on first 4 hex chars
        subdir = os.path.join(self.base_storage_dir, checksum[:2], checksum[2:4])
        os.makedirs(subdir, exist_ok=True)
        file_path = os.path.join(subdir, checksum)
        with open(file_path, "wb") as f:
            f.write(content)

        bs_id = f"BS-{checksum[:12]}"
        return Bitstream(
            id=bs_id,
            repository_item_id=item_id,
            filename=filename,
            mime_type=mime_type,
            size_bytes=len(content),
            sha256_checksum=checksum,
            storage_path=file_path
        )

    def verify_fixity(self, bitstream: Bitstream) -> bool:
        if not os.path.exists(bitstream.storage_path):
            is_valid = False
            actual_hash = "FILE_NOT_FOUND"
        else:
            with open(bitstream.storage_path, "rb") as f:
                actual_hash = hashlib.sha256(f.read()).hexdigest()
            is_valid = (actual_hash == bitstream.sha256_checksum)

        audit = ChecksumAuditRecord(
            id=f"AUDIT-{len(self.audit_log)+1:06d}",
            bitstream_id=bitstream.id,
            algorithm="SHA-256",
            expected_hash=bitstream.sha256_checksum,
            actual_hash=actual_hash,
            is_valid=is_valid
        )
        self.audit_log.append(audit)
        return is_valid
