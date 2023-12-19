import psycopg2


# DB接続用関数
def get_connection():
    user = "postgres"
    pwd = "postgres"
    server = "127.0.0.1"
    port = "5432"
    db = "postgres"

    con = psycopg2.connect(
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

    return con
