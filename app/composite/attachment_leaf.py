"""Attachment leaf component."""

from dataclasses import dataclass

from app.composite.mail_component import MailComponent
from app.models.attachment import Attachment


@dataclass
class AttachmentLeaf(MailComponent):
    attachment: Attachment

    def display_name(self) -> str:
        return self.attachment.file_name

    def to_dict(self) -> dict:
        return {
            "type": "attachment",
            "display_name": self.display_name(),
            "attachment_id": self.attachment.id,
            "file_name": self.attachment.file_name,
            "file_type": self.attachment.file_type.value,
        }
