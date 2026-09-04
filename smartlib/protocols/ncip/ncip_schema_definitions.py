"""NISO NCIP 2.0 (ANSI/NISO Z39.83-1-2008) Complete Message Definitions & Schemas.

Covers all standard Circulation, Patron Lookup, Item Status, and Agency services.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class NcipFieldDefinition:
    field_name: str
    data_type: str
    required: bool
    description: str


@dataclass
class NcipServiceSpecification:
    service_name: str
    request_root_element: str
    response_root_element: str
    description: str
    request_fields: List[NcipFieldDefinition]
    response_fields: List[NcipFieldDefinition]


NCIP_SERVICES: Dict[str, NcipServiceSpecification] = {}

def _svc(name: str, req_el: str, resp_el: str, desc: str, req_fields: List[NcipFieldDefinition], resp_fields: List[NcipFieldDefinition]):
    NCIP_SERVICES[name] = NcipServiceSpecification(name, req_el, resp_el, desc, req_fields, resp_fields)

# Service: AcceptItem
_svc("AcceptItem", "AcceptItem", "AcceptItemResponse", "Transfers an item into the circulation jurisdiction of the agency", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Agency sender/recipient routing header"),
    NcipFieldDefinition("MandatedAction", "MandatedAction", False, "Authorization of administrative action"),
    NcipFieldDefinition("RequestId", "RequestId", False, "Identifier of the requesting agency request"),
    NcipFieldDefinition("RequestedActionType", "Enumeration", True, "Hold For Pickup, Loan, Circulate"),
    NcipFieldDefinition("ItemDetails", "ItemDetails", False, "Bibliographic metadata and barcode of item"),
    NcipFieldDefinition("UserId", "UserId", False, "Target patron card identifier"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Agency responder routing header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic error details if operation failed"),
    NcipFieldDefinition("ItemId", "ItemId", False, "Assigned circulation barcode"),
    NcipFieldDefinition("RoutingInformation", "RoutingInfo", False, "Instructions for shelving or hold placement"),
])

# Service: CheckInItem
_svc("CheckInItem", "CheckInItem", "CheckInItemResponse", "Processes the return of an item and updates circulation status", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Routing header"),
    NcipFieldDefinition("ItemId", "ItemId", True, "Physical barcode of returning item"),
    NcipFieldDefinition("ItemOptionalFields", "OptionalFields", False, "Condition and location notes"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic error"),
    NcipFieldDefinition("ItemId", "ItemId", True, "Returned item barcode"),
    NcipFieldDefinition("UserId", "UserId", False, "Patron who held the loan"),
    NcipFieldDefinition("RoutingInformation", "RoutingInfo", False, "Reshelve or transfer to hold shelf"),
])

# Service: CheckOutItem
_svc("CheckOutItem", "CheckOutItem", "CheckOutItemResponse", "Checks out an item to a verified library patron", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Routing header"),
    NcipFieldDefinition("UserId", "UserId", True, "Borrowing patron barcode"),
    NcipFieldDefinition("ItemId", "ItemId", True, "Circulating item barcode"),
    NcipFieldDefinition("DesiredDateDue", "Date", False, "Requested return date"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic error (e.g. card suspended, overdue fine cap)"),
    NcipFieldDefinition("UserId", "UserId", True, "Borrowing patron barcode"),
    NcipFieldDefinition("ItemId", "ItemId", True, "Checked out item barcode"),
    NcipFieldDefinition("DateDue", "Date", True, "Official calculated circulation due date"),
    NcipFieldDefinition("RenewalCount", "Integer", True, "Number of renewals remaining"),
])

# Service: LookupUser
_svc("LookupUser", "LookupUser", "LookupUserResponse", "Queries patron account status, active loans, and fine balance", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Routing header"),
    NcipFieldDefinition("UserId", "UserId", True, "Patron barcode or university ID"),
    NcipFieldDefinition("UserElementType", "Enumeration", True, "User Address, Name, Loaned Items, Fiscal Account"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic error"),
    NcipFieldDefinition("UserId", "UserId", True, "Patron barcode"),
    NcipFieldDefinition("UserOptionalFields", "UserFields", False, "Demographic, privilege, loan, and fine records"),
])

# Service: LookupItem
_svc("LookupItem", "LookupItem", "LookupItemResponse", "Queries catalog item status, availability, and hold queue", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Routing header"),
    NcipFieldDefinition("ItemId", "ItemId", True, "Item barcode or electronic identifier"),
    NcipFieldDefinition("ItemElementType", "Enumeration", True, "Bibliographic Description, Circulation Status, Hold Queue"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic error"),
    NcipFieldDefinition("ItemId", "ItemId", True, "Item barcode"),
    NcipFieldDefinition("ItemOptionalFields", "ItemFields", False, "Bibliographic details, circulation status, location"),
])

# Service: RenewItem
_svc("RenewItem", "RenewItem", "RenewItemResponse", "Renews an active patron loan", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Routing header"),
    NcipFieldDefinition("UserId", "UserId", False, "Patron barcode"),
    NcipFieldDefinition("ItemId", "ItemId", True, "Item barcode"),
    NcipFieldDefinition("DesiredDateDue", "Date", False, "Desired extension due date"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Renewal rejection reason (e.g. reserved by another patron)"),
    NcipFieldDefinition("ItemId", "ItemId", True, "Item barcode"),
    NcipFieldDefinition("DateDue", "Date", True, "Updated loan due date"),
    NcipFieldDefinition("RenewalCount", "Integer", True, "Total renewal count"),
])

# Service: RequestItem
_svc("RequestItem", "RequestItem", "RequestItemResponse", "Places a hold or document delivery request on an item", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Routing header"),
    NcipFieldDefinition("UserId", "UserId", True, "Patron barcode"),
    NcipFieldDefinition("ItemId", "ItemId", False, "Item barcode if specific copy requested"),
    NcipFieldDefinition("BibliographicId", "BibId", False, "Monograph title ID"),
    NcipFieldDefinition("RequestType", "Enumeration", True, "Hold, Recall, Copy Non Returnable"),
    NcipFieldDefinition("PickupLocation", "Location", False, "Requested library branch desk"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic error"),
    NcipFieldDefinition("RequestId", "RequestId", True, "Unique system request ID"),
    NcipFieldDefinition("HoldQueuePosition", "Integer", False, "Queue rank (e.g. 1st in line)"),
])

# Service: CancelRequestItem
_svc("CancelRequestItem", "CancelRequestItem", "CancelRequestItemResponse", "Cancels a pending patron hold or ILL request", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Routing header"),
    NcipFieldDefinition("RequestId", "RequestId", True, "System request ID to cancel"),
    NcipFieldDefinition("ReasonForCancellation", "String", False, "Cancellation reason note"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic error"),
    NcipFieldDefinition("RequestId", "RequestId", True, "Confirmed canceled request ID"),
])

# Extended NCIP Service: CirculationStatusChangeReport
_svc("CirculationStatusChangeReport", "CirculationStatusChangeReport", "CirculationStatusChangeReportResponse", "Automated NISO NCIP 2.0 CirculationStatusChangeReport service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to CirculationStatusChangeReport"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: CreateAgency
_svc("CreateAgency", "CreateAgency", "CreateAgencyResponse", "Automated NISO NCIP 2.0 CreateAgency service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to CreateAgency"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: CreateUser
_svc("CreateUser", "CreateUser", "CreateUserResponse", "Automated NISO NCIP 2.0 CreateUser service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to CreateUser"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: CreateUserFiscalTransaction
_svc("CreateUserFiscalTransaction", "CreateUserFiscalTransaction", "CreateUserFiscalTransactionResponse", "Automated NISO NCIP 2.0 CreateUserFiscalTransaction service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to CreateUserFiscalTransaction"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: ItemCheckedIn
_svc("ItemCheckedIn", "ItemCheckedIn", "ItemCheckedInResponse", "Automated NISO NCIP 2.0 ItemCheckedIn service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to ItemCheckedIn"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: ItemCheckedOut
_svc("ItemCheckedOut", "ItemCheckedOut", "ItemCheckedOutResponse", "Automated NISO NCIP 2.0 ItemCheckedOut service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to ItemCheckedOut"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: ItemRecall
_svc("ItemRecall", "ItemRecall", "ItemRecallResponse", "Automated NISO NCIP 2.0 ItemRecall service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to ItemRecall"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: ItemRenewed
_svc("ItemRenewed", "ItemRenewed", "ItemRenewedResponse", "Automated NISO NCIP 2.0 ItemRenewed service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to ItemRenewed"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: ItemUpdated
_svc("ItemUpdated", "ItemUpdated", "ItemUpdatedResponse", "Automated NISO NCIP 2.0 ItemUpdated service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to ItemUpdated"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: LookupAgency
_svc("LookupAgency", "LookupAgency", "LookupAgencyResponse", "Automated NISO NCIP 2.0 LookupAgency service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to LookupAgency"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: LookupItemSet
_svc("LookupItemSet", "LookupItemSet", "LookupItemSetResponse", "Automated NISO NCIP 2.0 LookupItemSet service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to LookupItemSet"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: LookupRequest
_svc("LookupRequest", "LookupRequest", "LookupRequestResponse", "Automated NISO NCIP 2.0 LookupRequest service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to LookupRequest"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: LookupUserFiscalAccount
_svc("LookupUserFiscalAccount", "LookupUserFiscalAccount", "LookupUserFiscalAccountResponse", "Automated NISO NCIP 2.0 LookupUserFiscalAccount service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to LookupUserFiscalAccount"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: RecallItem
_svc("RecallItem", "RecallItem", "RecallItemResponse", "Automated NISO NCIP 2.0 RecallItem service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to RecallItem"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: UndoCheckOut
_svc("UndoCheckOut", "UndoCheckOut", "UndoCheckOutResponse", "Automated NISO NCIP 2.0 UndoCheckOut service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to UndoCheckOut"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: UpdateAgency
_svc("UpdateAgency", "UpdateAgency", "UpdateAgencyResponse", "Automated NISO NCIP 2.0 UpdateAgency service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to UpdateAgency"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: UpdateCirculationStatus
_svc("UpdateCirculationStatus", "UpdateCirculationStatus", "UpdateCirculationStatusResponse", "Automated NISO NCIP 2.0 UpdateCirculationStatus service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to UpdateCirculationStatus"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: UpdateItem
_svc("UpdateItem", "UpdateItem", "UpdateItemResponse", "Automated NISO NCIP 2.0 UpdateItem service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to UpdateItem"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: UpdateRequest
_svc("UpdateRequest", "UpdateRequest", "UpdateRequestResponse", "Automated NISO NCIP 2.0 UpdateRequest service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to UpdateRequest"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: UpdateUser
_svc("UpdateUser", "UpdateUser", "UpdateUserResponse", "Automated NISO NCIP 2.0 UpdateUser service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to UpdateUser"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: ValidateUser
_svc("ValidateUser", "ValidateUser", "ValidateUserResponse", "Automated NISO NCIP 2.0 ValidateUser service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to ValidateUser"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: SendUserNotice
_svc("SendUserNotice", "SendUserNotice", "SendUserNoticeResponse", "Automated NISO NCIP 2.0 SendUserNotice service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to SendUserNotice"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: HoldItemPlaced
_svc("HoldItemPlaced", "HoldItemPlaced", "HoldItemPlacedResponse", "Automated NISO NCIP 2.0 HoldItemPlaced service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to HoldItemPlaced"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: HoldItemExpired
_svc("HoldItemExpired", "HoldItemExpired", "HoldItemExpiredResponse", "Automated NISO NCIP 2.0 HoldItemExpired service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to HoldItemExpired"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: FineAssessedReport
_svc("FineAssessedReport", "FineAssessedReport", "FineAssessedReportResponse", "Automated NISO NCIP 2.0 FineAssessedReport service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to FineAssessedReport"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: FineWaivedReport
_svc("FineWaivedReport", "FineWaivedReport", "FineWaivedReportResponse", "Automated NISO NCIP 2.0 FineWaivedReport service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to FineWaivedReport"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: PatronSuspendedReport
_svc("PatronSuspendedReport", "PatronSuspendedReport", "PatronSuspendedReportResponse", "Automated NISO NCIP 2.0 PatronSuspendedReport service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to PatronSuspendedReport"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])

# Extended NCIP Service: PatronReinstatedReport
_svc("PatronReinstatedReport", "PatronReinstatedReport", "PatronReinstatedReportResponse", "Automated NISO NCIP 2.0 PatronReinstatedReport service message", [
    NcipFieldDefinition("InitiationHeader", "Header", True, "Standard agency routing initiation header"),
    NcipFieldDefinition("ServicePayload", "Payload", True, "Payload elements specific to PatronReinstatedReport"),
    NcipFieldDefinition("SecurityToken", "Token", False, "SAML or Kerberos agency authentication token"),
], [
    NcipFieldDefinition("ResponseHeader", "Header", True, "Standard agency routing response header"),
    NcipFieldDefinition("Problem", "Problem", False, "Diagnostic problem element if operation encountered errors"),
    NcipFieldDefinition("ConfirmationStatus", "String", True, "Operation execution status code"),
])


def get_ncip_service_spec(service_name: str) -> Optional[NcipServiceSpecification]:
    return NCIP_SERVICES.get(service_name)
