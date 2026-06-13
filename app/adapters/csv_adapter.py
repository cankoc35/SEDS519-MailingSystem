"""CSV file adapter."""

import csv
from html import escape

from app.adapters.file_adapter import FileAdapter


class CsvAdapter(FileAdapter):
    def to_html_table(self, file_path: str) -> str:
        with open(file_path, newline="", encoding="utf-8") as csv_file:
            rows = list(csv.reader(csv_file))

        if not rows:
            return "<table></table>"

        header = rows[0]
        body_rows = rows[1:]

        html_parts = ["<table>", "<thead>", "<tr>"]
        html_parts.extend(f"<th>{escape(cell)}</th>" for cell in header)
        html_parts.extend(["</tr>", "</thead>", "<tbody>"])

        for row in body_rows:
            html_parts.append("<tr>")
            html_parts.extend(f"<td>{escape(cell)}</td>" for cell in row)
            html_parts.append("</tr>")

        html_parts.extend(["</tbody>", "</table>"])
        return "".join(html_parts)
