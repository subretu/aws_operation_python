import boto3

# 対象バケットのオブジェクト一覧を表示
s3_client = boto3.client("s3")
bucket_name = "exampleread00000000"
folder_name = "test1"
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
for obj in response["Contents"]:
    if obj["Size"] > 0:
        print(obj)
        print(obj["Key"])
