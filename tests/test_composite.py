import unittest

from app.composite.attachment_leaf import AttachmentLeaf
from app.composite.mail_composite import MailComposite
from app.composite.mail_component import MailComponent
from app.composite.text_leaf import TextLeaf
from app.models.attachment import Attachment, AttachmentType


class CompositeTests(unittest.TestCase):
    def test_text_leaf_is_mail_component(self) -> None:
        text = TextLeaf("Please fill the attachment.")

        self.assertIsInstance(text, MailComponent)
        self.assertEqual(text.display_name(), "Text")
        self.assertEqual(
            text.to_dict(),
            {
                "type": "text",
                "display_name": "Text",
                "text": "Please fill the attachment.",
            },
        )

    def test_attachment_leaf_is_mail_component(self) -> None:
        attachment = Attachment(
            id=1,
            file_name="homework.csv",
            file_path="samples/attachments/homework.csv",
            file_type=AttachmentType.CSV,
        )
        leaf = AttachmentLeaf(attachment)

        self.assertIsInstance(leaf, MailComponent)
        self.assertEqual(leaf.display_name(), "homework.csv")
        self.assertEqual(
            leaf.to_dict(),
            {
                "type": "attachment",
                "display_name": "homework.csv",
                "attachment_id": 1,
                "file_name": "homework.csv",
                "file_type": "csv",
            },
        )

    def test_mail_composite_groups_components(self) -> None:
        attachment = Attachment(
            id=1,
            file_name="homework.csv",
            file_path="samples/attachments/homework.csv",
            file_type=AttachmentType.CSV,
        )
        mail_group = MailComposite("Homework Mail")

        mail_group.add(TextLeaf("Please fill the attachment."))
        mail_group.add(AttachmentLeaf(attachment))

        self.assertIsInstance(mail_group, MailComponent)
        self.assertEqual(mail_group.display_name(), "Homework Mail")
        self.assertEqual(
            mail_group.to_dict(),
            {
                "type": "group",
                "display_name": "Homework Mail",
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


if __name__ == "__main__":
    unittest.main()
