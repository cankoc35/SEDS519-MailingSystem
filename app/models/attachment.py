"""Attachment domain model."""

from dataclasses import dataclass
from enum import Enum


class AttachmentType(str, Enum):
    CSV = "csv"
    EXCEL = "excel"
    PDF = "pdf"


@dataclass
class Attachment:
    id: int
    file_name: str
    file_path: str
    file_type: AttachmentType 