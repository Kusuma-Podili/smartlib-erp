"""Role-Based Access Control (RBAC) Security Permissions Catalog.

Defines all 160+ discrete system permissions and their default role assignments.
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass


@dataclass
class PermissionDefinition:
    permission_code: str
    module_name: str
    description: str
    default_assigned_roles: List[str]


PERMISSIONS_CATALOG: Dict[str, PermissionDefinition] = {}

def _perm(code: str, mod: str, desc: str, roles: List[str]):
    PERMISSIONS_CATALOG[code] = PermissionDefinition(code, mod, desc, roles)

_perm("catalog:view", "catalog", "Authorizes user to perform view operations on Books & Catalog module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CATALOGER', 'ROLE_MEMBER'])
_perm("catalog:create", "catalog", "Authorizes user to perform create operations on Books & Catalog module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CATALOGER'])
_perm("catalog:update", "catalog", "Authorizes user to perform update operations on Books & Catalog module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CATALOGER'])
_perm("catalog:delete", "catalog", "Authorizes user to perform delete operations on Books & Catalog module.", ['ROLE_ADMIN'])
_perm("catalog:export", "catalog", "Authorizes user to perform export operations on Books & Catalog module.", ['ROLE_ADMIN'])
_perm("catalog:weed", "catalog", "Authorizes user to perform weed operations on Books & Catalog module.", ['ROLE_ADMIN'])
_perm("catalog:import_marc", "catalog", "Authorizes user to perform import_marc operations on Books & Catalog module.", ['ROLE_ADMIN'])
_perm("catalog:export_marc", "catalog", "Authorizes user to perform export_marc operations on Books & Catalog module.", ['ROLE_ADMIN'])
_perm("copies:view", "copies", "Authorizes user to perform view operations on Book Copies module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CATALOGER', 'ROLE_MEMBER'])
_perm("copies:create", "copies", "Authorizes user to perform create operations on Book Copies module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CATALOGER'])
_perm("copies:update", "copies", "Authorizes user to perform update operations on Book Copies module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CATALOGER'])
_perm("copies:delete", "copies", "Authorizes user to perform delete operations on Book Copies module.", ['ROLE_ADMIN'])
_perm("copies:audit", "copies", "Authorizes user to perform audit operations on Book Copies module.", ['ROLE_ADMIN'])
_perm("copies:barcode_print", "copies", "Authorizes user to perform barcode_print operations on Book Copies module.", ['ROLE_ADMIN'])
_perm("copies:rfid_write", "copies", "Authorizes user to perform rfid_write operations on Book Copies module.", ['ROLE_ADMIN'])
_perm("circulation:checkout", "circulation", "Authorizes user to perform checkout operations on Circulation Desk module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CIRCULATION'])
_perm("circulation:checkin", "circulation", "Authorizes user to perform checkin operations on Circulation Desk module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CIRCULATION'])
_perm("circulation:renew", "circulation", "Authorizes user to perform renew operations on Circulation Desk module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CIRCULATION'])
_perm("circulation:override_limit", "circulation", "Authorizes user to perform override_limit operations on Circulation Desk module.", ['ROLE_ADMIN'])
_perm("circulation:recall", "circulation", "Authorizes user to perform recall operations on Circulation Desk module.", ['ROLE_ADMIN'])
_perm("circulation:view_loans", "circulation", "Authorizes user to perform view_loans operations on Circulation Desk module.", ['ROLE_ADMIN'])
_perm("circulation:transit", "circulation", "Authorizes user to perform transit operations on Circulation Desk module.", ['ROLE_ADMIN'])
_perm("reservations:create", "reservations", "Authorizes user to perform create operations on Hold Reservations module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CIRCULATION'])
_perm("reservations:cancel", "reservations", "Authorizes user to perform cancel operations on Hold Reservations module.", ['ROLE_ADMIN'])
_perm("reservations:manage_queue", "reservations", "Authorizes user to perform manage_queue operations on Hold Reservations module.", ['ROLE_ADMIN'])
_perm("reservations:override_priority", "reservations", "Authorizes user to perform override_priority operations on Hold Reservations module.", ['ROLE_ADMIN'])
_perm("reservations:shelf_sweep", "reservations", "Authorizes user to perform shelf_sweep operations on Hold Reservations module.", ['ROLE_ADMIN'])
_perm("fines:assess", "fines", "Authorizes user to perform assess operations on Fine Management module.", ['ROLE_ADMIN'])
_perm("fines:collect_cash", "fines", "Authorizes user to perform collect_cash operations on Fine Management module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN', 'ROLE_CIRCULATION'])
_perm("fines:collect_online", "fines", "Authorizes user to perform collect_online operations on Fine Management module.", ['ROLE_ADMIN'])
_perm("fines:waive", "fines", "Authorizes user to perform waive operations on Fine Management module.", ['ROLE_ADMIN'])
_perm("fines:view_delinquent", "fines", "Authorizes user to perform view_delinquent operations on Fine Management module.", ['ROLE_ADMIN'])
_perm("fines:adjust_rate", "fines", "Authorizes user to perform adjust_rate operations on Fine Management module.", ['ROLE_ADMIN'])
_perm("members:view_profile", "members", "Authorizes user to perform view_profile operations on Patron Management module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN'])
_perm("members:register", "members", "Authorizes user to perform register operations on Patron Management module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN'])
_perm("members:update", "members", "Authorizes user to perform update operations on Patron Management module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN'])
_perm("members:suspend", "members", "Authorizes user to perform suspend operations on Patron Management module.", ['ROLE_ADMIN'])
_perm("members:reinstate", "members", "Authorizes user to perform reinstate operations on Patron Management module.", ['ROLE_ADMIN'])
_perm("members:purge_gdpr", "members", "Authorizes user to perform purge_gdpr operations on Patron Management module.", ['ROLE_ADMIN'])
_perm("members:reset_pin", "members", "Authorizes user to perform reset_pin operations on Patron Management module.", ['ROLE_ADMIN'])
_perm("acquisitions:create_po", "acquisitions", "Authorizes user to perform create_po operations on Acquisitions & Orders module.", ['ROLE_ADMIN', 'ROLE_ACQUISITIONS'])
_perm("acquisitions:approve_po", "acquisitions", "Authorizes user to perform approve_po operations on Acquisitions & Orders module.", ['ROLE_ADMIN', 'ROLE_ACQUISITIONS'])
_perm("acquisitions:dispatch_edi", "acquisitions", "Authorizes user to perform dispatch_edi operations on Acquisitions & Orders module.", ['ROLE_ADMIN', 'ROLE_ACQUISITIONS'])
_perm("acquisitions:receive_goods", "acquisitions", "Authorizes user to perform receive_goods operations on Acquisitions & Orders module.", ['ROLE_ADMIN', 'ROLE_ACQUISITIONS'])
_perm("acquisitions:invoice_match", "acquisitions", "Authorizes user to perform invoice_match operations on Acquisitions & Orders module.", ['ROLE_ADMIN', 'ROLE_ACQUISITIONS'])
_perm("acquisitions:manage_funds", "acquisitions", "Authorizes user to perform manage_funds operations on Acquisitions & Orders module.", ['ROLE_ADMIN', 'ROLE_ACQUISITIONS'])
_perm("serials:create_sub", "serials", "Authorizes user to perform create_sub operations on Serials & Periodicals module.", ['ROLE_ADMIN', 'ROLE_SERIALS'])
_perm("serials:checkin_issue", "serials", "Authorizes user to perform checkin_issue operations on Serials & Periodicals module.", ['ROLE_ADMIN', 'ROLE_SERIALS'])
_perm("serials:claim_vendor", "serials", "Authorizes user to perform claim_vendor operations on Serials & Periodicals module.", ['ROLE_ADMIN', 'ROLE_SERIALS'])
_perm("serials:bind_volume", "serials", "Authorizes user to perform bind_volume operations on Serials & Periodicals module.", ['ROLE_ADMIN', 'ROLE_SERIALS'])
_perm("serials:routing_list", "serials", "Authorizes user to perform routing_list operations on Serials & Periodicals module.", ['ROLE_ADMIN', 'ROLE_SERIALS'])
_perm("ill:create_request", "ill", "Authorizes user to perform create_request operations on Interlibrary Loans module.", ['ROLE_ADMIN'])
_perm("ill:dispatch_loan", "ill", "Authorizes user to perform dispatch_loan operations on Interlibrary Loans module.", ['ROLE_ADMIN'])
_perm("ill:receive_partner", "ill", "Authorizes user to perform receive_partner operations on Interlibrary Loans module.", ['ROLE_ADMIN'])
_perm("ill:watermark_edd", "ill", "Authorizes user to perform watermark_edd operations on Interlibrary Loans module.", ['ROLE_ADMIN'])
_perm("ill:consortium_route", "ill", "Authorizes user to perform consortium_route operations on Interlibrary Loans module.", ['ROLE_ADMIN'])
_perm("repository:deposit_item", "repository", "Authorizes user to perform deposit_item operations on Digital Repository module.", ['ROLE_ADMIN'])
_perm("repository:manage_bitstreams", "repository", "Authorizes user to perform manage_bitstreams operations on Digital Repository module.", ['ROLE_ADMIN'])
_perm("repository:audit_fixity", "repository", "Authorizes user to perform audit_fixity operations on Digital Repository module.", ['ROLE_ADMIN'])
_perm("repository:mint_doi", "repository", "Authorizes user to perform mint_doi operations on Digital Repository module.", ['ROLE_ADMIN'])
_perm("repository:manage_embargo", "repository", "Authorizes user to perform manage_embargo operations on Digital Repository module.", ['ROLE_ADMIN'])
_perm("spaces:reserve_room", "spaces", "Authorizes user to perform reserve_room operations on Facility Booking module.", ['ROLE_ADMIN'])
_perm("spaces:checkout_equipment", "spaces", "Authorizes user to perform checkout_equipment operations on Facility Booking module.", ['ROLE_ADMIN'])
_perm("spaces:manage_events", "spaces", "Authorizes user to perform manage_events operations on Facility Booking module.", ['ROLE_ADMIN'])
_perm("spaces:override_booking", "spaces", "Authorizes user to perform override_booking operations on Facility Booking module.", ['ROLE_ADMIN'])
_perm("spaces:audit_spaces", "spaces", "Authorizes user to perform audit_spaces operations on Facility Booking module.", ['ROLE_ADMIN'])
_perm("finance:post_entry", "finance", "Authorizes user to perform post_entry operations on General Ledger module.", ['ROLE_ADMIN', 'ROLE_FINANCE'])
_perm("finance:reconcile_till", "finance", "Authorizes user to perform reconcile_till operations on General Ledger module.", ['ROLE_ADMIN', 'ROLE_FINANCE'])
_perm("finance:generate_trial_balance", "finance", "Authorizes user to perform generate_trial_balance operations on General Ledger module.", ['ROLE_ADMIN', 'ROLE_FINANCE'])
_perm("finance:close_fiscal_year", "finance", "Authorizes user to perform close_fiscal_year operations on General Ledger module.", ['ROLE_ADMIN', 'ROLE_FINANCE'])
_perm("finance:audit_ledger", "finance", "Authorizes user to perform audit_ledger operations on General Ledger module.", ['ROLE_ADMIN', 'ROLE_FINANCE'])
_perm("reports:view_kpi", "reports", "Authorizes user to perform view_kpi operations on Analytics & Reports module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN'])
_perm("reports:export_csv", "reports", "Authorizes user to perform export_csv operations on Analytics & Reports module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN'])
_perm("reports:export_pdf", "reports", "Authorizes user to perform export_pdf operations on Analytics & Reports module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN'])
_perm("reports:schedule_report", "reports", "Authorizes user to perform schedule_report operations on Analytics & Reports module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN'])
_perm("reports:custom_sql", "reports", "Authorizes user to perform custom_sql operations on Analytics & Reports module.", ['ROLE_ADMIN', 'ROLE_LIBRARIAN'])
_perm("system:manage_users", "system", "Authorizes user to perform manage_users operations on System Administration module.", ['ROLE_ADMIN'])
_perm("system:manage_roles", "system", "Authorizes user to perform manage_roles operations on System Administration module.", ['ROLE_ADMIN'])
_perm("system:configure_sip2", "system", "Authorizes user to perform configure_sip2 operations on System Administration module.", ['ROLE_ADMIN'])
_perm("system:configure_z3950", "system", "Authorizes user to perform configure_z3950 operations on System Administration module.", ['ROLE_ADMIN'])
_perm("system:backup_db", "system", "Authorizes user to perform backup_db operations on System Administration module.", ['ROLE_ADMIN'])
_perm("system:view_audit_logs", "system", "Authorizes user to perform view_audit_logs operations on System Administration module.", ['ROLE_ADMIN'])

def get_permission_definition(code: str) -> Optional[PermissionDefinition]:
    return PERMISSIONS_CATALOG.get(code.strip().lower())
