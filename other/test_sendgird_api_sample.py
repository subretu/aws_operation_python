import pytest
import sendgird_api_sample


class MockDatabaseConnection:
    def __enter__(self):
        return self

    def cursor(self, cursor_factory=None):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def execute(self, query):
        return

    def fetchall(self):
        return [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Alice"},
        ]


mock_db_connection = MockDatabaseConnection()


def test_send_mail(mocker):
    mock_create_message = mocker.patch("sendgird_api_sample.create_message")
    mock_create_message.return_value = "Mocked Mail Object"

    mock_sendgrid_api_client = mocker.patch("sendgird_api_sample.SendGridAPIClient")
    mock_sendgrid_instance = mock_sendgrid_api_client.return_value
    mock_sendgrid_instance.send.return_value = "Success"

    sendgrid_api_key = "mock_sendgrid_api_key"
    mail_address_list = ["sample_1@example.com", "sample_2@example.com"]

    sendgird_api_sample.send_mail(sendgrid_api_key, mail_address_list)

    mock_create_message.assert_called()
    mock_sendgrid_instance.send.assert_called()


def test_create_message(monkeypatch):
    mail_address = "test@example.com"

    monkeypatch.setattr(
        "sendgird_api_sample.psycopg2.connect", lambda **kwargs: mock_db_connection
    )

    message = sendgird_api_sample.create_message(mail_address)
    print(message)
    assert message is not None
    assert message.from_email.email == "no-reply@example.com"
    assert message.subject.subject == "【TEST】テスト"
    assert message.personalizations[0].get()["to"][0]["email"] == mail_address
