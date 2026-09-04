"""3M SIP2 2.0 Command and Variable Field Detailed Specification Matrix."""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Sip2FieldRequirement:
    field_id: str
    field_name: str
    required: bool
    repeatable: bool
    max_length: int
    format_regex: str
    description: str


@dataclass
class Sip2CommandSpecification:
    command_code: str
    command_name: str
    is_request: bool
    fixed_field_format: str
    supported_fields: Dict[str, Sip2FieldRequirement]


SIP2_COMMAND_REGISTRY: Dict[str, Sip2CommandSpecification] = {}

def _cmd(code: str, name: str, req: bool, fixed_fmt: str, fields: List[Sip2FieldRequirement]):
    f_map = {f.field_id: f for f in fields}
    SIP2_COMMAND_REGISTRY[code] = Sip2CommandSpecification(code, name, req, fixed_fmt, f_map)

# Command 01: Block Patron Request
_cmd("01", "Block Patron Request", True, "1 char card retained + 18 chars date", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Unique barcode or card ID of patron to be blocked"),
    Sip2FieldRequirement("AC", "Terminal Password", False, False, 16, r"^.*$", "Authentication password of the client terminal"),
    Sip2FieldRequirement("AL", "Blocked Card Message", False, False, 60, r"^.*$", "Descriptive message explaining reason for blocking"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Identification code of library institution"),
])

# Command 02: Block Patron Response
_cmd("02", "Block Patron Response", False, "14 chars patron status flags + 18 chars date", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Echo of patron identifier"),
    Sip2FieldRequirement("AE", "Personal Name", False, False, 60, r"^.*$", "Patron full personal name"),
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "Text message to be shown on kiosk screen"),
    Sip2FieldRequirement("AG", "Print Line", False, True, 80, r"^.*$", "Text line to be printed on kiosk receipt"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
])

# Command 09: Checkin Request
_cmd("09", "Checkin Request", True, "1 char no-block + 18 chars date + 18 chars return date", [
    Sip2FieldRequirement("AB", "Item Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Item physical barcode"),
    Sip2FieldRequirement("AC", "Terminal Password", False, False, 16, r"^.*$", "Terminal security password"),
    Sip2FieldRequirement("AN", "Terminal Location", False, False, 30, r"^.*$", "Location of return station"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Library agency code"),
])

# Command 10: Checkin Response
_cmd("10", "Checkin Response", False, "1 char ok + 1 char resensitize + 1 char magnetic + 1 char alert + 18 chars date", [
    Sip2FieldRequirement("AA", "Patron Identifier", False, False, 30, r"^[A-Za-z0-9_-]+$", "Patron hold recipient if item is reserved"),
    Sip2FieldRequirement("AB", "Item Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Item physical barcode"),
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "Checkin confirmation screen message"),
    Sip2FieldRequirement("AG", "Print Line", False, True, 80, r"^.*$", "Return receipt receipt line"),
    Sip2FieldRequirement("AJ", "Title Identifier", False, False, 100, r"^.*$", "Monograph book title"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
    Sip2FieldRequirement("AQ", "Permanent Location", False, False, 50, r"^.*$", "Original home stack location"),
])

# Command 11: Checkout Request
_cmd("11", "Checkout Request", True, "1 char sc-renewal + 1 char no-block + 18 chars date + 18 chars desired due", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Borrowing patron barcode"),
    Sip2FieldRequirement("AB", "Item Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Checked out item barcode"),
    Sip2FieldRequirement("AC", "Terminal Password", False, False, 16, r"^.*$", "Kiosk authentication token"),
    Sip2FieldRequirement("AD", "Patron Password", False, False, 16, r"^.*$", "Patron PIN/password verification"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution identifier"),
    Sip2FieldRequirement("CH", "Item Properties", False, False, 40, r"^.*$", "Optional item properties"),
])

# Command 12: Checkout Response
_cmd("12", "Checkout Response", False, "1 char ok + 1 char renewal ok + 1 char magnetic + 1 char desensitize + 18 chars date", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Patron identifier"),
    Sip2FieldRequirement("AB", "Item Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Item barcode"),
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "Checkout confirmation or failure text"),
    Sip2FieldRequirement("AG", "Print Line", False, True, 80, r"^.*$", "Checkout date and due date receipt print line"),
    Sip2FieldRequirement("AH", "Due Date", False, False, 18, r"^[0-9]{8}\s+[0-9]{6}$", "Circulation due date"),
    Sip2FieldRequirement("AJ", "Title Identifier", False, False, 100, r"^.*$", "Book title"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Library institution code"),
])

