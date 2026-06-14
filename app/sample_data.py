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

empty_body_mail = Mail(
    id=2,
    sender="advisor@example.com",
    receiver="student@example.com",
    subject="Empty Body Validation Demo",
    body="",
)

text_only_mail = Mail(
    id=3,
    sender="department@example.com",
    receiver="student@example.com",
    subject="Text Only Announcement",
    body="The project presentation schedule will be announced next week.",
)

internship_mail = Mail(
    id=4,
    sender="career.office@example.com",
    receiver="student@example.com",
    subject="Internship Application Form",
    body="Please complete the attached application form and reply before Friday.",
    attachments=[excel_attachment],
    tasks=[
        Task(id=4, title="Review application requirements"),
        Task(id=5, title="Fill internship application form"),
        Task(id=6, title="Reply with completed form"),
    ],
)

project_feedback_mail = Mail(
    id=5,
    sender="instructor@example.com",
    receiver="student@example.com",
    subject="Course Project Feedback",
    body="Your design pattern explanations are clear. Please add one concrete user scenario before submission.",
    tasks=[
        Task(id=7, title="Add user scenario to presentation"),
        Task(id=8, title="Review UML before submission"),
    ],
)

attendance_mail = Mail(
    id=6,
    sender="lab.assistant@example.com",
    receiver="student@example.com",
    subject="Lab Attendance Sheet",
    body="Please review the attendance sheet and update missing status values.",
    attachments=[csv_attachment],
    tasks=[
        Task(id=9, title="Check attendance rows"),
        Task(id=10, title="Update missing statuses"),
    ],
)

MAILS: dict[int, Mail] = {
    homework_mail.id: homework_mail,
    empty_body_mail.id: empty_body_mail,
    text_only_mail.id: text_only_mail,
    internship_mail.id: internship_mail,
    project_feedback_mail.id: project_feedback_mail,
    attendance_mail.id: attendance_mail,
}

ATTACHMENTS: dict[int, Attachment] = {
    csv_attachment.id: csv_attachment,
    excel_attachment.id: excel_attachment,
    pdf_attachment.id: pdf_attachment,
}
