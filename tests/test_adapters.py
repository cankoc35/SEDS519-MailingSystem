import unittest

from app.adapters.csv_adapter import CsvAdapter
from app.adapters.excel_adapter import ExcelAdapter
from app.adapters.file_adapter import FileAdapter
from app.adapters.pdf_adapter import PdfAdapter


class AdapterTests(unittest.TestCase):
    def test_csv_adapter_is_file_adapter(self) -> None:
        adapter = CsvAdapter()

        self.assertIsInstance(adapter, FileAdapter)

    def test_csv_adapter_converts_csv_to_html_table(self) -> None:
        adapter = CsvAdapter()

        html = adapter.to_html_table("samples/attachments/sample.csv")

        self.assertEqual(
            html,
            "<table>"
            "<thead>"
            "<tr><th>Name</th><th>Email</th><th>Status</th></tr>"
            "</thead>"
            "<tbody>"
            "<tr><td>Ada Lovelace</td><td>ada@example.com</td><td>Pending</td></tr>"
            "<tr><td>Grace Hopper</td><td>grace@example.com</td><td>Completed</td></tr>"
            "</tbody>"
            "</table>",
        )

    def test_excel_adapter_is_file_adapter(self) -> None:
        adapter = ExcelAdapter()

        self.assertIsInstance(adapter, FileAdapter)

    def test_excel_adapter_converts_excel_to_html_table(self) -> None:
        adapter = ExcelAdapter()

        html = adapter.to_html_table("samples/attachments/sample.xlsx")

        self.assertEqual(
            html,
            "<table>"
            "<thead>"
            "<tr><th>Name</th><th>Email</th><th>Status</th></tr>"
            "</thead>"
            "<tbody>"
            "<tr><td>Ada Lovelace</td><td>ada@example.com</td><td>Pending</td></tr>"
            "<tr><td>Grace Hopper</td><td>grace@example.com</td><td>Completed</td></tr>"
            "</tbody>"
            "</table>",
        )

    def test_pdf_adapter_is_file_adapter(self) -> None:
        adapter = PdfAdapter()

        self.assertIsInstance(adapter, FileAdapter)

    def test_pdf_adapter_converts_pdf_to_html_table(self) -> None:
        adapter = PdfAdapter()

        html = adapter.to_html_table("samples/attachments/sample.pdf")

        self.assertEqual(
            html,
            "<table>"
            "<thead>"
            "<tr><th>Name</th><th>Email</th><th>Status</th></tr>"
            "</thead>"
            "<tbody>"
            "<tr><td>Ada Lovelace</td><td>ada@example.com</td><td>Pending</td></tr>"
            "<tr><td>Grace Hopper</td><td>grace@example.com</td><td>Completed</td></tr>"
            "</tbody>"
            "</table>",
        )


if __name__ == "__main__":
    unittest.main()