# Command 17: Item Information Request
_cmd("17", "Item Information Request", True, "18 chars date", [
    Sip2FieldRequirement("AB", "Item Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Item barcode to look up"),
    Sip2FieldRequirement("AC", "Terminal Password", False, False, 16, r"^.*$", "Terminal security password"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Library institution code"),
])

# Command 18: Item Information Response
_cmd("18", "Item Information Response", False, "2 chars circ status + 2 chars security + 2 chars fee + 18 chars date", [
    Sip2FieldRequirement("AB", "Item Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Item barcode"),
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "Item status screen note"),
    Sip2FieldRequirement("AG", "Print Line", False, True, 80, r"^.*$", "Item info print line"),
    Sip2FieldRequirement("AH", "Due Date", False, False, 18, r"^[0-9]{8}\s+[0-9]{6}$", "Current due date if on loan"),
    Sip2FieldRequirement("AJ", "Title Identifier", False, False, 100, r"^.*$", "Title"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
    Sip2FieldRequirement("AP", "Current Location", False, False, 50, r"^.*$", "Current shelf or desk location"),
    Sip2FieldRequirement("AQ", "Permanent Location", False, False, 50, r"^.*$", "Home collection stack location"),
    Sip2FieldRequirement("BG", "Owner Institution", False, False, 30, r"^.*$", "Owning library agency"),
])

# Command 23: Patron Status Request
_cmd("23", "Patron Status Request", True, "10 chars language + 18 chars date", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Patron card barcode"),
    Sip2FieldRequirement("AC", "Terminal Password", False, False, 16, r"^.*$", "Kiosk password"),
    Sip2FieldRequirement("AD", "Patron Password", False, False, 16, r"^.*$", "Patron PIN/password"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
])

# Command 24: Patron Status Response
_cmd("24", "Patron Status Response", False, "14 chars status flags + 3 chars language + 18 chars date", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Patron identifier"),
    Sip2FieldRequirement("AE", "Personal Name", True, False, 60, r"^.*$", "Patron full name"),
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "Account status screen message"),
    Sip2FieldRequirement("AG", "Print Line", False, True, 80, r"^.*$", "Receipt print line"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
    Sip2FieldRequirement("BL", "Valid Patron", False, False, 1, r"^[YN]$", "Patron valid flag"),
    Sip2FieldRequirement("BV", "Fee Amount", False, False, 12, r"^[0-9.]+$", "Outstanding fee balance"),
])

# Command 29: Renew Request
_cmd("29", "Renew Request", True, "1 char 3rd party + 1 char no-block + 18 chars date + 18 chars desired due", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Patron barcode"),
    Sip2FieldRequirement("AB", "Item Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Item barcode"),
    Sip2FieldRequirement("AC", "Terminal Password", False, False, 16, r"^.*$", "Terminal password"),
    Sip2FieldRequirement("AD", "Patron Password", False, False, 16, r"^.*$", "Patron PIN"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
])

# Command 30: Renew Response
_cmd("30", "Renew Response", False, "1 char ok + 1 char renewal ok + 1 char magnetic + 1 char desensitize + 18 chars date", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Patron barcode"),
    Sip2FieldRequirement("AB", "Item Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Item barcode"),
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "Renewal status message"),
    Sip2FieldRequirement("AG", "Print Line", False, True, 80, r"^.*$", "New due date print line"),
    Sip2FieldRequirement("AH", "Due Date", False, False, 18, r"^[0-9]{8}\s+[0-9]{6}$", "Updated loan due date"),
    Sip2FieldRequirement("AJ", "Title Identifier", False, False, 100, r"^.*$", "Book title"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
])

# Command 37: Fee Paid Request
_cmd("37", "Fee Paid Request", True, "2 chars fee type + 2 chars payment type + 3 chars currency + 18 chars date", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Patron barcode"),
    Sip2FieldRequirement("AC", "Terminal Password", False, False, 16, r"^.*$", "Terminal password"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
    Sip2FieldRequirement("BV", "Fee Amount", True, False, 12, r"^[0-9.]+$", "Amount paid in currency"),
    Sip2FieldRequirement("CG", "Fee Identifier", False, False, 30, r"^.*$", "Fine transaction ID"),
])

