import boto3


s3_client = boto3.client("s3")
bucket_name = "exampleread00000000"
folder_name = "test1"

response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
while True:
    # バケット内のファイルを表示
    for obj in response["Contents"]:
        # フォルダはsizeが0となるため除外
        if obj["Size"] > 0:
            print(obj["Key"])

    # NextContinuationTokenが存在する場合は次のデータ取得
    if "NextContinuationToken" in response:
        token = response["NextContinuationToken"]
        response = s3_client.list_objects_v2(
            Bucket=bucket_name, Prefix=folder_name, ContinuationToken=token
        )
    else:
        break
