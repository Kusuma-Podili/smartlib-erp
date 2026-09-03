"""
Currency, receipt, and tabular terminal formatting utilities.
"""

import json
from typing import List, Dict, Any, Optional

def format_currency(amount: float, symbol: str = "$") -> str:
    """Format numeric amount as standard currency representation."""
    return f"{symbol}{amount:,.2f}"

def format_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Format tabular records into clean ASCII table."""
    if not headers:
        return ""
    col_widths = [len(h) for h in headers]
    str_rows = []
    for row in rows:
        formatted_row = [str(cell) if cell is not None else "-" for cell in row]
        str_rows.append(formatted_row)
        for idx, cell in enumerate(formatted_row):
            if idx < len(col_widths):
                col_widths[idx] = max(col_widths[idx], len(cell))
            else:
                col_widths.append(len(cell))

    # Header line
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    separator_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    data_lines = [
        " | ".join(row[i].ljust(col_widths[i]) if i < len(row) else "".ljust(col_widths[i]) for i in range(len(headers)))
        for row in str_rows
    ]
    return "\n".join([header_line, separator_line] + data_lines)

def to_pretty_json(data: Any) -> str:
    """Serialize data structure to indented JSON."""
    return json.dumps(data, indent=2, default=str)
