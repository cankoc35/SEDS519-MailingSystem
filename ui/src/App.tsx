import { useEffect, useMemo, useRef, useState } from "react";

import {
  convertAttachment,
  getInbox,
  getMail,
  replyToMail,
  updateAttachment,
  validateMail,
  toggleTask,
  type ConvertedAttachment,
  type InboxMail,
  type MailComponent,
  type MailDetail,
  type ValidationResult,
} from "./api/client";

type AttachmentNode = Extract<MailComponent, { type: "attachment" }>;

function collectAttachments(component: MailComponent): AttachmentNode[] {
  if (component.type === "attachment") {
    return [component];
  }

  if (component.type === "group") {
    return component.children.flatMap(collectAttachments);
  }

  return [];
}

function collectText(component: MailComponent): string[] {
  if (component.type === "text") {
    return [component.text];
  }

  if (component.type === "group") {
    return component.children.flatMap(collectText);
  }

  return [];
}

export default function App() {
  const [inbox, setInbox] = useState<InboxMail[]>([]);
  const [selectedMail, setSelectedMail] = useState<MailDetail | null>(null);
  const [converted, setConverted] = useState<ConvertedAttachment | null>(null);
  const [loadingAttachmentId, setLoadingAttachmentId] = useState<number | null>(null);
  const [updatingAttachment, setUpdatingAttachment] = useState(false);
  const [updateMessage, setUpdateMessage] = useState<string | null>(null);
  const [replyBody, setReplyBody] = useState("");
  const [sendingReply, setSendingReply] = useState(false);
  const [replyMessage, setReplyMessage] = useState<string | null>(null);
  const [validatingMail, setValidatingMail] = useState(false);
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const [completingTaskId, setCompletingTaskId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const tableEditorRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    getInbox()
      .then((mails) => {
        setInbox(mails);
        if (mails.length > 0) {
          return getMail(mails[0].id);
        }
        return null;
      })
      .then((mail) => {
        if (mail) {
          setSelectedMail(mail);
        }
      })
      .catch(() => setError("Could not load inbox. Make sure the API is running."));
  }, []);

  const textBlocks = useMemo(
    () => (selectedMail ? collectText(selectedMail.content) : []),
    [selectedMail],
  );
  const attachments = useMemo(
    () => (selectedMail ? collectAttachments(selectedMail.content) : []),
    [selectedMail],
  );

  async function openMail(mailId: number) {
    setError(null);
    setConverted(null);
    setReplyBody("");
    setReplyMessage(null);
    setValidationResult(null);

    try {
      setSelectedMail(await getMail(mailId));
    } catch {
      setError("Could not open mail. Inbox was refreshed.");
      setConverted(null);
      setReplyBody("");
      setReplyMessage(null);

      try {
        const refreshedInbox = await getInbox();
        setInbox(refreshedInbox);

        if (refreshedInbox.length > 0) {
          setSelectedMail(await getMail(refreshedInbox[0].id));
        } else {
          setSelectedMail(null);
        }
      } catch {
        setInbox([]);
        setSelectedMail(null);
      }
    }
  }

  async function handleConvert(attachmentId: number) {
    setError(null);
    setUpdateMessage(null);
    setLoadingAttachmentId(attachmentId);

    try {
      setConverted(await convertAttachment(attachmentId));
    } catch {
      setError("Could not convert attachment.");
    } finally {
      setLoadingAttachmentId(null);
    }
  }

  async function handleUpdate() {
    if (!converted || !tableEditorRef.current) {
      return;
    }

    setError(null);
    setUpdateMessage(null);
    setUpdatingAttachment(true);

    try {
      const updated = await updateAttachment(
        converted.attachment_id,
        tableEditorRef.current.innerHTML,
      );
      setConverted({
        attachment_id: updated.attachment_id,
        file_name: updated.file_name,
        file_type: converted.file_type,
        html_table: updated.html_table,
      });
      setUpdateMessage("Attachment updated.");
    } catch {
      setError("Could not update attachment.");
    } finally {
      setUpdatingAttachment(false);
    }
  }

  async function handleReply() {
    if (!selectedMail || !replyBody.trim()) {
      return;
    }

    setError(null);
    setReplyMessage(null);
    setSendingReply(true);

    try {
      const reply = await replyToMail(selectedMail.id, replyBody.trim());
      const [updatedInbox, replyMail] = await Promise.all([getInbox(), getMail(reply.id)]);
      setInbox(updatedInbox);
      setSelectedMail(replyMail);
      setReplyMessage(`Reply created: ${reply.subject}`);
      setReplyBody("");
    } catch {
      setError("Could not send reply.");
    } finally {
      setSendingReply(false);
    }
  }

  async function handleValidateMail() {
    if (!selectedMail) {
      return;
    }

    setError(null);
    setValidationResult(null);
    setValidatingMail(true);

    try {
      setValidationResult(await validateMail(selectedMail.id));
    } catch {
      setError("Could not validate mail.");
    } finally {
      setValidatingMail(false);
    }
  }

  async function handleToggleTask(taskId: number) {
    if (!selectedMail) {
      return;
    }

    setError(null);
    setCompletingTaskId(taskId);

    try {
      await toggleTask(selectedMail.id, taskId);
      setSelectedMail(await getMail(selectedMail.id));
      setInbox(await getInbox());
    } catch {
      setError("Could not complete task.");
    } finally {
      setCompletingTaskId(null);
    }
  }

  return (
    <main className="app-shell">
      <aside className="inbox">
        <h1>Inbox</h1>
        <div className="mail-list">
          {inbox.map((mail) => (
            <button
              className={selectedMail?.id === mail.id ? "active" : ""}
              key={mail.id}
              onClick={() => void openMail(mail.id)}
              type="button"
            >
              <span className="mail-subject">{mail.subject}</span>
              <span className="mail-meta">
                {mail.sender} | {mail.attachment_count} attachments | {mail.task_count} tasks
              </span>
            </button>
          ))}
        </div>
      </aside>

      <section className="mail-view">
        {error && <p className="error">{error}</p>}

        {!selectedMail && !error && <p className="empty-state">No mail selected.</p>}

        {selectedMail && (
          <>
            <header className="mail-header">
              <div className="mail-title-row">
                <h2>{selectedMail.subject}</h2>
                <button
                  className="secondary-button"
                  disabled={validatingMail}
                  onClick={() => void handleValidateMail()}
                  type="button"
                >
                  {validatingMail ? "Validating" : "Validate Mail"}
                </button>
              </div>
              <dl>
                <dt>From</dt>
                <dd>{selectedMail.sender}</dd>
                <dt>To</dt>
                <dd>{selectedMail.receiver}</dd>
              </dl>
              {validationResult && (
                <div className={validationResult.valid ? "validation valid" : "validation invalid"}>
                  <strong>{validationResult.valid ? "Mail is valid." : "Mail is not valid."}</strong>
                  {validationResult.errors.length > 0 && (
                    <ul>
                      {validationResult.errors.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  )}
                  {validationResult.warnings.length > 0 && (
                    <ul>
                      {validationResult.warnings.map((item) => (
                        <li key={item}>Warning: {item}</li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </header>

            <div className="mail-content">
              <section className="section">
                <h3>Message</h3>
                {textBlocks.map((text, index) => (
                  <p className="body-text" key={`${selectedMail.id}-text-${index}`}>
                    {text}
                  </p>
                ))}
              </section>

              <section className="section reply-section">
                <h3>Reply</h3>
                <textarea
                  onChange={(event) => setReplyBody(event.target.value)}
                  placeholder="Write a reply..."
                  value={replyBody}
                />
                <div className="reply-actions">
                  <button
                    className="send-button"
                    disabled={sendingReply || !replyBody.trim()}
                    onClick={() => void handleReply()}
                    type="button"
                  >
                    {sendingReply ? "Sending" : "Send Reply"}
                  </button>
                  {replyMessage && <span className="success inline-success">{replyMessage}</span>}
                </div>
              </section>

              {selectedMail.tasks.length > 0 && (
                <section className="section tasks-section">
                  <h3>Tasks</h3>
                  <div className="task-list">
                    {selectedMail.tasks.map((task) => (
                      <button
                        className={task.completed ? "task-item completed" : "task-item"}
                        disabled={completingTaskId === task.id}
                        key={task.id}
                        onClick={() => void handleToggleTask(task.id)}
                        type="button"
                      >
                        <span className={task.completed ? "task-status completed" : "task-status"} />
                        <div>
                          <div className="task-title">{task.title}</div>
                          {task.description && (
                            <div className="task-description">{task.description}</div>
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                </section>
              )}

              <section className="section">
                <h3>Attachments</h3>
                <div className="attachment-list">
                  {attachments.map((attachment) => (
                    <div className="attachment-item" key={attachment.attachment_id}>
                      <div className="attachment-row">
                        <div>
                          <div className="file-name">{attachment.file_name}</div>
                          <div className="file-type">{attachment.file_type}</div>
                        </div>
                        <button
                          className="convert-button"
                          disabled={loadingAttachmentId === attachment.attachment_id}
                          onClick={() => void handleConvert(attachment.attachment_id)}
                          type="button"
                        >
                          {loadingAttachmentId === attachment.attachment_id ? "Converting" : "Convert"}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {converted && (
                <section className="section table-preview">
                  <div className="table-preview-header">
                    <div>
                      <h3>{converted.file_name}</h3>
                      <p>Edit cells directly, then update the attachment.</p>
                    </div>
                    <button
                      className="update-button"
                      disabled={updatingAttachment}
                      onClick={() => void handleUpdate()}
                      type="button"
                    >
                      {updatingAttachment ? "Updating" : "Update Attachment"}
                    </button>
                  </div>
                  {updateMessage && <p className="success">{updateMessage}</p>}
                  <div
                    className="editable-table"
                    contentEditable
                    dangerouslySetInnerHTML={{ __html: converted.html_table }}
                    ref={tableEditorRef}
                    suppressContentEditableWarning
                  />
                </section>
              )}
            </div>
          </>
        )}
      </section>
    </main>
  );
}
