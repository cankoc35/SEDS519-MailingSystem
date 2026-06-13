"""Mail validity checks."""

from dataclasses import dataclass, field

from app.models.mail import Mail


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def is_valid(self) -> bool:
        return len(self.errors) == 0


class MailValidator:
    @staticmethod
    def validate(mail: Mail) -> ValidationResult:
        result = ValidationResult()

        if not mail.has_body():
            result.errors.append("Mail body cannot be empty.")

        if not mail.has_attachments():
            result.warnings.append("Mail has no attachments.")

        return result

    @staticmethod
    def is_valid(mail: Mail) -> bool:
        return MailValidator.validate(mail).is_valid()
