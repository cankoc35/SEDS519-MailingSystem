"""Composite mail component."""

from dataclasses import dataclass, field

from app.composite.mail_component import MailComponent


@dataclass
class MailComposite(MailComponent):
    name: str
    children: list[MailComponent] = field(default_factory=list)

    def add(self, component: MailComponent) -> None:
        self.children.append(component)

    def remove(self, component: MailComponent) -> None:
        self.children.remove(component)

    def display_name(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {
            "type": "group",
            "display_name": self.display_name(),
            "children": [child.to_dict() for child in self.children],
        }
