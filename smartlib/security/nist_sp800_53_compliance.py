"""NIST SP 800-53 Rev. 5 Security Controls Catalog for Library Information Systems.

Defines access control, audit, identification & authentication, system integrity,
and contingency controls required for enterprise university and governmental libraries.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class NistSecurityControl:
    control_id: str
    family_code: str
    family_name: str
    title: str
    baseline_impact: str  # 'LOW', 'MODERATE', 'HIGH'
    description: str
    smartlib_implementation: str
    audit_event_types: List[str] = field(default_factory=list)


NIST_CONTROLS_REGISTRY: Dict[str, NistSecurityControl] = {}


def _nist(cid: str, fam_code: str, fam_name: str, title: str, baseline: str, desc: str, impl: str, evts: List[str]):
    NIST_CONTROLS_REGISTRY[cid] = NistSecurityControl(
        control_id=cid,
        family_code=fam_code,
        family_name=fam_name,
        title=title,
        baseline_impact=baseline,
        description=desc,
        smartlib_implementation=impl,
        audit_event_types=evts
    )

_nist(
    cid="AC-1",
    fam_code="AC",
    fam_name="Access Control",
    title="Policy and Procedures",
    baseline="LOW",
    desc="Establish and maintain access control policy and operational procedures",
    impl="Documented in SmartLib RBAC documentation and security policy matrix",
    evts=['POLICY_REVIEW', 'ADMIN_AUDIT']
)
_nist(
    cid="AC-2",
    fam_code="AC",
    fam_name="Access Control",
    title="Account Management",
    baseline="LOW",
    desc="Manage system accounts, roles, approvals, and credentials",
    impl="Handled via UserService, User model, and automatic deactivation hooks",
    evts=['USER_CREATE', 'USER_UPDATE', 'USER_DEACTIVATE']
)
_nist(
    cid="AC-3",
    fam_code="AC",
    fam_name="Access Control",
    title="Access Enforcement",
    baseline="LOW",
    desc="Enforce approved authorizations for logical access to information",
    impl="RBAC decorator guards @require_role and ABAC rule engine",
    evts=['AUTH_CHECK', 'ACCESS_DENIED']
)
_nist(
    cid="AC-4",
    fam_code="AC",
    fam_name="Access Control",
    title="Information Flow Enforcement",
    baseline="MODERATE",
    desc="Enforce approved authorizations for controlling information flow",
    impl="Restricts patron access exclusively to their own loan records and fines",
    evts=['DATA_TRANSFER', 'EXPORT_AUDIT']
)
_nist(
    cid="AC-5",
    fam_code="AC",
    fam_name="Access Control",
    title="Separation of Duties",
    baseline="MODERATE",
    desc="Enforce separation of duties through assigned access authorizations",
    impl="Separates Cashier payment collection from Administrative fee waivers",
    evts=['CASHIER_PAYMENT', 'FINE_WAIVE']
)
_nist(
    cid="AC-6",
    fam_code="AC",
    fam_name="Access Control",
    title="Least Privilege",
    baseline="LOW",
    desc="Employ the principle of least privilege, allowing only necessary authorized accesses",
    impl="Role-based scopes limit circulation staff from accessing full system audit logs",
    evts=['PRIVILEGE_ELEVATION', 'ROLE_ASSIGN']
)
_nist(
    cid="AC-7",
    fam_code="AC",
    fam_name="Access Control",
    title="Unsuccessful Logon Attempts",
    baseline="LOW",
    desc="Enforce a limit of consecutive invalid logon attempts",
    impl="Account lockout after 5 consecutive failed authentication attempts",
    evts=['LOGIN_FAILED', 'ACCOUNT_LOCKED']
)
_nist(
    cid="AC-8",
    fam_code="AC",
    fam_name="Access Control",
    title="System Use Notification",
    baseline="LOW",
    desc="Display system use notification message before granting access",
    impl="Displays authorized use terms on login portal footer",
    evts=['BANNER_DISPLAY']
)
_nist(
    cid="AC-14",
    fam_code="AC",
    fam_name="Access Control",
    title="Permitted Actions without Identification or Authentication",
    baseline="LOW",
    desc="Identify and document user actions permitted without authentication",
    impl="OPAC public catalog browsing and book search allowed anonymously",
    evts=['PUBLIC_SEARCH']
)
_nist(
    cid="AC-17",
    fam_code="AC",
    fam_name="Access Control",
    title="Remote Access",
    baseline="MODERATE",
    desc="Authorize, monitor, and control remote access sessions",
    impl="Session tokens with cryptographically random identifiers and TLS encryption",
    evts=['REMOTE_SESSION', 'SESSION_EXPIRE']
)
_nist(
    cid="AT-1",
    fam_code="AT",
    fam_name="Awareness and Training",
    title="Policy and Procedures",
    baseline="LOW",
    desc="Establish and maintain security awareness training policies",
    impl="Admin guides and operational checklists for library personnel",
    evts=['TRAINING_AUDIT']
)
_nist(
    cid="AT-2",
    fam_code="AT",
    fam_name="Awareness and Training",
    title="Security Awareness Training",
    baseline="LOW",
    desc="Deliver basic security awareness training to personnel",
    impl="Periodic role-specific security prompt reminders",
    evts=['TRAINING_LOG']
)
_nist(
    cid="AU-1",
    fam_code="AU",
    fam_name="Audit and Accountability",
    title="Policy and Procedures",
    baseline="LOW",
    desc="Establish and maintain audit and accountability policies",
    impl="AuditService maintaining state differential audit logging",
    evts=['AUDIT_POLICY']
)
_nist(
    cid="AU-2",
    fam_code="AU",
    fam_name="Audit and Accountability",
    title="Event Logging",
    baseline="LOW",
    desc="Identify the types of events that the system will log",
    impl="Logs all checkout, checkin, fine assessment, waiver, and payment events",
    evts=['EVENT_LOGGED', 'AUDIT_APPEND']
)
_nist(
    cid="AU-3",
    fam_code="AU",
    fam_name="Audit and Accountability",
    title="Content of Audit Records",
    baseline="LOW",
    desc="Ensure audit records contain information to determine what occurred",
    impl="Records timestamp, actor ID, entity name, entity ID, action, and JSON payload",
    evts=['AUDIT_RECORD_STRUCTURE']
)
_nist(
    cid="AU-4",
    fam_code="AU",
    fam_name="Audit and Accountability",
    title="Audit Storage Capacity",
    baseline="LOW",
    desc="Allocate audit record storage capacity to prevent exhaustion",
    impl="Database-backed transactional WAL logging with automated archiving",
    evts=['CAPACITY_ALERT']
)
_nist(
    cid="AU-5",
    fam_code="AU",
    fam_name="Audit and Accountability",
    title="Response to Audit Processing Failures",
    baseline="LOW",
    desc="Alert designated personnel in the event of an audit processing failure",
    impl="System exceptions raised if transactional audit logging fails to commit",
    evts=['AUDIT_FAILURE_ALERT']
)
_nist(
    cid="AU-6",
    fam_code="AU",
    fam_name="Audit and Accountability",
    title="Audit Review, Analysis, and Reporting",
    baseline="LOW",
    desc="Review and analyze system audit records for indications of unusual activity",
    impl="Admin dashboard audit log filtering, inspection, and anomaly alerts",
    evts=['AUDIT_INSPECT', 'FILTER_APPLIED']
)
_nist(
    cid="AU-8",
    fam_code="AU",
    fam_name="Audit and Accountability",
    title="Time Stamps",
    baseline="LOW",
    desc="Use internal system clocks to generate timestamps for audit records",
    impl="All records stamped with ISO 8601 UTC / local microsecond precision",
    evts=['TIMESTAMP_CHECK']
)
_nist(
    cid="AU-9",
    fam_code="AU",
    fam_name="Audit and Accountability",
    title="Protection of Audit Information",
    baseline="MODERATE",
    desc="Protect audit information and tools from unauthorized access and modification",
    impl="Append-only database journal table with restricted write permissions",
    evts=['TAMPER_DETECT']
)
_nist(
    cid="IA-1",
    fam_code="IA",
    fam_name="Identification and Authentication",
    title="Policy and Procedures",
    baseline="LOW",
    desc="Establish and maintain identification and authentication policies",
    impl="SmartLib Authentication documentation",
    evts=['AUTH_POLICY']
)
_nist(
    cid="IA-2",
    fam_code="IA",
    fam_name="Identification and Authentication",
    title="Identification and Authentication (Organizational Users)",
    baseline="LOW",
    desc="Uniquely identify and authenticate organizational users",
    impl="Unique usernames, email uniqueness constraint, and PBKDF2 hashed passwords",
    evts=['USER_IDENTIFIED', 'CREDENTIAL_VERIFY']
)
_nist(
    cid="IA-4",
    fam_code="IA",
    fam_name="Identification and Authentication",
    title="Identifier Management",
    baseline="LOW",
    desc="Manage information system identifiers by uniquely assigning each to an entity",
    impl="Serialized patron codes MEM-YYYY-XXXX and employee codes EMP-XXXX",
    evts=['IDENTIFIER_MINTED']
)
_nist(
    cid="IA-5",
    fam_code="IA",
    fam_name="Identification and Authentication",
    title="Authenticator Management",
    baseline="LOW",
    desc="Manage information system authenticators including passwords, keys, and tokens",
    impl="PBKDF2 HMAC SHA-256 with per-user 16-byte random cryptographic salt",
    evts=['PASSWORD_CHANGE', 'SALT_GENERATE']
)
_nist(
    cid="IA-7",
    fam_code="IA",
    fam_name="Identification and Authentication",
    title="Cryptographic Module Authentication",
    baseline="MODERATE",
    desc="Employ authentication mechanisms that meet requirements of FIPS standards",
    impl="Python hashlib and standard cryptographic primitives",
    evts=['FIPS_AUDIT']
)
_nist(
    cid="SC-1",
    fam_code="SC",
    fam_name="System and Communications Protection",
    title="Policy and Procedures",
    baseline="LOW",
    desc="Establish and maintain communications protection policy",
    impl="TLS configuration requirements for web interface and API endpoints",
    evts=['COMM_POLICY']
)
_nist(
    cid="SC-8",
    fam_code="SC",
    fam_name="System and Communications Protection",
    title="Transmission Confidentiality and Integrity",
    baseline="MODERATE",
    desc="Protect confidentiality and integrity of transmitted information",
    impl="HTTPS and secure WebSocket connections for all patron transactions",
    evts=['TLS_VERIFY']
)
_nist(
    cid="SC-13",
    fam_code="SC",
    fam_name="System and Communications Protection",
    title="Cryptographic Protection",
    baseline="LOW",
    desc="Implement cryptographic modules in accordance with applicable laws",
    impl="Modern cryptographic standards: SHA-256, AES-256-GCM, and PBKDF2",
    evts=['CRYPTO_SELFTEST']
)
_nist(
    cid="SI-1",
    fam_code="SI",
    fam_name="System and Information Integrity",
    title="Policy and Procedures",
    baseline="LOW",
    desc="Establish system and information integrity policies",
    impl="Software deployment, data validation, and input sanitization policies",
    evts=['INTEGRITY_POLICY']
)
_nist(
    cid="SI-2",
    fam_code="SI",
    fam_name="System and Information Integrity",
    title="Flaw Remediation",
    baseline="LOW",
    desc="Identify, report, and correct information system flaws",
    impl="Strict unit test coverage enforcing all domain invariant validation rules",
    evts=['FLAW_REMEDIATION', 'TEST_SUITE']
)
_nist(
    cid="SI-10",
    fam_code="SI",
    fam_name="System and Information Integrity",
    title="Information Input Validation",
    baseline="LOW",
    desc="Check the validity of information inputs to the system",
    impl="Rigorous validation for ISBN-10/13 checksums, barcodes, amounts, dates",
    evts=['INPUT_VALIDATION_ERROR']
)
_nist(
    cid="CP-1",
    fam_code="CP",
    fam_name="Contingency Planning",
    title="Contingency Planning Policy and Procedures",
    baseline="LOW",
    desc="Disaster recovery, backup procedures, and continuous operations plans",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "CP_VERIFY"]
)
_nist(
    cid="CP-2",
    fam_code="CP",
    fam_name="Contingency Planning",
    title="Contingency Plan Development",
    baseline="LOW",
    desc="Develop and implement contingency plan addressing critical library circulation operations",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "CP_VERIFY"]
)
_nist(
    cid="CP-9",
    fam_code="CP",
    fam_name="Contingency Planning",
    title="Information System Backup",
    baseline="LOW",
    desc="Conduct user-level and system-level backups of SQLite database files",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "CP_VERIFY"]
)
_nist(
    cid="CP-10",
    fam_code="CP",
    fam_name="Contingency Planning",
    title="Information System Recovery and Reconstitution",
    baseline="LOW",
    desc="Restore database integrity and catalog consistency from transaction logs",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "CP_VERIFY"]
)
_nist(
    cid="IR-1",
    fam_code="IR",
    fam_name="Incident Response",
    title="Incident Response Policy and Procedures",
    baseline="LOW",
    desc="Procedures for detecting, analyzing, containing, and recovering from incidents",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "IR_VERIFY"]
)
_nist(
    cid="IR-2",
    fam_code="IR",
    fam_name="Incident Response",
    title="Incident Response Training",
    baseline="LOW",
    desc="Staff training for security breaches and patron data privacy incidents",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "IR_VERIFY"]
)
_nist(
    cid="IR-4",
    fam_code="IR",
    fam_name="Incident Response",
    title="Incident Handling",
    baseline="LOW",
    desc="Incident containment and eradication procedures",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "IR_VERIFY"]
)
_nist(
    cid="IR-6",
    fam_code="IR",
    fam_name="Incident Response",
    title="Incident Reporting",
    baseline="LOW",
    desc="Timely incident reporting to library dean and campus CISO",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "IR_VERIFY"]
)
_nist(
    cid="RA-1",
    fam_code="RA",
    fam_name="Risk Assessment",
    title="Risk Assessment Policy and Procedures",
    baseline="LOW",
    desc="Periodic evaluation of vulnerability vectors and threat likelihoods",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "RA_VERIFY"]
)
_nist(
    cid="RA-3",
    fam_code="RA",
    fam_name="Risk Assessment",
    title="Risk Assessment",
    baseline="LOW",
    desc="Formal risk assessments for all patron PII and financial records",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "RA_VERIFY"]
)
_nist(
    cid="SA-1",
    fam_code="SA",
    fam_name="System and Services Acquisition",
    title="Acquisition Policy and Procedures",
    baseline="LOW",
    desc="Supply chain risk management for acquisitions hardware and third-party software",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "SA_VERIFY"]
)
_nist(
    cid="SA-4",
    fam_code="SA",
    fam_name="System and Services Acquisition",
    title="Acquisition Development",
    baseline="LOW",
    desc="Security functional requirements specified in vendor RFPs",
    impl="Standard operational security protocol implemented in SmartLib core architecture",
    evts=["SECURITY_AUDIT", "SA_VERIFY"]
)

def get_control_by_id(control_id: str) -> Optional[NistSecurityControl]:
    """Retrieve security control definition by its NIST identifier."""
    return NIST_CONTROLS_REGISTRY.get(control_id.strip().upper())


def get_controls_by_family(family_code: str) -> List[NistSecurityControl]:
    """Retrieve all controls belonging to a specified security family (e.g. 'AC', 'AU')."""
    clean = family_code.strip().upper()
    return [c for c in NIST_CONTROLS_REGISTRY.values() if c.family_code == clean]


def audit_control_compliance() -> Dict[str, int]:
    """Calculate the distribution of implemented controls across impact baselines."""
    counts = {"LOW": 0, "MODERATE": 0, "HIGH": 0}
    for ctrl in NIST_CONTROLS_REGISTRY.values():
        if ctrl.baseline_impact in counts:
            counts[ctrl.baseline_impact] += 1
    return counts
