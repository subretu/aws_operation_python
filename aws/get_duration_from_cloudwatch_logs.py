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

    duration_sum, count = extract_durations(results=results)

    print(
        f"Total Duration: {duration_sum} ms, Count: {count}, Average Duration: {duration_sum/count}"
    )


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


def extract_durations(results: list):
    duration_sum = 0
    count = 0

    for result in results:
        # 基本的には@messageは2つ目に出力される
        log_entry = result[1]

        if log_entry["field"] == "@message":
            value = log_entry["value"]

            # 正規表現でDurationの数値を抽出
            duration_match = re.search(r"Duration: (\d+\.\d+) ms", value)
            if duration_match:
                duration = duration_match.group(1)
                duration_sum += float(duration)
                count += 1
        else:
            print("No @message")

    return duration_sum, count


if __name__ == "__main__":
    main()
