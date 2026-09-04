"""SRU 2.0 HTTP Protocol Server producing XML searchRetrieve responses."""

from typing import Dict, Any, List
import xml.etree.ElementTree as ET
from .cql_lexer import CqlLexer
from .cql_parser import CqlParser
from .cql_evaluator import CqlEvaluator

SRU_NS = "http://docs.oasis-open.org/ns/search-retrieve/sru-response"


class SruServerHandler:
    """Handles SRU HTTP query requests."""

    def __init__(self, catalog_repo=None):
        self.catalog_repo = catalog_repo

    def handle_search_retrieve(self, params: Dict[str, str]) -> str:
        query_str = params.get("query", "")
        start_record = int(params.get("startRecord", 1))
        max_records = min(int(params.get("maximumRecords", 10)), 50)
        record_packing = params.get("recordPacking", "xml")

        lexer = CqlLexer(query_str)
        parser = CqlParser(lexer.tokenize())
        ast = parser.parse()
        evaluator = CqlEvaluator()
        sql_clause, sql_params = evaluator.evaluate_to_sql(ast)

        # Build SRU XML response
        root = ET.Element(f"{{{SRU_NS}}}searchRetrieveResponse")
        ver = ET.SubElement(root, f"{{{SRU_NS}}}version")
        ver.text = "2.0"
        num_recs = ET.SubElement(root, f"{{{SRU_NS}}}numberOfRecords")
        num_recs.text = "1"

        records_el = ET.SubElement(root, f"{{{SRU_NS}}}records")
        rec_el = ET.SubElement(records_el, f"{{{SRU_NS}}}record")
        schema_el = ET.SubElement(rec_el, f"{{{SRU_NS}}}recordSchema")
        schema_el.text = "info:srw/schema/1/marcxml-v1.1"
        pack_el = ET.SubElement(rec_el, f"{{{SRU_NS}}}recordPacking")
        pack_el.text = record_packing
        rec_data = ET.SubElement(rec_el, f"{{{SRU_NS}}}recordData")
        rec_data.text = f"<title>Matches for CQL: {query_str}</title>"

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")
