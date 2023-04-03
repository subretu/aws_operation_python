import psycopg2


def main():
    # 選択されたID
    tareget_id = ["e", "g", "i"]
    tareget_id_count = len(tareget_id)
    # 対象IDの元の番号を取得（別途関数を用意）
    tareget_id_num = [5, 7, 9]

    # 指定された開始の順番
    start_num = 3

    excute_update(tareget_id, tareget_id_count, tareget_id_num, start_num)


def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="postgres",
        database="postgres",
        port=5432,
    )

    return connection


def excute_update(tareget_id, tareget_id_count, tareget_id_num, start_num):
    # taegetが該当する行のupdate文を作成
    update_sql_target = create_sql_target_row(tareget_id, start_num)
    # 残りの行を更新するupdate文を作成
    update_sql_other = create_sql_other_row(tareget_id_count, start_num, tareget_id_num)

    conn = get_db_connection()
    cursor = conn.cursor()

    # 残りの行を更新するupdate文から実行
    cursor.execute(update_sql_other[0], update_sql_other[1])
    cursor.execute(update_sql_target[0], update_sql_target[1])

    conn.commit()

    cursor.close()
    conn.close()


def create_sql_target_row(tareget_id, start_num):
    sql_part_1st = """
    update sample set num = case
    """
    sql_part_last = """
    else num end
    ;
    """

    sql_main = ""

    query_params = ()
    for i, id in enumerate(tareget_id):
        sql_main += """
        when  id = %s then %s
        """
        query_params += (id, start_num + i)

    sql = sql_part_1st + sql_main + sql_part_last

    return [sql, query_params]


def create_sql_other_row(tareget_id_count, start_num, tareget_id_num):
    sql_part_1st = """
    update sample set num = case
    """
    sql_part_last = """
    else num end
    ;
    """

    sql_main = ""

    # 残りの行更新用のupdate文
    # 指定の開始番号が1ではない場合
    if start_num > 1:
        sql_main = """
        when num between %s and %s then num + %s
        """
        params = [start_num, tareget_id_num[0] - 1, tareget_id_count]
    # 指定の開始順番が1の場合
    elif start_num == 1:
        sql_main = """
        when num < %s then num + %s
        """
        params = [tareget_id_num[0], tareget_id_count]
    else:
        raise ValueError("Invalid start num.")

    query_params = tuple(params)

    # 残りの行を更新
    for i in range(1, tareget_id_count):
        keisuu = tareget_id_count - i
        sql_main += """
        when num between %s and %s then num + %s
        """
        query_params += (tareget_id_num[i - 1] + 1, tareget_id_num[i] - 1, keisuu)

    sql = sql_part_1st + sql_main + sql_part_last

    return [sql, query_params]


if __name__ == "__main__":
    main()
