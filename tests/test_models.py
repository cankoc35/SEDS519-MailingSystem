import unittest

from app.models.attachment import Attachment, AttachmentType
from app.models.mail import Mail
from app.models.task import Task
from app.validation.mail_validator import MailValidator


class ModelTests(unittest.TestCase):
    def test_mail_with_body_and_attachment_is_valid(self) -> None:
        attachment = Attachment(
            id=1,
            file_name="homework.csv",
            file_path="samples/attachments/homework.csv",
            file_type=AttachmentType.CSV,
        )
        mail = Mail(
            id=1,
            sender="teacher@example.com",
            receiver="student@example.com",
            subject="Homework",
            body="Please fill the attachment.",
            attachments=[attachment],
        )

        self.assertTrue(MailValidator.is_valid(mail))
        result = MailValidator.validate(mail)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])

    def test_mail_without_body_is_invalid_and_missing_attachment_is_warning(self) -> None:
        mail = Mail(
            id=2,
            sender="teacher@example.com",
            receiver="student@example.com",
            subject="Incomplete Mail",
            body=" ",
        )

        result = MailValidator.validate(mail)

        self.assertFalse(result.is_valid())
        self.assertEqual(result.errors, ["Mail body cannot be empty."])
        self.assertEqual(result.warnings, ["Mail has no attachments."])

    def test_mail_without_attachments_can_still_be_valid(self) -> None:
        mail = Mail(
            id=3,
            sender="teacher@example.com",
            receiver="student@example.com",
            subject="No Attachment",
            body="This mail has text only.",
        )

        result = MailValidator.validate(mail)

        self.assertTrue(result.is_valid())
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, ["Mail has no attachments."])

    def test_mail_can_collect_attachments_and_tasks(self) -> None:
        mail = Mail(
            id=4,
            sender="teacher@example.com",
            receiver="student@example.com",
            subject="Homework",
            body="Please review the task and attachment.",
        )
        attachment = Attachment(
            id=1,
            file_name="homework.csv",
            file_path="samples/attachments/homework.csv",
            file_type=AttachmentType.CSV,
        )
        task = Task(id=1, title="Fill the attachment")

        mail.add_attachment(attachment)
        mail.add_task(task)

        self.assertEqual(mail.attachments, [attachment])
        self.assertEqual(mail.tasks, [task])

    def test_mail_can_be_represented_as_composite(self) -> None:
        attachment = Attachment(
            id=1,
            file_name="homework.csv",
            file_path="samples/attachments/homework.csv",
            file_type=AttachmentType.CSV,
        )
        mail = Mail(
            id=5,
            sender="teacher@example.com",
            receiver="student@example.com",
            subject="Homework",
            body="Please fill the attachment.",
            attachments=[attachment],
        )

        component = mail.to_component()

        self.assertEqual(
            component.to_dict(),
            {
                "type": "group",
                "display_name": "Homework",
                "children": [
                    {
                        "type": "text",
                        "display_name": "Text",
                        "text": "Please fill the attachment.",
                    },
                    {
                        "type": "attachment",
                        "display_name": "homework.csv",
                        "attachment_id": 1,
                        "file_name": "homework.csv",
                        "file_type": "csv",
                    },
                ],
            },
        )

    def test_task_can_be_marked_completed(self) -> None:
        task = Task(id=1, title="Reply to mail")

        task.mark_completed()

        self.assertTrue(task.completed)


if __name__ == "__main__":
    unittest.main()
