"""Factory for selecting file adapters."""

from app.adapters.csv_adapter import CsvAdapter
from app.adapters.excel_adapter import ExcelAdapter
from app.adapters.file_adapter import FileAdapter
from app.adapters.pdf_adapter import PdfAdapter
from app.models.attachment import AttachmentType


class AdapterFactory:
    @staticmethod
    def get_adapter(file_type: AttachmentType) -> FileAdapter:
        adapters: dict[AttachmentType, FileAdapter] = {
            AttachmentType.CSV: CsvAdapter(),
            AttachmentType.EXCEL: ExcelAdapter(),
            AttachmentType.PDF: PdfAdapter(),
        }

        return adapters[file_type]
