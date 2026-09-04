"""Complete OpenAPI 3.0.3 Specification Document and Path Registry.

Full REST contract definitions covering all 35+ services across the Library ERP.
"""

from typing import Dict, Any, List


OPENAPI_PATHS: Dict[str, Any] = {}

def _add_path(path_str: str, method: str, op_dict: Dict[str, Any]):
    if path_str not in OPENAPI_PATHS:
        OPENAPI_PATHS[path_str] = {}
    OPENAPI_PATHS[path_str][method.lower()] = op_dict

# POST /api/v1/auth/login
_add_path("/api/v1/auth/login", "POST", {
    "summary": "User Authentication",
    "description": "Authenticate library user credentials and receive JWT bearer token",
    "tags": ["Authentication"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/LoginRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AuthTokenResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/auth/refresh
_add_path("/api/v1/auth/refresh", "POST", {
    "summary": "Token Refresh",
    "description": "Refresh an expired access token using a valid refresh token",
    "tags": ["Authentication"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RefreshTokenRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AuthTokenResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/auth/2fa/verify
_add_path("/api/v1/auth/2fa/verify", "POST", {
    "summary": "Verify Two-Factor TOTP",
    "description": "Validate RFC 6238 TOTP token for high-privilege operations",
    "tags": ["Authentication"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TotpVerifyRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ActionSuccessResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/books
_add_path("/api/v1/books", "GET", {
    "summary": "List Catalog Books",
    "description": "Search, filter, and paginate bibliographic books in the library catalog",
    "tags": ["Catalog"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BookListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/books
_add_path("/api/v1/books", "POST", {
    "summary": "Create Catalog Book",
    "description": "Add a new bibliographic book record with ISBN, metadata, and classification",
    "tags": ["Catalog"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BookCreateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BookSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/books/{id}
_add_path("/api/v1/books/{id}", "GET", {
    "summary": "Get Book Details",
    "description": "Retrieve complete bibliographic monograph details by unique ID",
    "tags": ["Catalog"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BookSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# PUT /api/v1/books/{id}
_add_path("/api/v1/books/{id}", "PUT", {
    "summary": "Update Book Record",
    "description": "Modify bibliographic information, categories, authors, and summary",
    "tags": ["Catalog"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BookUpdateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BookSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# DELETE /api/v1/books/{id}
_add_path("/api/v1/books/{id}", "DELETE", {
    "summary": "Weed / Delete Book",
    "description": "Mark book record as withdrawn/weeded from the collection",
    "tags": ["Catalog"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ActionSuccessResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/books/{id}/copies
_add_path("/api/v1/books/{id}/copies", "GET", {
    "summary": "List Physical Copies",
    "description": "List all circulating and non-circulating physical copies of a book",
    "tags": ["Catalog"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CopyListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/books/{id}/copies
_add_path("/api/v1/books/{id}/copies", "POST", {
    "summary": "Add Physical Copy",
    "description": "Ingest a new physical book copy and assign unique barcode/RFID",
    "tags": ["Catalog"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CopyCreateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CopySingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/circulation/checkout
_add_path("/api/v1/circulation/checkout", "POST", {
    "summary": "Issue Book (Checkout)",
    "description": "Check out an available book copy to an active patron",
    "tags": ["Circulation"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CheckoutRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/LoanSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/circulation/checkin
_add_path("/api/v1/circulation/checkin", "POST", {
    "summary": "Return Book (Checkin)",
    "description": "Process the physical return of a loaned book, check condition, and clear dues",
    "tags": ["Circulation"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CheckinRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ReturnReceiptResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/circulation/renew
_add_path("/api/v1/circulation/renew", "POST", {
    "summary": "Renew Loan",
    "description": "Extend loan due date if no pending reservations exist for the title",
    "tags": ["Circulation"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RenewalRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/LoanSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/circulation/loans
_add_path("/api/v1/circulation/loans", "GET", {
    "summary": "List Active Loans",
    "description": "Query all ongoing circulation loans with due dates and overdue statuses",
    "tags": ["Circulation"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/LoanListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/circulation/loans/{id}
_add_path("/api/v1/circulation/loans/{id}", "GET", {
    "summary": "Get Loan Details",
    "description": "Retrieve audit trail and history of a specific loan transaction",
    "tags": ["Circulation"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/LoanSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/reservations
_add_path("/api/v1/reservations", "GET", {
    "summary": "List Reservations",
    "description": "Query patron hold queue requests and reservation shelf pickups",
    "tags": ["Reservations"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ReservationListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/reservations
_add_path("/api/v1/reservations", "POST", {
    "summary": "Place Hold Reservation",
    "description": "Place a reservation queue hold on an issued or in-process book",
    "tags": ["Reservations"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ReservationCreateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ReservationSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/reservations/{id}/cancel
_add_path("/api/v1/reservations/{id}/cancel", "POST", {
    "summary": "Cancel Reservation",
    "description": "Cancel an active patron hold reservation",
    "tags": ["Reservations"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ActionSuccessResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/fines
_add_path("/api/v1/fines", "GET", {
    "summary": "List Fines",
    "description": "Query assessed patron overdue and damage fines across the system",
    "tags": ["Fines"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/FineListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/fines/assess
_add_path("/api/v1/fines/assess", "POST", {
    "summary": "Assess Fine",
    "description": "Manually or automatically assess a fine to a patron account",
    "tags": ["Fines"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/FineAssessRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/FineSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/fines/{id}/pay
_add_path("/api/v1/fines/{id}/pay", "POST", {
    "summary": "Process Fine Payment",
    "description": "Record cashier cash, card, or online payment against an unpaid fine",
    "tags": ["Fines"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/FinePaymentRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PaymentReceiptResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/fines/{id}/waive
_add_path("/api/v1/fines/{id}/waive", "POST", {
    "summary": "Waive Fine",
    "description": "Authorize supervisor fine waiver with audit reason and signature",
    "tags": ["Fines"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/FineWaiveRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ActionSuccessResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/members
_add_path("/api/v1/members", "GET", {
    "summary": "Search Members",
    "description": "Search patron accounts by card number, name, email, or membership tier",
    "tags": ["Members"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MemberListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/members
_add_path("/api/v1/members", "POST", {
    "summary": "Register Member",
    "description": "Enroll a new library member, issue digital barcode, and establish tier",
    "tags": ["Members"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MemberCreateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MemberSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/members/{id}
_add_path("/api/v1/members/{id}", "GET", {
    "summary": "Get Member Profile",
    "description": "Retrieve patron profile, active loans, borrowing history, and fine balance",
    "tags": ["Members"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MemberSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# PUT /api/v1/members/{id}
_add_path("/api/v1/members/{id}", "PUT", {
    "summary": "Update Member Profile",
    "description": "Update contact address, phone, email, and membership expiration date",
    "tags": ["Members"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MemberUpdateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MemberSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# PUT /api/v1/members/{id}/status
_add_path("/api/v1/members/{id}/status", "PUT", {
    "summary": "Toggle Member Status",
    "description": "Activate, suspend, or block patron borrowing privileges",
    "tags": ["Members"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MemberStatusRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ActionSuccessResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/acquisitions/vendors
_add_path("/api/v1/acquisitions/vendors", "GET", {
    "summary": "List Book Vendors",
    "description": "Query authorized book jobbers, periodical publishers, and supply vendors",
    "tags": ["Acquisitions"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/VendorListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/acquisitions/vendors
_add_path("/api/v1/acquisitions/vendors", "POST", {
    "summary": "Create Vendor",
    "description": "Register a new commercial publishing vendor and payment terms",
    "tags": ["Acquisitions"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/VendorCreateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/VendorSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/acquisitions/orders
_add_path("/api/v1/acquisitions/orders", "GET", {
    "summary": "List Purchase Orders",
    "description": "Query purchase orders across fiscal year quarters and approval states",
    "tags": ["Acquisitions"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/POListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/acquisitions/orders
_add_path("/api/v1/acquisitions/orders", "POST", {
    "summary": "Create Purchase Order",
    "description": "Create a purchase requisition with multi-line items and fund allocation",
    "tags": ["Acquisitions"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/POCreateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/POSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/acquisitions/orders/{id}/approve
_add_path("/api/v1/acquisitions/orders/{id}/approve", "POST", {
    "summary": "Approve Purchase Order",
    "description": "Authorize encumbrance against budget ledger and dispatch EDI order",
    "tags": ["Acquisitions"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/POSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/acquisitions/invoices
_add_path("/api/v1/acquisitions/invoices", "POST", {
    "summary": "Create Invoice",
    "description": "Process vendor invoice, perform 3-way match, and authorize disbursement",
    "tags": ["Acquisitions"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/InvoiceCreateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/InvoiceSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/serials/subscriptions
_add_path("/api/v1/serials/subscriptions", "GET", {
    "summary": "List Subscriptions",
    "description": "Query active continuing serials and journal subscriptions",
    "tags": ["Serials"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SubscriptionListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/serials/subscriptions
_add_path("/api/v1/serials/subscriptions", "POST", {
    "summary": "Create Subscription",
    "description": "Register new periodical title with publication frequency pattern",
    "tags": ["Serials"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SubscriptionCreateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SubscriptionSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/serials/checkin
_add_path("/api/v1/serials/checkin", "POST", {
    "summary": "Rapid Issue Check-in",
    "description": "Check in an arriving serial issue, generate barcode, and print routing slip",
    "tags": ["Serials"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/IssueCheckinRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/IssueSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/serials/claims
_add_path("/api/v1/serials/claims", "POST", {
    "summary": "File Vendor Claim",
    "description": "Generate automated claim notice for late or missing journal issues",
    "tags": ["Serials"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ClaimNoticeRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ActionSuccessResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/ill/requests
_add_path("/api/v1/ill/requests", "GET", {
    "summary": "List ILL Requests",
    "description": "List borrowing and lending resource sharing transactions",
    "tags": ["ILL"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/IllRequestListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/ill/requests
_add_path("/api/v1/ill/requests", "POST", {
    "summary": "Submit ILL Request",
    "description": "Create an ISO 18626 interlibrary loan borrowing request for a patron",
    "tags": ["ILL"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/IllRequestCreate"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/IllSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/ill/requests/{id}/ship
_add_path("/api/v1/ill/requests/{id}/ship", "POST", {
    "summary": "Mark Shipped",
    "description": "Update shipping tracking number and dispatch partner loan",
    "tags": ["ILL"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/IllShipRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ActionSuccessResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/repository/items
_add_path("/api/v1/repository/items", "GET", {
    "summary": "List Repository Items",
    "description": "Search open-access academic publications, theses, and faculty papers",
    "tags": ["Repository"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RepoItemListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/repository/items
_add_path("/api/v1/repository/items", "POST", {
    "summary": "Deposit Repository Item",
    "description": "Submit a scholarly publication with Dublin Core metadata and DOI minting",
    "tags": ["Repository"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RepoItemCreateRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RepoItemSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/repository/items/{id}/citation
_add_path("/api/v1/repository/items/{id}/citation", "GET", {
    "summary": "Generate Citations",
    "description": "Generate formatted academic citations in APA 7th, MLA 9th, and BibTeX",
    "tags": ["Repository"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/CitationResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/spaces/rooms
_add_path("/api/v1/spaces/rooms", "GET", {
    "summary": "List Study Rooms",
    "description": "Check real-time availability of group study rooms and media labs",
    "tags": ["Spaces"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RoomListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/spaces/reservations
_add_path("/api/v1/spaces/reservations", "POST", {
    "summary": "Book Study Room",
    "description": "Reserve a collaborative study space for a specific time block",
    "tags": ["Spaces"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SpaceBookRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SpaceResSingleResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/equipment/loans
_add_path("/api/v1/equipment/loans", "POST", {
    "summary": "Checkout Tech Equipment",
    "description": "Loan out a laptop, camera, or projector to a patron with inspection checklist",
    "tags": ["Equipment"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/EquipmentLoanRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/EquipmentLoanResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/finance/accounts
_add_path("/api/v1/finance/accounts", "GET", {
    "summary": "Chart of Accounts",
    "description": "List general ledger double-entry accounts with current balances",
    "tags": ["Finance"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AccountListResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# POST /api/v1/finance/journal-entries
_add_path("/api/v1/finance/journal-entries", "POST", {
    "summary": "Record Journal Entry",
    "description": "Post a balanced double-entry transaction to the general ledger",
    "tags": ["Finance"],
    "requestBody": {
        "required": True,
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/JournalEntryRequest"}}}
    },
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ActionSuccessResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/finance/reports/trial-balance
_add_path("/api/v1/finance/reports/trial-balance", "GET", {
    "summary": "Trial Balance Report",
    "description": "Generate debit-credit trial balance sheet verification",
    "tags": ["Finance"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TrialBalanceResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# GET /api/v1/finance/reports/income-statement
_add_path("/api/v1/finance/reports/income-statement", "GET", {
    "summary": "Income Statement",
    "description": "Generate operating revenue and acquisitions expense statement",
    "tags": ["Finance"],
    "responses": {
        "200": {
            "description": "Successful operation",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/IncomeStatementResponse"}}}
        },
        "400": {"description": "Invalid input parameters or validation failure"},
        "401": {"description": "Unauthorized - Missing or expired JWT bearer token"},
        "403": {"description": "Forbidden - Insufficient ABAC role permissions"},
        "404": {"description": "Target entity or resource not found"},
        "500": {"description": "Internal server processing error"}
    }
})

# Report: inventory
_add_path("/api/v1/reports/inventory", "GET", {
    "summary": "Generate Comprehensive Book Inventory & Catalog Statistics",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for Comprehensive Book Inventory & Catalog Statistics.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})

# Report: overdue
_add_path("/api/v1/reports/overdue", "GET", {
    "summary": "Generate Active Overdue Borrowing & Delinquency Ledger",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for Active Overdue Borrowing & Delinquency Ledger.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})

# Report: fines
_add_path("/api/v1/reports/fines", "GET", {
    "summary": "Generate Fine Collections, Cashier Receipts & Financial Ledger",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for Fine Collections, Cashier Receipts & Financial Ledger.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})

# Report: popular
_add_path("/api/v1/reports/popular", "GET", {
    "summary": "Generate High Circulation Frequency & Top Borrowed Titles",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for High Circulation Frequency & Top Borrowed Titles.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})

# Report: lost_books
_add_path("/api/v1/reports/lost_books", "GET", {
    "summary": "Generate Lost and Damaged Material Replacement Schedule",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for Lost and Damaged Material Replacement Schedule.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})

# Report: acquisitions
_add_path("/api/v1/reports/acquisitions", "GET", {
    "summary": "Generate Annual Vendor Expenditures and Fund Allocation Analysis",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for Annual Vendor Expenditures and Fund Allocation Analysis.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})

# Report: serials
_add_path("/api/v1/reports/serials", "GET", {
    "summary": "Generate Serials Check-in Compliance & Vendor Claim History",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for Serials Check-in Compliance & Vendor Claim History.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})

# Report: ill_summary
_add_path("/api/v1/reports/ill_summary", "GET", {
    "summary": "Generate Consortium Resource Sharing Balance-of-Trade Ledger",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for Consortium Resource Sharing Balance-of-Trade Ledger.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})

# Report: repository
_add_path("/api/v1/reports/repository", "GET", {
    "summary": "Generate Institutional Repository Download Metrics and Altmetrics",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for Institutional Repository Download Metrics and Altmetrics.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})

# Report: spaces_util
_add_path("/api/v1/reports/spaces_util", "GET", {
    "summary": "Generate Study Room & Facility Booking Utilization Heatmap",
    "description": "Calculates aggregated analytics, KPI cards, and filtered table data for Study Room & Facility Booking Utilization Heatmap.",
    "tags": ["Reports & Analytics"],
    "parameters": [
        {"name": "start_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "end_date", "in": "query", "required": False, "schema": {"type": "string", "format": "date"}},
        {"name": "export_format", "in": "query", "required": False, "schema": {"type": "string", "enum": ["json", "csv", "pdf", "excel"]}}
    ],
    "responses": {"200": {"description": "Aggregated report payload and export headers"}}
})


def get_full_openapi_paths() -> Dict[str, Any]:
    return OPENAPI_PATHS
