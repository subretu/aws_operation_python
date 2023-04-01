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
    tareget_id = ["e", "f", "g", "i"]
    tareget_id_count = len(tareget_id)

    # 指定された開始の順番
    start_num = 2

    # 対象IDの元の番号を取得（別途関数を用意）
    tareget_id_num = [5, 6, 7, 9]

    # taegetが該当する行のupdate文を作成
    update_sql_target = create_sql_target_row(tareget_id, start_num)
    # 残りの行を更新するupdate文を作成
    update_sql_other = create_sql_other_row(tareget_id_count, start_num, tareget_id_num)

    print(update_sql_target)
    print(update_sql_other)

    conn = get_db_connection()
    cursor = conn.cursor()

    for sql in reversed(update_sql_other):
        cursor.execute(sql)

    for sql in update_sql_target:
        cursor.execute(sql)

    conn.commit()

    cursor.close()
    conn.close()


def create_sql_target_row(tareget_id, start_num):
    sql_list = []
    sql_list.append(f"update sample set num = {start_num} where id = 'e';")
    sql_list.append(f"update sample set num = {start_num+1} where id = 'f';")
    sql_list.append(f"update sample set num = {start_num+2} where id = 'g';")
    sql_list.append(f"update sample set num = {start_num+3} where id = 'i';")

    return sql_list


def create_sql_other_row(tareget_id_count, start_num, tareget_id_num):
    sql_list = []

    # 残りの行更新用のupdate文
    # 指定の開始番号が1出ない場合
    if start_num > 1:
        sql_1st = f"""
        update sample
          set
            num = num + {tareget_id_count}
        where
          {start_num} <= num and num < {tareget_id_num[0]}
        ;
        """

        sql_list.append(sql_1st)

        # 残りの行を更新
        for i in range(1, tareget_id_count):
            keisuu = tareget_id_count - i
            sql_2st = f"""
            update sample
              set
                num = num + ({keisuu})
            where
              {tareget_id_num[i-1]} < num and num < {tareget_id_num[i]}
            ;
            """

            sql_list.append(sql_2st)

        return sql_list

    # 指定の開始順番が1の場合
    elif start_num == 1:
        sql_1st = f"""
        update sample
          set
            num = num + {tareget_id_count}
        where
          num < {tareget_id_num[0]}
        ;
        """

        sql_list.append(sql_1st)

        # 残りの行を更新
        for i in range(1, tareget_id_count):
            keisuu = tareget_id_count - i
            sql_2st = f"""
            update sample
              set
                num = num+({keisuu})
              where
                {tareget_id_num[i-1]} < num and num < {tareget_id_num[i]}
            ;
            """

            sql_list.append(sql_2st)

        return sql_list
    else:
        raise ValueError("Invalid start num.")


if __name__ == "__main__":
    main()
