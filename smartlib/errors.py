"""
Domain-specific exception hierarchy for SmartLibrary ERP.
Prevents internal stack trace leakage while providing structured error diagnostics.
"""

from typing import Optional, Dict, Any

class SmartLibError(Exception):
    """Base exception for all SmartLibrary ERP domain errors."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": True,
            "code": self.code,
            "message": self.message,
            "details": self.details
        }

class AuthenticationError(SmartLibError):
    """Raised when credentials fail authentication."""
    def __init__(self, message: str = "Invalid username or password", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="AUTH_FAILED", details=details)

class InvalidCredentialsError(AuthenticationError):
    """Explicit credential mismatch."""
    def __init__(self, message: str = "The username or password provided is incorrect"):
        super().__init__(message=message)

class AccountLockedError(AuthenticationError):
    """Raised when an account is temporarily locked due to brute force protection."""
    def __init__(self, minutes_remaining: int = 15):
        msg = f"Account is locked due to consecutive failed attempts. Try again in {minutes_remaining} minutes."
        super().__init__(message=msg, details={"minutes_remaining": minutes_remaining})
        self.code = "ACCOUNT_LOCKED"

class AccountInactiveError(AuthenticationError):
    """Raised when attempting to log into a deactivated or suspended account."""
    def __init__(self, status: str = "INACTIVE"):
        super().__init__(message=f"Account is currently {status}. Contact system administrator.", details={"status": status})
        self.code = "ACCOUNT_INACTIVE"

class SessionExpiredError(AuthenticationError):
    """Raised when a session token has expired."""
    def __init__(self, message: str = "Session has expired. Please log in again."):
        super().__init__(message=message)
        self.code = "SESSION_EXPIRED"

class AuthorizationError(SmartLibError):
    """Raised when user attempts an unauthorized operation."""
    def __init__(self, message: str = "Access denied: insufficient permissions", required_role: Optional[str] = None):
        super().__init__(message, code="ACCESS_DENIED", details={"required_role": required_role} if required_role else {})

class EntityNotFoundError(SmartLibError):
    """Raised when a requested domain entity does not exist."""
    def __init__(self, entity_name: str, identifier: Any):
        super().__init__(f"{entity_name} with identifier '{identifier}' was not found.", code="NOT_FOUND", details={"entity": entity_name, "identifier": str(identifier)})

class UserNotFoundError(EntityNotFoundError):
    def __init__(self, identifier: Any):
        super().__init__("User", identifier)

class DuplicateEntityError(SmartLibError):
    """Raised when a uniqueness constraint is violated."""
    def __init__(self, entity_name: str, field: str, value: Any):
        super().__init__(f"{entity_name} with {field} '{value}' already exists.", code="DUPLICATE_ENTITY", details={"entity": entity_name, "field": field, "value": str(value)})

class ValidationError(SmartLibError):
    """Raised when domain or schema validation fails."""
    def __init__(self, message: str, errors: Optional[Dict[str, str]] = None):
        super().__init__(message, code="VALIDATION_ERROR", details=errors or {})

class BusinessRuleViolationError(SmartLibError):
    """Raised when an enterprise business invariant is violated."""
    def __init__(self, rule_name: str, message: str, details: Optional[Dict[str, Any]] = None):
        d = details or {}
        d["rule"] = rule_name
        super().__init__(message, code="BUSINESS_RULE_VIOLATION", details=d)

class BorrowingLimitReachedError(BusinessRuleViolationError):
    def __init__(self, limit: int, current: int):
        super().__init__("MAX_BORROWING_LIMIT", f"Member has reached their maximum borrowing quota of {limit} books (currently holding {current}).", {"limit": limit, "current": current})

class CopyUnavailableError(BusinessRuleViolationError):
    def __init__(self, copy_id: str, status: str):
        super().__init__("COPY_UNAVAILABLE", f"Physical copy '{copy_id}' is not available for issue (current status: {status}).", {"copy_id": copy_id, "status": status})

class MembershipExpiredError(BusinessRuleViolationError):
    def __init__(self, expiry_date: str):
        super().__init__("MEMBERSHIP_EXPIRED", f"Membership expired on {expiry_date}. Cannot perform circulation operations.", {"expiry_date": expiry_date})

class DatabaseError(SmartLibError):
    """Low-level database transaction failure."""
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message, code="DATABASE_ERROR", details={"original": str(original_exception)} if original_exception else {})
