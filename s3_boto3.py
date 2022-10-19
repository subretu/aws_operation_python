import boto3

# 対象バケットのオブジェクト一覧を表示
s3_client = boto3.client('s3')
bucket_name = "mailbody00001111"
response = s3_client.list_objects_v2(Bucket=bucket_name)
for obj in response['Contents']:
    print(obj)
    print(obj['Key'])
