import pytest
from sendgird_api_sample import create_message


# モックデータベース接続クラス
class MockDatabaseConnection:
    def __enter__(self):
        return self

    def cursor(self, cursor_factory=None):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def execute(self, query):
        # テスト用のダミーデータを返す
        return

    def fetchall(self):
        # テスト用のダミーデータを返す
        return [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Alice"},
        ]


# テスト用のデータベース接続インスタンスを作成
mock_db_connection = MockDatabaseConnection()


# モックされたSendGridAPIClientクラスを生成
class MockSendGridAPIClient:
    def __init__(self, *args, **kwargs):
        pass

    def send(self, message):
        return MockResponse(status_code=202)


# モックされたレスポンスクラスを生成
class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code


# create_message関数のテスト
def test_create_message(monkeypatch):
    mail_address = "test@example.com"

    # モックしたデータベース接続をインジェクト
    monkeypatch.setattr(
        "sendgird_api_sample.psycopg2.connect", lambda **kwargs: mock_db_connection
    )

    message = create_message(mail_address)
    print(message)
    assert message is not None
    assert message.from_email.email == "no-reply@example.com"
    assert message.subject.subject == "【TEST】テスト"
    assert message.personalizations[0].get()["to"][0]["email"] == mail_address
