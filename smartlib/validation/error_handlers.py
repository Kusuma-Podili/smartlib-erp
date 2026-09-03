"""
Safe exception mapper and customer-facing error serializer.
"""

import logging
from typing import Dict, Any, Tuple
from smartlib.errors import SmartLibError, AuthenticationError, AuthorizationError, EntityNotFoundError, ValidationError, BusinessRuleViolationError

logger = logging.getLogger("smartlib.errors")

def map_exception_to_response(exc: Exception) -> Tuple[int, Dict[str, Any]]:
    """
    Translate any domain or unexpected Python exception into a clean, safe HTTP-style status and payload.
    Ensures zero internal trace or stack exposure to clients.
    """
    if isinstance(exc, AuthenticationError):
        return 401, {
            "success": False,
            "error_code": exc.code,
            "message": exc.message,
            "details": exc.details
        }
    if isinstance(exc, AuthorizationError):
        return 403, {
            "success": False,
            "error_code": exc.code,
            "message": exc.message,
            "details": exc.details
        }
    if isinstance(exc, EntityNotFoundError):
        return 404, {
            "success": False,
            "error_code": exc.code,
            "message": exc.message,
            "details": exc.details
        }
    if isinstance(exc, ValidationError):
        return 422, {
            "success": False,
            "error_code": exc.code,
            "message": exc.message,
            "validation_errors": exc.details
        }
    if isinstance(exc, BusinessRuleViolationError):
        return 400, {
            "success": False,
            "error_code": exc.code,
            "message": exc.message,
            "rule_details": exc.details
        }
    if isinstance(exc, SmartLibError):
        return 400, {
            "success": False,
            "error_code": exc.code,
            "message": exc.message,
            "details": exc.details
        }

    # Catch-all unexpected internal system error
    logger.error("Unhandled internal exception: %s", str(exc), exc_info=True)
    return 500, {
        "success": False,
        "error_code": "INTERNAL_SERVER_ERROR",
        "message": "An unexpected error occurred. Please contact the library administrator.",
        "details": {}
    }
