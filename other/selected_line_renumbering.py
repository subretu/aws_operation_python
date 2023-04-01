import psycopg2


def main():
    excute_update()


def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        user="hoge",
        password="hoge",
        database="hoge",
        port=5432,
    )

    return connection


def excute_update():
    # 選択されたID
    tareget_id = ["e", "g", "i"]
    tareget_id_count = len(tareget_id)

    # 指定された開始の順番
    start_num = 3

    # 対象IDの元の番号を取得（別途関数を用意）
    tareget_id_num = [5, 7, 9]

    # taegetが該当する行のupdate文を作成
    update_sql_target = create_sql_target_row(tareget_id, start_num)
    # 残りの行を更新するupdate文を作成
    update_sql_other = create_sql_other_row(tareget_id_count, start_num, tareget_id_num)

    print(update_sql_target)
    print(update_sql_other)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(update_sql_other)

    for sql in update_sql_target:
        cursor.execute(sql)

    conn.commit()

    cursor.close()
    conn.close()


def create_sql_target_row(tareget_id, start_num):
    sql_list = []
    sql_list.append(f"update sample set num = {start_num} where id = 'e';")
    sql_list.append(f"update sample set num = {start_num+1} where id = 'g';")
    sql_list.append(f"update sample set num = {start_num+2} where id = 'i';")

    return sql_list


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
        sql_main = f"""
        when {start_num} <= num and num < {tareget_id_num[0]} then num + {tareget_id_count}
        """
    # 指定の開始順番が1の場合
    elif start_num == 1:
        sql_main = f"""
        when num < {tareget_id_num[0]} then num + {tareget_id_count}
        """
    else:
        raise ValueError("Invalid start num.")

    # 残りの行を更新
    for i in range(1, tareget_id_count):
        keisuu = tareget_id_count - i
        sql_main += f"""
        when {tareget_id_num[i-1]} < num and num < {tareget_id_num[i]} then num + {keisuu}
        """

    sql = sql_part_1st + sql_main + sql_part_last

    return sql


if __name__ == "__main__":
    main()
