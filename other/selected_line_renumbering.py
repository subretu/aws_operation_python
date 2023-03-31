# 選択されたID
tareget_id = ["c", "e", "g"]
tareget_id_count = len(tareget_id)

# 指定された開始の順番
start_num = 3

# 対象IDの元の番号を取得（別途関数を用意）
tareget_id_num = [5, 7, 9]

# ここでtaegetが該当する行のupdate文を作成（TBD）
for id in tareget_id:
    pass

# 残りの行更新用のupdate文
# 指定の開始番号が1出ない場合
if start_num > 1:
    sql_1st = f"""
    update sample
      set
        num = num + {tareget_id_count}
    where
      {start_num} < num and num < {tareget_id_num[0]}
    ;
    """

    print(sql_1st)

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

        print(sql_2st)
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

    print(sql_1st)

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

        print(sql_2st)
else:
    raise ValueError("Invalid start num.")
