import boto3
import time


def lambda_handler(event, context):
    main(event, context)


def main(event, context):
    create_data()


def wait_for_result(data_client, query_id: str, interval_sec=1):
    statement = ""
    status = ""
    while status != "FINISHED" and status != "FAILED" and status != "ABORTED":
        statement = data_client.describe_statement(Id=query_id)
        status = statement["Status"]
        time.sleep(interval_sec)
    return statement


def execute_query(
    data_client, cluster_identifier: str, database: str, db_user: str, sql: str
):
    return data_client.execute_statement(
        ClusterIdentifier=cluster_identifier,
        Database=database,
        DbUser=db_user,
        Sql=sql,
    )


def create_data():
    sql = """
    select
        *
    from
        hogehoge
    ;
    """

    # Redshiftにクエリを投げる。非同期なのですぐ返ってくる
    data_client = boto3.client("redshift-data")
    result = execute_query(
        data_client, "redshift_identifier", "sample_db", "test_user", sql
    )

    # 実行IDを取得
    query_id = result["Id"]

    # クエリが終わるのを待つ
    wait_for_result(data_client, query_id)
    # ページネーターを作成
    paginator = data_client.get_paginator("get_statement_result")
    # ページネーションを実施
    for resp in paginator.paginate(Id=query_id):
        print(resp)


if __name__ == "__main__":
    # lambda_handler(event, context)
    lambda_handler(1, 1)
