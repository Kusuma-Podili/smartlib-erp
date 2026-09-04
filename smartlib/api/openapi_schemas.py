"""OpenAPI 3.0.3 Component Schemas and Entity Data Dictionaries.

Defines standard JSON Schema structures for all 35+ core resources in the Library ERP.
"""

from typing import Dict, Any

ENTITY_SCHEMAS: Dict[str, Dict[str, Any]] = {}

# 1. Book Schema
ENTITY_SCHEMAS["Book"] = {
    "type": "object",
    "description": "Bibliographic monograph record representing a work in the library catalog.",
    "required": ["id", "title", "isbn"],
    "properties": {
        "id": {"type": "integer", "format": "int64", "example": 101},
        "title": {"type": "string", "example": "Clean Code: A Handbook of Agile Software Craftsmanship"},
        "subtitle": {"type": "string", "example": "A Handbook of Agile Software Craftsmanship"},
        "isbn": {"type": "string", "pattern": "^[0-9Xx-]{10,17}$", "example": "9780132350884"},
        "edition": {"type": "string", "example": "1st Edition"},
        "publication_year": {"type": "integer", "minimum": 1450, "maximum": 2030, "example": 2008},
        "language": {"type": "string", "example": "eng"},
        "page_count": {"type": "integer", "minimum": 1, "example": 464},
        "summary": {"type": "string", "example": "Even bad code can function. But if code isn't clean..."},
        "category_id": {"type": "integer", "example": 1},
        "category_name": {"type": "string", "example": "Computer Science"},
        "publisher_id": {"type": "integer", "example": 2},
        "publisher_name": {"type": "string", "example": "Prentice Hall"},
        "author_ids": {"type": "array", "items": {"type": "integer"}, "example": [1]},
        "authors": {"type": "array", "items": {"type": "string"}, "example": ["Robert C. Martin"]},
        "total_copies": {"type": "integer", "minimum": 0, "example": 5},
        "available_copies": {"type": "integer", "minimum": 0, "example": 4},
        "created_at": {"type": "string", "format": "date-time", "example": "2026-09-01T10:00:00Z"},
        "updated_at": {"type": "string", "format": "date-time", "example": "2026-09-04T12:00:00Z"}
    }
}

# 2. BookCopy Schema
ENTITY_SCHEMAS["BookCopy"] = {
    "type": "object",
    "description": "Physical circulating copy or volume of a bibliographic book record.",
    "required": ["id", "book_id", "barcode", "status"],
    "properties": {
        "id": {"type": "integer", "format": "int64", "example": 201},
        "book_id": {"type": "integer", "example": 101},
        "barcode": {"type": "string", "example": "BC-9780132350884-001"},
        "rfid_tag": {"type": "string", "example": "E004015077C54E91"},
        "status": {"type": "string", "enum": ["AVAILABLE", "ISSUED", "RESERVED", "MAINTENANCE", "LOST", "DAMAGED"], "example": "AVAILABLE"},
        "condition_notes": {"type": "string", "example": "Good condition, slight shelf wear"},
        "shelf_location": {"type": "string", "example": "Stack 4, Tier 2, Shelf B"},
        "call_number": {"type": "string", "example": "QA76.76.C65 M37 2008"},
        "acquisition_date": {"type": "string", "format": "date", "example": "2026-01-15"},
        "price_cents": {"type": "integer", "example": 3500}
    }
}

