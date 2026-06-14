from fastapi import APIRouter, HTTPException

from app.controllers.attachment_controller import AttachmentController
from app.controllers.mail_controller import MailController
from app.sample_data import ATTACHMENTS, MAILS
from app.schemas.attachment_schema import AttachmentUpdateRequest
from app.schemas.mail_schema import ReplyRequest


router = APIRouter()
mail_controller = MailController()
attachment_controller = AttachmentController()


@router.get("/mails")
def get_inbox() -> list[dict]:
    return [
        {
            "id": mail.id,
            "sender": mail.sender,
            "receiver": mail.receiver,
            "subject": mail.subject,
            "attachment_count": len(mail.attachments),
            "task_count": len(mail.tasks),
        }
        for mail in MAILS.values()
    ]


@router.get("/mails/{mail_id}")
def get_mail(mail_id: int) -> dict:
    mail = MAILS.get(mail_id)
    if mail is None:
        raise HTTPException(status_code=404, detail="Mail not found.")

    return {
        "id": mail.id,
        "sender": mail.sender,
        "receiver": mail.receiver,
        "subject": mail.subject,
        "content": mail_controller.display_mail(mail),
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
            }
            for task in mail.tasks
        ],
    }


@router.post("/mails/{mail_id}/validate")
def validate_mail(mail_id: int) -> dict:
    mail = MAILS.get(mail_id)
    if mail is None:
        raise HTTPException(status_code=404, detail="Mail not found.")

    result = mail_controller.validate_mail(mail)

    return {
        "valid": result.is_valid(),
        "errors": result.errors,
        "warnings": result.warnings,
    }


@router.post("/mails/{mail_id}/reply")
def reply_to_mail(mail_id: int, request: ReplyRequest) -> dict:
    mail = MAILS.get(mail_id)
    if mail is None:
        raise HTTPException(status_code=404, detail="Mail not found.")

    reply_id = max(MAILS) + 1
    reply = mail_controller.reply_to_mail(
        original_mail=mail,
        reply_body=request.body,
        reply_id=reply_id,
    )
    MAILS[reply.id] = reply

    return {
        "id": reply.id,
        "sender": reply.sender,
        "receiver": reply.receiver,
        "subject": reply.subject,
        "body": reply.body,
    }


@router.post("/mails/{mail_id}/tasks/{task_id}/toggle")
def toggle_task(mail_id: int, task_id: int) -> dict:
    mail = MAILS.get(mail_id)
    if mail is None:
        raise HTTPException(status_code=404, detail="Mail not found.")

    task_completed = mail_controller.toggle_task(mail, task_id)
    if task_completed is None:
        raise HTTPException(status_code=404, detail="Task not found.")

    return {
        "mail_id": mail.id,
        "task_id": task_id,
        "completed": task_completed,
    }


@router.post("/attachments/{attachment_id}/convert")
def convert_attachment(attachment_id: int) -> dict:
    attachment = ATTACHMENTS.get(attachment_id)
    if attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found.")

    html_table = attachment_controller.convert_attachment(attachment)

    return {
        "attachment_id": attachment.id,
        "file_name": attachment.file_name,
        "file_type": attachment.file_type.value,
        "html_table": html_table,
    }


@router.post("/attachments/{attachment_id}/update")
def update_attachment(attachment_id: int, request: AttachmentUpdateRequest) -> dict:
    attachment = ATTACHMENTS.get(attachment_id)
    if attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found.")

    updated_attachment = attachment_controller.update_attachment(
        attachment=attachment,
        html_table=request.html_table,
    )

    return {
        "attachment_id": updated_attachment.id,
        "file_name": updated_attachment.file_name,
        "html_table": updated_attachment.html_table,
    }
