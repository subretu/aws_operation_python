import boto3
from dataclasses import asdict, dataclass, field
from psycopg2.extras import RealDictCursor
from typing import List, Optional
import psycopg2
import re


@dataclass
class TestClasss:
    name: str
    date: str
    salary: int
    img_list: Optional[List[str]] = field(default=None)


def get_connection() -> psycopg2.connect:
    user = "postgres"
    pwd = "postgres"
    server = "127.0.0.1"
    port = "5432"
    db = "postgres"
    conn = psycopg2.connect(
        "host="
        + server
        + " port="
        + port
        + " dbname="
        + db
        + " user="
        + user
        + " password="
        + pwd
    )
    return conn


def get_s3_object() -> dict:
    s3_client = boto3.client("s3")
    bucket_name = "exampleread00000000"

    s3_object_list = {}

    response = s3_client.list_objects_v2(Bucket=bucket_name)
    while True:
        for obj in response["Contents"]:
            if obj["Size"] == 0:
                s3_object_list[obj["Key"][:-1]] = []

            if obj["Size"] > 0:
                key = (re.search(r"(.*)(?=/)", obj["Key"])).group()
                if key in s3_object_list.keys():
                    s3_object_list[key].append(obj["Key"])

        if "NextContinuationToken" in response:
            token = response["NextContinuationToken"]
            response = s3_client.list_objects_v2(
                Bucket=bucket_name, ContinuationToken=token
            )
        else:
            break

    return s3_object_list


def main() -> dict:
    # S3オブジェクト一覧を取得
    s3_objects = get_s3_object()

    conn = get_connection()
    sql = """
        select
            name
            ,(datetime::date)::text as date
            ,salary
        from
            saki
        limit
            5
        ;
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql)
        data = [TestClasss(**x) for x in cursor.fetchall()]

    main_data = []

    # TestClasssクラスをdictにして書き換え
    for item in data:
        item_dict = asdict(item)
        main_data.append(item_dict)

    for i, item in enumerate(main_data):
        if item["name"] in s3_objects.keys():
            main_data[i]["img_list"] = s3_objects[item["name"]]

    response_data = {"hogehoge": main_data}

    return response_data


if __name__ == "__main__":
    main()
