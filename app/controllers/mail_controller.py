"""Mail actions such as display, reply, and validation."""

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
        )
