from boto3.client import BaseClient
import boto3
import time
from datetime import datetime, timezone
import re


LOG_GROUP_NAMES = ["/aws/lambda/sample-hoge"]

QUERY_STRING = "fields @timestamp, @message, @logStream, @log | sort @timestamp asc"

START_DATE_TIME = datetime(2025, 1, 4)
END_DATE_TIME = datetime(2025, 1, 7)

# LIMIT = 10


class QueryStatusException(Exception):
    pass


def main():
    client = boto3.client("logs")

    query_id = start_query(client=client)

    results = get_query_results(client=client, query_id=query_id)

    # 暫定で最後の実行から抽出するようにした
    # 配列の最後の要素を取得
    last_element = results[-1]
    # Lambdaの統計情報は基本的には最後に出るはず
    log_entry = last_element[1]["value"]

    # 正規表現でDurationの数値を抽出
    duration_match = re.search(r"Duration: (\d+\.\d+) ms", log_entry)
    if duration_match:
        duration = duration_match.group(1)
        print(f"{duration}")
    else:
        print("Duration not found")


def start_query(client: BaseClient) -> str:
    resp = client.start_query(
        logGroupNames=LOG_GROUP_NAMES,
        startTime=int(START_DATE_TIME.replace(tzinfo=timezone.utc).timestamp()),
        endTime=int(END_DATE_TIME.replace(tzinfo=timezone.utc).timestamp()),
        queryString=QUERY_STRING,
        # limit=LIMIT,
    )
    return resp["queryId"]


def get_query_results(client: BaseClient, query_id: str) -> list[dict]:
    while True:
        time.sleep(1)
        resp = client.get_query_results(queryId=query_id)

        if ["Scheduled", "Failed", "Cancelled", "Timeout", "Unknown"] in resp[
            "results"
        ]:
            raise QueryStatusException(resp["status"])

        if resp["status"] == "Running":
            continue

        if resp["status"] == "Complete":
            return resp["results"]


if __name__ == "__main__":
    main()
