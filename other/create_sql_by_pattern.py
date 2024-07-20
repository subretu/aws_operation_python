import psycopg2


def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="postgres",
        database="postgres",
        port=5432,
    )

    return connection


def main(pattern: str):
    pattern_a = "opstime between '2022-03-01 10:00:00' and '2022-03-01 12:00:00'"
    pattern_b = "opstime = '2022-03-03 10:00:00'"
    pattern_c = "to_char(opstime, 'yyyy-mm') = '2022-03'"

    pattern_var = locals().get(f"pattern_{pattern}")

    sql_parts = [
        "select * from public.sample_date_summary where",
        pattern_var,
        "and value > 0;",
    ]

    sql = "\n".join(sql_parts)

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
            print(data)

    conn.close()


if __name__ == "__main__":
    main(pattern="a")
