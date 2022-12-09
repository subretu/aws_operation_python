import datetime
from dateutil.relativedelta import relativedelta
import boto3
import json
import time


def lambda_handler(event, context):
    main(event, context)


def wait_for_result(data_client, id, interval_sec=1):
    statement = ""
    status = ""
    while status != "FINISHED" and status != "FAILED" and status != "ABORTED":
        statement = data_client.describe_statement(Id=id)
        status = statement["Status"]
        time.sleep(interval_sec)
    return


def main(event, context):
    # トリガーのSQSからメッセージを取得
    key = event["Records"][0]["body"]
    # 実行日より前月を取得
    last_month = (datetime.date.today() + relativedelta(months=-1)).strftime("%Y-%m")
    # SQSに送るメッセージを作成
    data = create_data(key, last_month)
    # SQSにメッセージを送信
    put_sqs(data)


def create_data(key, last_month):
    sql = f"""
    select
        key
        ,to_char(opsdate, 'yyyy-mm') as last_month
        ,sum(value_data1) as value_data1
        ,sum(value_data2) as value_data2
    from

    where
        key = '{key}'
        and
        last_month = '{last_month}'
    group by
        key, last_month
    ;
    """

    # Redshiftにクエリを投げる。非同期なのですぐ返ってくる
    data_client = boto3.client("redshift-data")
    result = data_client.execute_statement(
        ClusterIdentifier="test-cluster",
        Database="test-db",
        DbUser="test",
        Sql=sql,
    )

    # 実行IDを取得
    query_id = result["Id"]

    # クエリが終わるのを待つ
    statement = wait_for_result(data_client, query_id)
    status = statement["Status"]

    if status == "FINISHED":
        # クエリ結果を取得
        statement = data_client.get_statement_result(Id=query_id)

        result = []
        result_data = {}
        # クエリ結果からdict形式にデータを加工
        for i, data in enumerate(statement["ColumnMetadata"]):
            result_data[data["name"]] = list((statement["Records"][0][i]).values())[0]

        result.append(result_data)

    return result


def put_sqs(result_data):
    # sqs操作オブジェクト作成
    sqs = boto3.resource("sqs")
    # キューの取得
    queue = sqs.get_queue_by_name(QueueName="sample-queue")
    # キューにメッセージを送信
    sqsresponse = queue.send_message(MessageBody=json.dumps({"test": result_data}))

    print(json.dumps(sqsresponse))
