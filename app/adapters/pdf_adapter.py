"""PDF file adapter."""

from html import escape
from typing import Optional

import pdfplumber

from app.adapters.file_adapter import FileAdapter


class PdfAdapter(FileAdapter):
    def to_html_table(self, file_path: str) -> str:
        table = self._extract_first_table(file_path)

        if not table:
            return "<table></table>"

        header = table[0]
        body_rows = table[1:]

        html_parts = ["<table>", "<thead>", "<tr>"]
        html_parts.extend(f"<th>{self._format_cell(cell)}</th>" for cell in header)
        html_parts.extend(["</tr>", "</thead>", "<tbody>"])

        for row in body_rows:
            html_parts.append("<tr>")
            html_parts.extend(f"<td>{self._format_cell(cell)}</td>" for cell in row)
            html_parts.append("</tr>")

        html_parts.extend(["</tbody>", "</table>"])
        return "".join(html_parts)

    def _extract_first_table(self, file_path: str) -> list[list[Optional[str]]]:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    return table
        return []

    def _format_cell(self, cell: object) -> str:
        if cell is None:
            return ""
        return escape(str(cell).strip())
