import unittest

from app.controllers.attachment_controller import AttachmentController
from app.controllers.mail_controller import MailController
from app.models.attachment import Attachment, AttachmentType
from app.models.mail import Mail


EXPECTED_TABLE = (
    "<table>"
    "<thead>"
    "<tr><th>Name</th><th>Email</th><th>Status</th></tr>"
    "</thead>"
    "<tbody>"
    "<tr><td>Ada Lovelace</td><td>ada@example.com</td><td>Pending</td></tr>"
    "<tr><td>Grace Hopper</td><td>grace@example.com</td><td>Completed</td></tr>"
    "</tbody>"
    "</table>"
)


class ControllerTests(unittest.TestCase):
    def test_attachment_controller_converts_csv_attachment(self) -> None:
        controller = AttachmentController()
        attachment = Attachment(
            id=1,
            file_name="sample.csv",
            file_path="samples/attachments/sample.csv",
            file_type=AttachmentType.CSV,
        )

        html = controller.convert_attachment(attachment)

        self.assertEqual(html, EXPECTED_TABLE)

    def test_attachment_controller_converts_excel_attachment(self) -> None:
        controller = AttachmentController()
        attachment = Attachment(
            id=2,
            file_name="sample.xlsx",
            file_path="samples/attachments/sample.xlsx",
            file_type=AttachmentType.EXCEL,
        )

        html = controller.convert_attachment(attachment)

        self.assertEqual(html, EXPECTED_TABLE)

    def test_attachment_controller_converts_pdf_attachment(self) -> None:
        controller = AttachmentController()
        attachment = Attachment(
            id=3,
            file_name="sample.pdf",
            file_path="samples/attachments/sample.pdf",
            file_type=AttachmentType.PDF,
        )

        html = controller.convert_attachment(attachment)

        self.assertEqual(html, EXPECTED_TABLE)

    def test_attachment_controller_updates_attachment_html_table(self) -> None:
        controller = AttachmentController()
        attachment = Attachment(
            id=4,
            file_name="sample.csv",
            file_path="samples/attachments/sample.csv",
            file_type=AttachmentType.CSV,
        )
        updated_table = (
            "<table><tbody>"
            "<tr><td>Ada Lovelace</td><td>Updated</td></tr>"
            "</tbody></table>"
        )

        updated_attachment = controller.update_attachment(attachment, updated_table)

        self.assertIs(updated_attachment, attachment)
        self.assertEqual(attachment.html_table, updated_table)

    def test_attachment_controller_convert_returns_updated_html_when_available(self) -> None:
        controller = AttachmentController()
        updated_table = (
            "<table><tbody>"
            "<tr><td>Edited value</td></tr>"
            "</tbody></table>"
        )
        attachment = Attachment(
            id=5,
            file_name="sample.csv",
            file_path="samples/attachments/sample.csv",
            file_type=AttachmentType.CSV,
            html_table=updated_table,
        )

        html = controller.convert_attachment(attachment)

        self.assertEqual(html, updated_table)

    def test_mail_controller_displays_mail_as_composite_dict(self) -> None:
        controller = MailController()
        attachment = Attachment(
            id=1,
            file_name="sample.csv",
            file_path="samples/attachments/sample.csv",
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

        display_data = controller.display_mail(mail)

        self.assertEqual(
            display_data,
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
                        "display_name": "sample.csv",
                        "attachment_id": 1,
                        "file_name": "sample.csv",
                        "file_type": "csv",
                    },
                ],
            },
        )

    def test_mail_controller_validates_mail(self) -> None:
        controller = MailController()
        mail = Mail(
            id=2,
            sender="teacher@example.com",
            receiver="student@example.com",
            subject="Question",
            body="Can I submit tomorrow?",
        )

        result = controller.validate_mail(mail)

        self.assertTrue(result.is_valid())
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, ["Mail has no attachments."])

    def test_mail_controller_replies_to_mail(self) -> None:
        controller = MailController()
        attachment = Attachment(
            id=1,
            file_name="sample.csv",
            file_path="samples/attachments/sample.csv",
            file_type=AttachmentType.CSV,
            html_table="<table><tbody><tr><td>Edited</td></tr></tbody></table>",
        )
        original_mail = Mail(
            id=3,
            sender="teacher@example.com",
            receiver="student@example.com",
            subject="Homework",
            body="Please fill the attachment.",
            attachments=[attachment],
        )

        reply = controller.reply_to_mail(
            original_mail=original_mail,
            reply_body="I completed the homework.",
            reply_id=4,
        )

        self.assertEqual(reply.id, 4)
        self.assertEqual(reply.sender, "student@example.com")
        self.assertEqual(reply.receiver, "teacher@example.com")
        self.assertEqual(reply.subject, "Re: Homework")
        self.assertEqual(reply.body, "I completed the homework.")
        self.assertEqual(reply.attachments, [attachment])
        self.assertEqual(reply.tasks, [])

    def test_mail_controller_does_not_duplicate_reply_prefix(self) -> None:
        controller = MailController()
        original_mail = Mail(
            id=5,
            sender="teacher@example.com",
            receiver="student@example.com",
            subject="Re: Homework",
            body="Please review again.",
        )

        reply = controller.reply_to_mail(
            original_mail=original_mail,
            reply_body="Thanks.",
            reply_id=6,
        )

        self.assertEqual(reply.subject, "Re: Homework")


if __name__ == "__main__":
    unittest.main()
