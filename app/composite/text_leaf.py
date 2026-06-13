"""Text leaf component."""

from dataclasses import dataclass

from app.composite.mail_component import MailComponent


@dataclass
class TextLeaf(MailComponent):
    text: str

    def display_name(self) -> str:
        return "Text"

    def to_dict(self) -> dict:
        return {
            "type": "text",
            "display_name": self.display_name(),
            "text": self.text,
        }