# 3. Member Schema
ENTITY_SCHEMAS["Member"] = {
    "type": "object",
    "description": "Registered library patron account eligible for borrowing and services.",
    "required": ["id", "member_number", "first_name", "last_name", "email", "status"],
    "properties": {
        "id": {"type": "integer", "format": "int64", "example": 501},
        "member_number": {"type": "string", "example": "MEM-2026-0001"},
        "first_name": {"type": "string", "example": "John"},
        "last_name": {"type": "string", "example": "Patron"},
        "email": {"type": "string", "format": "email", "example": "john.patron@library.org"},
        "phone": {"type": "string", "example": "+1-555-0199"},
        "address": {"type": "string", "example": "123 Academic Way, University City"},
        "membership_tier": {"type": "string", "enum": ["STUDENT", "FACULTY", "COMMUNITY", "RESEARCHER"], "example": "STUDENT"},
        "status": {"type": "string", "enum": ["ACTIVE", "SUSPENDED", "EXPIRED", "DEACTIVATED"], "example": "ACTIVE"},
        "max_concurrent_loans": {"type": "integer", "example": 5},
        "active_loans_count": {"type": "integer", "example": 1},
        "unpaid_fines_cents": {"type": "integer", "example": 0},
        "expires_at": {"type": "string", "format": "date", "example": "2027-08-31"}
    }
}

# 4. Loan (Borrowing Transaction) Schema
ENTITY_SCHEMAS["Loan"] = {
    "type": "object",
    "description": "Circulation loan transaction recording book checkout to a patron.",
    "required": ["id", "book_copy_id", "member_id", "issued_at", "due_date", "status"],
    "properties": {
        "id": {"type": "integer", "format": "int64", "example": 1001},
        "book_copy_id": {"type": "integer", "example": 201},
        "barcode": {"type": "string", "example": "BC-9780132350884-001"},
        "book_title": {"type": "string", "example": "Clean Code"},
        "member_id": {"type": "integer", "example": 501},
        "member_name": {"type": "string", "example": "John Patron"},
        "issued_at": {"type": "string", "format": "date-time", "example": "2026-09-01T14:30:00Z"},
        "issued_by_employee_id": {"type": "integer", "example": 12},
        "due_date": {"type": "string", "format": "date", "example": "2026-09-15"},
        "returned_at": {"type": "string", "format": "date-time", "nullable": True, "example": None},
        "renewal_count": {"type": "integer", "example": 0},
        "status": {"type": "string", "enum": ["ACTIVE", "RETURNED", "OVERDUE", "LOST"], "example": "ACTIVE"}
    }
}

# 5. FineRecord Schema
ENTITY_SCHEMAS["FineRecord"] = {
    "type": "object",
    "description": "Financial penalty or fee assessed to a patron for overdue return or damage.",
    "required": ["id", "member_id", "amount_cents", "reason", "status"],
    "properties": {
        "id": {"type": "integer", "format": "int64", "example": 3001},
        "loan_id": {"type": "integer", "nullable": True, "example": 1001},
        "member_id": {"type": "integer", "example": 501},
        "member_name": {"type": "string", "example": "John Patron"},
        "amount_cents": {"type": "integer", "minimum": 1, "example": 2500},
        "reason": {"type": "string", "example": "Overdue return 5 days @ 5.00/day"},
        "assessed_at": {"type": "string", "format": "date-time", "example": "2026-09-04T09:00:00Z"},
        "status": {"type": "string", "enum": ["UNPAID", "PAID", "PARTIALLY_PAID", "WAIVED"], "example": "UNPAID"},
        "paid_at": {"type": "string", "format": "date-time", "nullable": True, "example": None}
    }
}

# 6. PurchaseOrder Schema
ENTITY_SCHEMAS["PurchaseOrder"] = {
    "type": "object",
    "description": "Acquisitions purchase order sent to book jobber or subscription vendor.",
    "required": ["id", "po_number", "vendor_id", "status"],
    "properties": {
        "id": {"type": "integer", "format": "int64", "example": 4001},
        "po_number": {"type": "string", "example": "PO-202609-0012"},
        "vendor_id": {"type": "integer", "example": 8},
        "vendor_name": {"type": "string", "example": "Ingram Content Group"},
        "status": {"type": "string", "enum": ["DRAFT", "APPROVED", "DISPATCHED", "PARTIAL", "FULFILLED", "CANCELLED"], "example": "APPROVED"},
        "total_amount_cents": {"type": "integer", "example": 145000},
        "fund_code": {"type": "string", "example": "FUND-CS-2026"},
        "created_at": {"type": "string", "format": "date-time", "example": "2026-09-02T11:00:00Z"}
    }
}

