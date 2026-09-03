"""Data export formatters (CSV, JSON, ASCII table)."""
import csv
import io
import json
from typing import List, Dict, Any

class ReportExporter:
    @staticmethod
    def to_csv(headers: List[str], data_rows: List[List[Any]]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        for r in data_rows:
            writer.writerow(r)
        return output.getvalue()

    @staticmethod
    def to_json(records: List[Dict[str, Any]]) -> str:
        return json.dumps(records, indent=2, default=str)