# Command 38: Fee Paid Response
_cmd("38", "Fee Paid Response", False, "1 char payment accepted + 18 chars date", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Patron barcode"),
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "Payment acknowledgment text"),
    Sip2FieldRequirement("AG", "Print Line", False, True, 80, r"^.*$", "Cashier receipt line"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
    Sip2FieldRequirement("BK", "Transaction ID", False, False, 30, r"^.*$", "Payment ledger transaction ID"),
])

# Command 63: Patron Information Request
_cmd("63", "Patron Information Request", True, "10 chars language + 18 chars date + 1 char summary", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Patron barcode"),
    Sip2FieldRequirement("AC", "Terminal Password", False, False, 16, r"^.*$", "Terminal password"),
    Sip2FieldRequirement("AD", "Patron Password", False, False, 16, r"^.*$", "Patron PIN"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
    Sip2FieldRequirement("BP", "Start Item", False, False, 5, r"^[0-9]+$", "Pagination start"),
    Sip2FieldRequirement("BQ", "End Item", False, False, 5, r"^[0-9]+$", "Pagination end"),
])

# Command 64: Patron Information Response
_cmd("64", "Patron Information Response", False, "14 chars status + 3 chars lang + 18 chars date + 40 chars counts", [
    Sip2FieldRequirement("AA", "Patron Identifier", True, False, 30, r"^[A-Za-z0-9_-]+$", "Patron barcode"),
    Sip2FieldRequirement("AE", "Personal Name", True, False, 60, r"^.*$", "Patron full name"),
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "Screen message"),
    Sip2FieldRequirement("AG", "Print Line", False, True, 80, r"^.*$", "Print line"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
    Sip2FieldRequirement("AS", "Hold Items", False, True, 100, r"^.*$", "Titles awaiting pickup"),
    Sip2FieldRequirement("AT", "Overdue Items", False, True, 100, r"^.*$", "Titles currently overdue"),
    Sip2FieldRequirement("AU", "Charged Items", False, True, 100, r"^.*$", "Titles currently on loan"),
    Sip2FieldRequirement("AV", "Fine Items", False, True, 100, r"^.*$", "List of assessed unpaid fines"),
    Sip2FieldRequirement("BD", "Home Address", False, False, 100, r"^.*$", "Patron postal address"),
    Sip2FieldRequirement("BE", "Email Address", False, False, 80, r"^.*$", "Patron email"),
    Sip2FieldRequirement("BF", "Phone Number", False, False, 30, r"^.*$", "Patron telephone"),
    Sip2FieldRequirement("BV", "Fee Amount", False, False, 12, r"^[0-9.]+$", "Total unpaid dues balance"),
])

# Command 93: Login Request
_cmd("93", "Login Request", True, "1 char uid algo + 1 char pwd algo", [
    Sip2FieldRequirement("CN", "Login User Id", True, False, 30, r"^.*$", "SIP2 terminal operator username"),
    Sip2FieldRequirement("CO", "Login Password", True, False, 30, r"^.*$", "SIP2 terminal operator password"),
    Sip2FieldRequirement("CP", "Location Code", False, False, 30, r"^.*$", "Physical kiosk station branch"),
])

# Command 94: Login Response
_cmd("94", "Login Response", False, "1 char ok", [
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "Login acknowledgment"),
])

# Command 99: SC Status Request
_cmd("99", "SC Status Request", True, "1 char status code + 3 chars max print width + 4 chars protocol version", [
    Sip2FieldRequirement("AC", "Terminal Password", False, False, 16, r"^.*$", "Terminal security password"),
])

# Command 98: ACS Status Response
_cmd("98", "ACS Status Response", False, "6 chars flags + 6 chars timeouts + 18 chars date + 4 chars version", [
    Sip2FieldRequirement("AM", "Library Name", False, False, 60, r"^.*$", "Official library system name"),
    Sip2FieldRequirement("AN", "Terminal Location", False, False, 30, r"^.*$", "Location of server"),
    Sip2FieldRequirement("AO", "Institution ID", True, False, 30, r"^.*$", "Institution code"),
    Sip2FieldRequirement("AF", "Screen Message", False, True, 80, r"^.*$", "System online greeting message"),
])


def get_command_spec(command_code: str) -> Optional[Sip2CommandSpecification]:
    return SIP2_COMMAND_REGISTRY.get(command_code)
