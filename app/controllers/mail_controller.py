"""Mail actions such as display, reply, and validation."""

from typing import Optional

from app.models.mail import Mail
from app.validation.mail_validator import MailValidator, ValidationResult


class MailController:
    def display_mail(self, mail: Mail) -> dict:
        return mail.to_component().to_dict()

    def validate_mail(self, mail: Mail) -> ValidationResult:
        return MailValidator.validate(mail)

    def reply_to_mail(self, original_mail: Mail, reply_body: str, reply_id: int) -> Mail:
        subject = original_mail.subject
        if not subject.startswith("Re: "):
            subject = f"Re: {subject}"

        return Mail(
            id=reply_id,
            sender=original_mail.receiver,
            receiver=original_mail.sender,
            subject=subject,
            body=reply_body,
            attachments=list(original_mail.attachments),
        )

    def toggle_task(self, mail: Mail, task_id: int) -> Optional[bool]:
        for task in mail.tasks:
            if task.id == task_id:
                task.toggle_completed()
                return task.completed

        return None
