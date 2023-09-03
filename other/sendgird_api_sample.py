from io import StringIO, BytesIO
import psycopg2
from psycopg2.extras import RealDictCursor
from base64 import b64encode
from csv import DictWriter
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)
from sendgrid import SendGridAPIClient
from zipfile import ZIP_DEFLATED, ZipFile


def main():
    mail_address_list = ["sample_1@example.com", "sample_2@example.com"]
    sendgird_api_key = "samplekeyhogehoge"
    send_mail(sendgird_api_key, mail_address_list)


def send_mail(sendgird_api_key, mail_address_list):
    for mail in mail_address_list:
        try:
            message = create_message(mail)
            sg = SendGridAPIClient(sendgird_api_key)
            response = sg.send(message)
            print(response.status_code)
        except Exception as e:
            print(e)


def create_message(mail_address):
    htmlText = """
    {name}様<br><br>

    メールを送ります。
    """
    name = " hogehoge"
    textData = htmlText.format(name=name)

    message = Mail(
        from_email="no-reply@example.com",
        to_emails=mail_address,
        subject="【TEST】テスト",
        html_content=textData,
    )

    param = {
        "port": "54321",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "dbname": "postgres",
    }

    query = """
    select
        id
        ,name
    from
        hoge
    ;
    """

    columns_csv = ["ID", "名前"]

    with psycopg2.connect(**param) as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        data = cursor.fetchall()

        sio = StringIO()
        writer = DictWriter(
            f=sio,
            fieldnames=columns_csv,
            lineterminator="\n",
        )
        writer.writeheader()
        for i, record in enumerate(data):
            writer.writerow({"ID": record["id"], "名前": record["name"]})
        sss = sio.getvalue()

        # インメモリでzipのバイナリを保持するためにBytesIOを使用
        io = BytesIO()

        # zipファイルを生成
        with ZipFile(io, "w", compression=ZIP_DEFLATED, compresslevel=9) as zf:
            zf.writestr("sample.csv", data=sss)
        obj_bytes = io.getvalue()
        raw = b64encode(obj_bytes).decode()

        attached_file = Attachment(
            FileContent(raw),
            FileName("sample.zip"),
            FileType("application/zip"),
            Disposition("attachment"),
        )

        message.attachment = attached_file

        return message
