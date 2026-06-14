import unittest

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class RouteTests(unittest.TestCase):
    def test_get_inbox_returns_mail_summaries(self) -> None:
        response = client.get("/mails")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            {
                "id": 1,
                "sender": "teacher@example.com",
                "receiver": "student@example.com",
                "subject": "Homework Form",
                "attachment_count": 3,
                "task_count": 3,
            },
            response.json(),
        )

    def test_get_mail_returns_sample_mail(self) -> None:
        response = client.get("/mails/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["subject"], "Homework Form")
        self.assertEqual(response.json()["content"]["type"], "group")
        self.assertEqual(len(response.json()["content"]["children"]), 4)

    def test_get_mail_returns_404_for_missing_mail(self) -> None:
        response = client.get("/mails/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Mail not found.")

    def test_convert_attachment_returns_html_table(self) -> None:
        response = client.post("/attachments/1/convert")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["attachment_id"], 1)
        self.assertEqual(response.json()["file_name"], "sample.csv")
        self.assertIn("<table>", response.json()["html_table"])

    def test_convert_attachment_returns_404_for_missing_attachment(self) -> None:
        response = client.post("/attachments/999/convert")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Attachment not found.")

    def test_validate_mail_returns_validation_result(self) -> None:
        response = client.post("/mails/1/validate")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "valid": True,
                "errors": [],
                "warnings": [],
            },
        )

    def test_validate_mail_returns_404_for_missing_mail(self) -> None:
        response = client.post("/mails/999/validate")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Mail not found.")

    def test_reply_to_mail_creates_reply(self) -> None:
        response = client.post(
            "/mails/1/reply",
            json={"body": "I completed the form."},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sender"], "student@example.com")
        self.assertEqual(response.json()["receiver"], "teacher@example.com")
        self.assertEqual(response.json()["subject"], "Re: Homework Form")
        self.assertEqual(response.json()["body"], "I completed the form.")

    def test_reply_to_mail_returns_404_for_missing_mail(self) -> None:
        response = client.post(
            "/mails/999/reply",
            json={"body": "This should not send."},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Mail not found.")

    def test_update_attachment_stores_html_table(self) -> None:
        html_table = "<table><tbody><tr><td>Updated</td></tr></tbody></table>"

        response = client.post(
            "/attachments/1/update",
            json={"html_table": html_table},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["attachment_id"], 1)
        self.assertEqual(response.json()["html_table"], html_table)

    def test_update_attachment_returns_404_for_missing_attachment(self) -> None:
        response = client.post(
            "/attachments/999/update",
            json={"html_table": "<table></table>"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Attachment not found.")


if __name__ == "__main__":
    unittest.main()
