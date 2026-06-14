"""Attachment API schemas."""

from pydantic import BaseModel


class AttachmentUpdateRequest(BaseModel):
    html_table: str
