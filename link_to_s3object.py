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


def main():
    s3_objects = get_s3_object()
    linkdata = link_to_s3object(s3_objects)

    print(linkdata)


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
                # フォルダ名からkeyを作成して初期化
                s3_object_list[obj["Key"][:-1]] = []

            if obj["Size"] > 0:
                # 該当するkeyのvalueにオブジェクトのキーを挿入
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


def link_to_s3object(s3_objects: dict) -> dict:
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

    # 一致するデータのimg_listをS3オブジェクト一覧の該当する値に書き換え
    for i, item in enumerate(main_data):
        if item["name"] in s3_objects.keys():
            main_data[i]["img_list"] = s3_objects[item["name"]]

    response_data = {"hogehoge": main_data}
    return response_data


if __name__ == "__main__":
    main()