# 7. SerialSubscription Schema
ENTITY_SCHEMAS["SerialSubscription"] = {
    "type": "object",
    "description": "Continuing periodicals or journal subscription schedule.",
    "required": ["id", "title", "issn", "frequency", "status"],
    "properties": {
        "id": {"type": "integer", "format": "int64", "example": 5001},
        "title": {"type": "string", "example": "Communications of the ACM"},
        "issn": {"type": "string", "example": "0001-0782"},
        "frequency": {"type": "string", "enum": ["MONTHLY", "QUARTERLY", "WEEKLY", "BIMONTHLY"], "example": "MONTHLY"},
        "vendor_id": {"type": "integer", "example": 8},
        "current_volume": {"type": "integer", "example": 69},
        "start_date": {"type": "string", "format": "date", "example": "2026-01-01"},
        "end_date": {"type": "string", "format": "date", "example": "2026-12-31"},
        "status": {"type": "string", "enum": ["ACTIVE", "EXPIRED", "SUSPENDED", "CANCELLED"], "example": "ACTIVE"}
    }
}

# 8. RepositoryItem Schema
ENTITY_SCHEMAS["RepositoryItem"] = {
    "type": "object",
    "description": "Scholarly digital archive item with metadata and associated bitstreams.",
    "required": ["id", "title", "handle", "license"],
    "properties": {
        "id": {"type": "integer", "format": "int64", "example": 6001},
        "title": {"type": "string", "example": "Fault-Tolerant Distributed Consensus Algorithms"},
        "authors": {"type": "array", "items": {"type": "string"}, "example": ["Dr. Alan Turing"]},
        "abstract": {"type": "string", "example": "We propose a novel Paxos variant..."},
        "handle": {"type": "string", "example": "10.5072/smartlib/cs-2026-0042"},
        "license": {"type": "string", "example": "CC-BY-4.0"},
        "bitstreams_count": {"type": "integer", "example": 2},
        "embargo_until": {"type": "string", "format": "date", "nullable": True, "example": None}
    }
}

# 9. SpaceRoom Schema
ENTITY_SCHEMAS["SpaceRoom"] = {
    "type": "object",
    "description": "Reservable library room or physical facility.",
    "required": ["id", "room_number", "name", "space_type", "capacity"],
    "properties": {
        "id": {"type": "integer", "format": "int64", "example": 7001},
        "room_number": {"type": "string", "example": "SR-204"},
        "name": {"type": "string", "example": "Ada Lovelace Collaborative Study Suite"},
        "space_type": {"type": "string", "enum": ["QUIET_STUDY", "GROUP_STUDY", "CONFERENCE", "MEDIA_LAB"], "example": "GROUP_STUDY"},
        "capacity": {"type": "integer", "example": 8},
        "is_available": {"type": "boolean", "example": True}
    }
}

# 10. GeneralLedgerAccount Schema
ENTITY_SCHEMAS["GeneralLedgerAccount"] = {
    "type": "object",
    "description": "Double-entry accounting general ledger chart of accounts node.",
    "required": ["code", "name", "account_type", "normal_balance"],
    "properties": {
        "code": {"type": "string", "example": "1010"},
        "name": {"type": "string", "example": "Cash on Hand - Main Circulation Desk"},
        "account_type": {"type": "string", "enum": ["ASSET", "LIABILITY", "EQUITY", "REVENUE", "EXPENSE"], "example": "ASSET"},
        "normal_balance": {"type": "string", "enum": ["DEBIT", "CREDIT"], "example": "DEBIT"},
        "balance_cents": {"type": "integer", "example": 154000}
    }
}

def get_entity_schema(name: str) -> Dict[str, Any]:
    return ENTITY_SCHEMAS.get(name, {})
