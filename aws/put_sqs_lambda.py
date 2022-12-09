from dataclasses import asdict, dataclass
import psycopg2
from psycopg2.extras import RealDictCursor
import boto3
import json


@dataclass(frozen=True)
class SampleData:
    opsdate: str
    value_data1: int
    value_data2: int
    text_data: str


def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        user="hoge",
        password="hogehoge",
        database="hogehogehoge",
        port=5432,
    )

    return connection


def lambda_handler(event, context):
    main(event, context)


def main(event, context):
    # SQSのメッセージを取得(LambdaのトリガーがSQSを想定)
    key = event["Records"][0]["body"]
    data = create_data(key)
    put_sqs(data)


def create_data(key):
    conn = get_db_connection()

    sql = f"""
    select
        opsdate::text
        ,value_data1
        ,value_data2
        ,text_data
    from
        sample
    where
        key = {key}
    ;
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        data = [SampleData(**x) for x in cur.fetchall()]
        conn.close

    # バリューにセットするデータ用のリスト
    dict_data = []
    # SampleDataクラスのデータをdictに変換
    for item in data:
        item_dict = asdict(item)
        dict_data.append(item_dict)

    return dict_data


def put_sqs(dict_data):
    # sqs操作オブジェクト作成
    sqs = boto3.resource("sqs")
    # キュー情報の取得
    queue = sqs.get_queue_by_name(QueueName="sample-queue")
    # キューにメッセージを送信(MessageBodyはstrにすること)
    sqsresponse = queue.send_message(MessageBody=json.dumps({"sample": dict_data[0]}))

    print(json.dumps(sqsresponse))
