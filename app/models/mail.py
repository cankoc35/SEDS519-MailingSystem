"""Mail domain model."""

from dataclasses import dataclass, field

from app.composite.attachment_leaf import AttachmentLeaf
from app.composite.mail_composite import MailComposite
from app.composite.text_leaf import TextLeaf
from app.models.attachment import Attachment
from app.models.task import Task


@dataclass
class Mail:
    id: int
    sender: str
    receiver: str
    subject: str
    body: str
    attachments: list[Attachment] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def has_body(self) -> bool:
        return bool(self.body.strip())

    def has_attachments(self) -> bool:
        return len(self.attachments) > 0

    def add_attachment(self, attachment: Attachment) -> None:
        self.attachments.append(attachment)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def to_component(self) -> MailComposite:
        mail_component = MailComposite(self.subject)

        if self.has_body():
            mail_component.add(TextLeaf(self.body))

        for attachment in self.attachments:
            mail_component.add(AttachmentLeaf(attachment))

        return mail_component
