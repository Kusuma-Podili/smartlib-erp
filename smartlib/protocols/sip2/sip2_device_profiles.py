"""3M SIP2 Self-Check Kiosk and Automated Material Handling (AMH) Hardware Profiles.

Defines terminal profiles for Bibliotheca, Lyngsoe Sortation Systems, FE Technologies,
and 3M SelfCheck kiosks, including timeout settings, supported SIP2 commands, and character sets.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Sip2TerminalProfile:
    terminal_id: str
    manufacturer: str
    model_name: str
    supported_protocols: List[str]
    max_packet_length: int
    heartbeat_interval_sec: int
    supports_offline_mode: bool
    requires_crc: bool
    supported_commands: List[str] = field(default_factory=list)
    screen_width_chars: int = 40
    notes: str = ""


SIP2_TERMINALS: Dict[str, Sip2TerminalProfile] = {}


def _term(tid: str, mfr: str, model: str, protos: List[str], max_len: int, hb: int,
          offline: bool, crc: bool, cmds: List[str], width: int, notes: str):
    SIP2_TERMINALS[tid] = Sip2TerminalProfile(
        terminal_id=tid,
        manufacturer=mfr,
        model_name=model,
        supported_protocols=protos,
        max_packet_length=max_len,
        heartbeat_interval_sec=hb,
        supports_offline_mode=offline,
        requires_crc=crc,
        supported_commands=cmds,
        screen_width_chars=width,
        notes=notes
    )

_term(
    tid="BIBLIO-SC-01",
    mfr="Bibliotheca",
    model="smartserve-1000",
    protos=['SIP2', 'ISO28560'],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=['09', '11', '17', '23', '29', '35', '37', '63', '65', '93', '97'],
    width=40,
    notes="Standard patron self-service lending kiosk with capacitive touchscreen"
)
_term(
    tid="BIBLIO-SC-02",
    mfr="Bibliotheca",
    model="smartserve-hybrid",
    protos=['SIP2', 'ISO28560'],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=['09', '11', '17', '23', '29', '35', '37', '63', '65', '93', '97'],
    width=40,
    notes="Dual barcode and high-frequency RFID patron checkout and return terminal"
)
_term(
    tid="LYNGSOE-AMH-01",
    mfr="Lyngsoe Systems",
    model="SortMate-5",
    protos=['SIP2'],
    max_len=2048,
    hb=10,
    offline=False,
    crc=True,
    cmds=['09', '11', '93', '97'],
    width=80,
    notes="Automated 5-bin materials sortation handling system for automated book drop"
)
_term(
    tid="LYNGSOE-AMH-02",
    mfr="Lyngsoe Systems",
    model="SortMate-12",
    protos=['SIP2'],
    max_len=2048,
    hb=10,
    offline=False,
    crc=True,
    cmds=['09', '11', '93', '97'],
    width=80,
    notes="High-capacity 12-bin branching materials sorter with optical barcode scanner"
)
_term(
    tid="3M-SC-8210",
    mfr="3M Library Systems",
    model="SelfCheck 8210",
    protos=['SIP2'],
    max_len=512,
    hb=60,
    offline=True,
    crc=False,
    cmds=['09', '11', '17', '29', '35', '93', '97'],
    width=40,
    notes="Legacy 3M checkout terminal with electromagnetic tattle-tape desensitizer"
)
_term(
    tid="3M-SC-VSeries",
    mfr="3M Library Systems",
    model="V-Series SelfCheck",
    protos=['SIP2', 'ISO28560'],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=['09', '11', '17', '23', '29', '35', '37', '63', '65', '93', '97'],
    width=40,
    notes="Modern 3M kiosk with receipt thermal printer and magnetic stripe patron reader"
)
_term(
    tid="FETECH-K-01",
    mfr="FE Technologies",
    model="Smart Station V3",
    protos=['SIP2', 'ISO28560'],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=['09', '11', '17', '23', '29', '35', '37', '63', '65', '93', '97'],
    width=40,
    notes="Touchless RFID checkout station supporting multi-item simultaneously scanned loans"
)
_term(
    tid="D-TECH-01",
    mfr="D-Tech International",
    model="App-It Kiosk",
    protos=['SIP2'],
    max_len=1024,
    hb=45,
    offline=True,
    crc=True,
    cmds=['09', '11', '17', '29', '35', '93', '97'],
    width=40,
    notes="Patron self-checkout terminal with integrated barcode scanner and thermal slip printer"
)
_term(
    tid="KIOSK-BR-001",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-001"
)
_term(
    tid="KIOSK-BR-002",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-002"
)
_term(
    tid="KIOSK-BR-003",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-003"
)
_term(
    tid="KIOSK-BR-004",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-004"
)
_term(
    tid="KIOSK-BR-005",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-005"
)
_term(
    tid="KIOSK-BR-006",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-006"
)
_term(
    tid="KIOSK-BR-007",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-007"
)
_term(
    tid="KIOSK-BR-008",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-008"
)
_term(
    tid="KIOSK-BR-009",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-009"
)
_term(
    tid="KIOSK-BR-010",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-010"
)
_term(
    tid="KIOSK-BR-011",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-011"
)
_term(
    tid="KIOSK-BR-012",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-012"
)
_term(
    tid="KIOSK-BR-013",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-013"
)
_term(
    tid="KIOSK-BR-014",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-014"
)
_term(
    tid="KIOSK-BR-015",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-015"
)
_term(
    tid="KIOSK-BR-016",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-016"
)
_term(
    tid="KIOSK-BR-017",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-017"
)
_term(
    tid="KIOSK-BR-018",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-018"
)
_term(
    tid="KIOSK-BR-019",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-019"
)
_term(
    tid="KIOSK-BR-020",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-020"
)
_term(
    tid="KIOSK-BR-021",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-021"
)
_term(
    tid="KIOSK-BR-022",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-022"
)
_term(
    tid="KIOSK-BR-023",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-023"
)
_term(
    tid="KIOSK-BR-024",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-024"
)
_term(
    tid="KIOSK-BR-025",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-025"
)
_term(
    tid="KIOSK-BR-026",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-026"
)
_term(
    tid="KIOSK-BR-027",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-027"
)
_term(
    tid="KIOSK-BR-028",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-028"
)
_term(
    tid="KIOSK-BR-029",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-029"
)
_term(
    tid="KIOSK-BR-030",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-030"
)
_term(
    tid="KIOSK-BR-031",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-031"
)
_term(
    tid="KIOSK-BR-032",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-032"
)
_term(
    tid="KIOSK-BR-033",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-033"
)
_term(
    tid="KIOSK-BR-034",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-034"
)
_term(
    tid="KIOSK-BR-035",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-035"
)
_term(
    tid="KIOSK-BR-036",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-036"
)
_term(
    tid="KIOSK-BR-037",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-037"
)
_term(
    tid="KIOSK-BR-038",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-038"
)
_term(
    tid="KIOSK-BR-039",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-039"
)
_term(
    tid="KIOSK-BR-040",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-040"
)
_term(
    tid="KIOSK-BR-041",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-041"
)
_term(
    tid="KIOSK-BR-042",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-042"
)
_term(
    tid="KIOSK-BR-043",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-043"
)
_term(
    tid="KIOSK-BR-044",
    mfr="SmartLib Unified Hardware",
    model="SL-Kiosk-Pro-2026",
    protos=["SIP2", "ISO28560"],
    max_len=1024,
    hb=30,
    offline=True,
    crc=True,
    cmds=["09", "11", "17", "23", "29", "35", "37", "63", "65", "93", "97"],
    width=40,
    notes="Institutional self-service lending station node KIOSK-BR-044"
)

def lookup_sip2_terminal(terminal_id: str) -> Optional[Sip2TerminalProfile]:
    """Look up SIP2 terminal hardware configuration profile by terminal ID."""
    return SIP2_TERMINALS.get(terminal_id.strip().upper())


def validate_terminal_command(terminal_id: str, command_code: str) -> bool:
    """Verify whether a specific SIP2 command code is supported by the terminal."""
    profile = lookup_sip2_terminal(terminal_id)
    if not profile:
        return False
    return command_code.strip() in profile.supported_commands
