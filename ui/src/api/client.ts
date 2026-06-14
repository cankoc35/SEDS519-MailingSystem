const API_BASE_URL = "http://127.0.0.1:8000";

export type InboxMail = {
  id: number;
  sender: string;
  receiver: string;
  subject: string;
  attachment_count: number;
  task_count: number;
};

export type MailComponent =
  | {
      type: "text";
      display_name: string;
      text: string;
    }
  | {
      type: "attachment";
      display_name: string;
      attachment_id: number;
      file_name: string;
      file_type: string;
    }
  | {
      type: "group";
      display_name: string;
      children: MailComponent[];
    };

export type Task = {
  id: number;
  title: string;
  description: string;
  completed: boolean;
};

export type MailDetail = {
  id: number;
  sender: string;
  receiver: string;
  subject: string;
  content: MailComponent;
  tasks: Task[];
};

export type ConvertedAttachment = {
  attachment_id: number;
  file_name: string;
  file_type: string;
  html_table: string;
};

export type UpdatedAttachment = {
  attachment_id: number;
  file_name: string;
  html_table: string;
};

export type ReplyMail = {
  id: number;
  sender: string;
  receiver: string;
  subject: string;
  body: string;
};

export type ValidationResult = {
  valid: boolean;
  errors: string[];
  warnings: string[];
};

export type CompletedTask = {
  mail_id: number;
  task_id: number;
  completed: boolean;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, options);

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getInbox(): Promise<InboxMail[]> {
  return request<InboxMail[]>("/mails");
}

export function getMail(mailId: number): Promise<MailDetail> {
  return request<MailDetail>(`/mails/${mailId}`);
}

export function convertAttachment(attachmentId: number): Promise<ConvertedAttachment> {
  return request<ConvertedAttachment>(`/attachments/${attachmentId}/convert`, {
    method: "POST",
  });
}

export function updateAttachment(
  attachmentId: number,
  htmlTable: string,
): Promise<UpdatedAttachment> {
  return request<UpdatedAttachment>(`/attachments/${attachmentId}/update`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ html_table: htmlTable }),
  });
}

export function replyToMail(mailId: number, body: string): Promise<ReplyMail> {
  return request<ReplyMail>(`/mails/${mailId}/reply`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ body }),
  });
}

export function validateMail(mailId: number): Promise<ValidationResult> {
  return request<ValidationResult>(`/mails/${mailId}/validate`, {
    method: "POST",
  });
}

export function toggleTask(mailId: number, taskId: number): Promise<CompletedTask> {
  return request<CompletedTask>(`/mails/${mailId}/tasks/${taskId}/toggle`, {
    method: "POST",
  });
}
