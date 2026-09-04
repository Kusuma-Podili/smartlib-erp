"""Vendor Management Service."""

from typing import List, Dict, Optional
from .models import Vendor


class VendorService:
    """Manages vendor registry, terms, and supplier performance."""

    def __init__(self):
        self.vendors: Dict[str, Vendor] = {}

    def create_vendor(self, code: str, name: str, email: str, phone: str = "", discount: float = 0.0) -> Vendor:
        v_id = f"VEND-{len(self.vendors)+1:04d}"
        vendor = Vendor(
            id=v_id,
            code=code,
            name=name,
            contact_person="Sales Representative",
            email=email,
            phone=phone,
            address="Library Supplies St.",
            discount_percentage=discount
        )
        self.vendors[v_id] = vendor
        return vendor

    def get_vendor(self, vendor_id: str) -> Optional[Vendor]:
        return self.vendors.get(vendor_id)

    def list_vendors(self) -> List[Vendor]:
        return list(self.vendors.values())
