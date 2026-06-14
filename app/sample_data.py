"""In-memory sample data for the homework prototype."""

from app.models.attachment import Attachment, AttachmentType
from app.models.mail import Mail
from app.models.task import Task


csv_attachment = Attachment(
    id=1,
    file_name="sample.csv",
    file_path="samples/attachments/sample.csv",
    file_type=AttachmentType.CSV,
)

excel_attachment = Attachment(
    id=2,
    file_name="sample.xlsx",
    file_path="samples/attachments/sample.xlsx",
    file_type=AttachmentType.EXCEL,
)

pdf_attachment = Attachment(
    id=3,
    file_name="sample.pdf",
    file_path="samples/attachments/sample.pdf",
    file_type=AttachmentType.PDF,
)

homework_mail = Mail(
    id=1,
    sender="teacher@example.com",
    receiver="student@example.com",
    subject="Homework Form",
    body="Please review the instructions and fill the attached form.",
    attachments=[csv_attachment, excel_attachment, pdf_attachment],
    tasks=[
        Task(id=1, title="Review instructions"),
        Task(id=2, title="Fill the attachment"),
        Task(id=3, title="Reply to the mail"),
    ],
)

MAILS: dict[int, Mail] = {
    homework_mail.id: homework_mail,
}

ATTACHMENTS: dict[int, Attachment] = {
    csv_attachment.id: csv_attachment,
    excel_attachment.id: excel_attachment,
    pdf_attachment.id: pdf_attachment,
}
