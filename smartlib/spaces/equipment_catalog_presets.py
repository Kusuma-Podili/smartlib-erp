"""Library Technology Lending Catalog, Hardware Presets, and Policies.

Defines loan policies, maintenance inspection protocols, replacement fee schedules,
and accessories checklists for equipment circulating from academic library tech desks.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class EquipmentPreset:
    preset_code: str
    model_name: str
    category: str  # 'laptop', 'camera', 'audio', 'maker', 'calculator', 'projector'
    replacement_cost: Decimal
    max_loan_hours: int
    hourly_overdue_fine: Decimal
    is_in_library_use_only: bool
    included_accessories: List[str] = field(default_factory=list)
    inspection_checklist: List[str] = field(default_factory=list)


EQUIPMENT_PRESETS: Dict[str, EquipmentPreset] = {}


def _equip(code: str, name: str, cat: str, cost: float, hours: int, fine: float,
           in_lib: bool, accs: List[str], checks: List[str]):
    EQUIPMENT_PRESETS[code] = EquipmentPreset(
        preset_code=code,
        model_name=name,
        category=cat,
        replacement_cost=Decimal(str(cost)),
        max_loan_hours=hours,
        hourly_overdue_fine=Decimal(str(fine)),
        is_in_library_use_only=in_lib,
        included_accessories=accs,
        inspection_checklist=checks
    )

_equip(
    code="EQ-MBP-14",
    name="Apple MacBook Pro 14 (M3, 16GB, 512GB)",
    cat="laptop",
    cost=1999.0,
    hours=4,
    fine=10.0,
    in_lib=False,
    accs=['MagSafe Charger 70W', 'USB-C Cable', 'Padded Neoprene Sleeve'],
    checks=['Check for physical screen cracks', 'Verify trackpad click', 'Power cycle and check battery health', 'Wipe disk user profile via MDM']
)
_equip(
    code="EQ-DELL-XPS",
    name="Dell XPS 15 (Core i7, 32GB, 1TB)",
    cat="laptop",
    cost=1799.0,
    hours=4,
    fine=10.0,
    in_lib=False,
    accs=['130W USB-C AC Adapter', 'Power Cord', 'Protective Sleeve'],
    checks=['Screen inspection', 'Keyboard and hinge integrity', 'Re-image Windows 11 Enterprise OS']
)
_equip(
    code="EQ-CANON-R6",
    name="Canon EOS R6 Mark II Mirrorless Camera",
    cat="camera",
    cost=2499.0,
    hours=48,
    fine=15.0,
    in_lib=False,
    accs=['24-105mm F4 L Lens', '2x LP-E6NH Batteries', 'Battery Charger', 'SanDisk Extreme 128GB SDXC', 'Neck Strap', 'Camera Bag'],
    checks=['Check lens glass for scratches', 'Test shutter mechanism and autofocus', 'Format SD card to exFAT', 'Sensor clean inspection']
)
_equip(
    code="EQ-SONY-A7",
    name="Sony Alpha a7 IV Full-Frame Camera",
    cat="camera",
    cost=2498.0,
    hours=48,
    fine=15.0,
    in_lib=False,
    accs=['28-70mm Lens', '2x NP-FZ100 Batteries', 'External Dual Charger', '64GB Tough SD Card', 'Carrying Case'],
    checks=['Lens and sensor inspection', 'EVF electronic viewfinder test', 'Card format']
)
_equip(
    code="EQ-RODE-POD",
    name="Rode RodeCaster Pro II Audio Studio",
    cat="audio",
    cost=699.0,
    hours=24,
    fine=5.0,
    in_lib=True,
    accs=['Power Adapter', 'USB-C to USB-C Cable', 'Headphone Adapter 1/4 inch', '32GB MicroSD'],
    checks=['Fader smoothness inspection', 'Phantom power test on XLR inputs', 'Reset audio mixer firmware settings']
)
_equip(
    code="EQ-SHURE-SM7B",
    name="Shure SM7B Vocal Dynamic Microphone",
    cat="audio",
    cost=399.0,
    hours=24,
    fine=5.0,
    in_lib=True,
    accs=['Foam Windscreen', 'Close-Talk Windscreen', '5/8-inch Thread Adapter', 'XLR 10ft Cable'],
    checks=['Check capsule grille', 'Acoustic signal clarity test', 'Inspect XLR locking pins']
)
_equip(
    code="EQ-TI84-PLUS",
    name="Texas Instruments TI-84 Plus CE Graphing Calculator",
    cat="calculator",
    cost=149.0,
    hours=4,
    fine=2.0,
    in_lib=False,
    accs=['Slide Case', 'Mini-USB Charging Cable'],
    checks=['Keypad responsiveness', 'Screen pixels integrity', 'Memory reset to clear unauthorized programs']
)
_equip(
    code="EQ-EPSON-PROJ",
    name="Epson PowerLite 1781W Wireless Projector",
    cat="projector",
    cost=799.0,
    hours=24,
    fine=10.0,
    in_lib=False,
    accs=['Power Cable', 'HDMI Cable 15ft', 'Remote Control with Batteries', 'Soft Carrying Case'],
    checks=['Test lamp hours remaining', 'Check lens focus ring and keystone', 'Clean air filter intake']
)
_equip(
    code="EQ-VR-QUEST3",
    name="Meta Quest 3 128GB VR Headset",
    cat="maker",
    cost=499.0,
    hours=2,
    fine=5.0,
    in_lib=True,
    accs=['2x Touch Plus Controllers', 'Silicone Facial Interface', 'USB-C Charging Cable and Brick'],
    checks=['Clean lenses with microfiber cloth only', 'Controller battery check', 'Factory reset and sanitize headset strap']
)
_equip(
    code="EQ-PRUSA-MK4",
    name="Original Prusa MK4 3D Printer (Makerspace Desk)",
    cat="maker",
    cost=999.0,
    hours=0,
    fine=0.0,
    in_lib=True,
    accs=['Smooth PEI Steel Sheet', 'Textured PEI Sheet', 'Nozzle Cleaning Needle', 'Hex Key Set'],
    checks=['Nozzle clogs inspection', 'Bed leveling calibration test', 'X/Y/Z axis belt tension check']
)
_equip(
    code="EQ-ACC-001",
    name="Auxiliary Lending Accessory Unit EQ-ACC-001",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-002",
    name="Auxiliary Lending Accessory Unit EQ-ACC-002",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-003",
    name="Auxiliary Lending Accessory Unit EQ-ACC-003",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-004",
    name="Auxiliary Lending Accessory Unit EQ-ACC-004",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-005",
    name="Auxiliary Lending Accessory Unit EQ-ACC-005",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-006",
    name="Auxiliary Lending Accessory Unit EQ-ACC-006",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-007",
    name="Auxiliary Lending Accessory Unit EQ-ACC-007",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-008",
    name="Auxiliary Lending Accessory Unit EQ-ACC-008",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-009",
    name="Auxiliary Lending Accessory Unit EQ-ACC-009",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-010",
    name="Auxiliary Lending Accessory Unit EQ-ACC-010",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-011",
    name="Auxiliary Lending Accessory Unit EQ-ACC-011",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-012",
    name="Auxiliary Lending Accessory Unit EQ-ACC-012",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-013",
    name="Auxiliary Lending Accessory Unit EQ-ACC-013",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-014",
    name="Auxiliary Lending Accessory Unit EQ-ACC-014",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-015",
    name="Auxiliary Lending Accessory Unit EQ-ACC-015",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-016",
    name="Auxiliary Lending Accessory Unit EQ-ACC-016",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-017",
    name="Auxiliary Lending Accessory Unit EQ-ACC-017",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-018",
    name="Auxiliary Lending Accessory Unit EQ-ACC-018",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-019",
    name="Auxiliary Lending Accessory Unit EQ-ACC-019",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-020",
    name="Auxiliary Lending Accessory Unit EQ-ACC-020",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-021",
    name="Auxiliary Lending Accessory Unit EQ-ACC-021",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-022",
    name="Auxiliary Lending Accessory Unit EQ-ACC-022",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-023",
    name="Auxiliary Lending Accessory Unit EQ-ACC-023",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-024",
    name="Auxiliary Lending Accessory Unit EQ-ACC-024",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-025",
    name="Auxiliary Lending Accessory Unit EQ-ACC-025",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-026",
    name="Auxiliary Lending Accessory Unit EQ-ACC-026",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-027",
    name="Auxiliary Lending Accessory Unit EQ-ACC-027",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-028",
    name="Auxiliary Lending Accessory Unit EQ-ACC-028",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-029",
    name="Auxiliary Lending Accessory Unit EQ-ACC-029",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-030",
    name="Auxiliary Lending Accessory Unit EQ-ACC-030",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-031",
    name="Auxiliary Lending Accessory Unit EQ-ACC-031",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-032",
    name="Auxiliary Lending Accessory Unit EQ-ACC-032",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-033",
    name="Auxiliary Lending Accessory Unit EQ-ACC-033",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-034",
    name="Auxiliary Lending Accessory Unit EQ-ACC-034",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-035",
    name="Auxiliary Lending Accessory Unit EQ-ACC-035",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-036",
    name="Auxiliary Lending Accessory Unit EQ-ACC-036",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-037",
    name="Auxiliary Lending Accessory Unit EQ-ACC-037",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-038",
    name="Auxiliary Lending Accessory Unit EQ-ACC-038",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-039",
    name="Auxiliary Lending Accessory Unit EQ-ACC-039",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-040",
    name="Auxiliary Lending Accessory Unit EQ-ACC-040",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-041",
    name="Auxiliary Lending Accessory Unit EQ-ACC-041",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-042",
    name="Auxiliary Lending Accessory Unit EQ-ACC-042",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-043",
    name="Auxiliary Lending Accessory Unit EQ-ACC-043",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)
_equip(
    code="EQ-ACC-044",
    name="Auxiliary Lending Accessory Unit EQ-ACC-044",
    cat="audio",
    cost=75.00,
    hours=8,
    fine=1.50,
    in_lib=False,
    accs=["Protective Carrying Pouch", "Connection Cable"],
    checks=["Visual check for physical damage", "Connectivity and cable integrity test"]
)

def lookup_equipment_preset(preset_code: str) -> Optional[EquipmentPreset]:
    """Retrieve equipment preset specifications by code."""
    return EQUIPMENT_PRESETS.get(preset_code.strip().upper())


def get_presets_by_category(category: str) -> List[EquipmentPreset]:
    """Retrieve all equipment items belonging to a specified equipment category."""
    clean = category.strip().lower()
    return [p for p in EQUIPMENT_PRESETS.values() if p.category.lower() == clean]
