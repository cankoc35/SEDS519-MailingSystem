"""Attachment actions such as display, update, and conversion."""

from app.adapters.adapter_factory import AdapterFactory
from app.models.attachment import Attachment


class AttachmentController:
    def convert_attachment(self, attachment: Attachment) -> str:
        if attachment.html_table:
            return attachment.html_table

        adapter = AdapterFactory.get_adapter(attachment.file_type)
        return adapter.to_html_table(attachment.file_path)

    def update_attachment(self, attachment: Attachment, html_table: str) -> Attachment:
        attachment.html_table = html_table
        return attachment
