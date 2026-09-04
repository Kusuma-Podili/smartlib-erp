"""Library of Congress MARC Geographic Area Codes (GAC) Reference Directory.

Standard 7-character MARC geographic codes (043 field) mapping nations, states, and regions.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class GeographicAreaCode:
    code: str
    name: str
    region: str
    iso_code: str


MARC_GAC_TABLE: Dict[str, GeographicAreaCode] = {}

def _g(code: str, name: str, region: str, iso: str):
    MARC_GAC_TABLE[code] = GeographicAreaCode(code, name, region, iso)

_g("a-af---", "Afghanistan", "Asia", "AF")
_g("a-ba---", "Bahrain", "Asia", "BH")
_g("a-bd---", "Bangladesh", "Asia", "BD")
_g("a-bt---", "Bhutan", "Asia", "BT")
_g("a-cb---", "Cambodia", "Asia", "KH")
_g("a-cc---", "China", "Asia", "CN")
_g("a-cy---", "Cyprus", "Asia", "CY")
_g("a-ii---", "India", "Asia", "IN")
_g("a-io---", "Indonesia", "Asia", "ID")
_g("a-iq---", "Iraq", "Asia", "IQ")
_g("a-ir---", "Iran", "Asia", "IR")
_g("a-is---", "Israel", "Asia", "IL")
_g("a-ja---", "Japan", "Asia", "JP")
_g("a-jo---", "Jordan", "Asia", "JO")
_g("a-kn---", "Korea (North)", "Asia", "KP")
_g("a-ko---", "Korea (South)", "Asia", "KR")
_g("a-kw---", "Kuwait", "Asia", "KW")
_g("a-kz---", "Kazakhstan", "Asia", "KZ")
_g("a-le---", "Lebanon", "Asia", "LB")
_g("a-my---", "Malaysia", "Asia", "MY")
_g("a-np---", "Nepal", "Asia", "NP")
_g("a-om---", "Oman", "Asia", "OM")
_g("a-pk---", "Pakistan", "Asia", "PK")
_g("a-ph---", "Philippines", "Asia", "PH")
_g("a-qa---", "Qatar", "Asia", "QA")
_g("a-sa---", "Saudi Arabia", "Asia", "SA")
_g("a-si---", "Singapore", "Asia", "SG")
_g("a-sy---", "Syria", "Asia", "SY")
_g("a-th---", "Thailand", "Asia", "TH")
_g("a-ts---", "United Arab Emirates", "Asia", "AE")
_g("a-uz---", "Uzbekistan", "Asia", "UZ")
_g("a-vn---", "Vietnam", "Asia", "VN")
_g("a-ye---", "Yemen", "Asia", "YE")
_g("e-au---", "Austria", "Europe", "AT")
_g("e-be---", "Belgium", "Europe", "BE")
_g("e-bu---", "Bulgaria", "Europe", "BG")
_g("e-ch---", "Switzerland", "Europe", "CH")
_g("e-cs---", "Czech Republic", "Europe", "CZ")
_g("e-dk---", "Denmark", "Europe", "DK")
_g("e-er---", "Estonia", "Europe", "EE")
_g("e-fi---", "Finland", "Europe", "FI")
_g("e-fr---", "France", "Europe", "FR")
_g("e-ge---", "Germany", "Europe", "DE")
_g("e-gr---", "Greece", "Europe", "GR")
_g("e-hu---", "Hungary", "Europe", "HU")
_g("e-ie---", "Ireland", "Europe", "IE")
_g("e-it---", "Italy", "Europe", "IT")
_g("e-lv---", "Latvia", "Europe", "LV")
_g("e-lh---", "Lithuania", "Europe", "LT")
_g("e-lu---", "Luxembourg", "Europe", "LU")
_g("e-nl---", "Netherlands", "Europe", "NL")
_g("e-no---", "Norway", "Europe", "NO")
_g("e-pl---", "Poland", "Europe", "PL")
_g("e-pt---", "Portugal", "Europe", "PT")
_g("e-ro---", "Romania", "Europe", "RO")
_g("e-ru---", "Russia", "Europe", "RU")
_g("e-sp---", "Spain", "Europe", "ES")
_g("e-sw---", "Sweden", "Europe", "SE")
_g("e-uk---", "United Kingdom", "Europe", "GB")
_g("e-ur---", "Ukraine", "Europe", "UA")
_g("f-ae---", "Algeria", "Africa", "DZ")
_g("f-eg---", "Egypt", "Africa", "EG")
_g("f-et---", "Ethiopia", "Africa", "ET")
_g("f-gh---", "Ghana", "Africa", "GH")
_g("f-ke---", "Kenya", "Africa", "KE")
_g("f-mr---", "Morocco", "Africa", "MA")
_g("f-ng---", "Nigeria", "Africa", "NG")
_g("f-sa---", "South Africa", "Africa", "ZA")
_g("f-tz---", "Tanzania", "Africa", "TZ")
_g("f-ug---", "Uganda", "Africa", "UG")
_g("n-us---", "United States", "North America", "US")
_g("n-cn---", "Canada", "North America", "CA")
_g("n-mx---", "Mexico", "North America", "MX")
_g("s-ag---", "Argentina", "South America", "AR")
_g("s-bl---", "Brazil", "South America", "BR")
_g("s-cl---", "Chile", "South America", "CL")
_g("s-ck---", "Colombia", "South America", "CO")
_g("s-pe---", "Peru", "South America", "PE")
_g("s-ve---", "Venezuela", "South America", "VE")
_g("u-at---", "Australia", "Oceania", "AU")
_g("u-nz---", "New Zealand", "Oceania", "NZ")

def lookup_gac(code: str) -> Optional[GeographicAreaCode]:
    return MARC_GAC_TABLE.get(code.strip().lower())
