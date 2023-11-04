def get_date_summary(cur):
    cur.execute(
        """
        select
            id
            ,opsdate
            ,sum_value
        from
            sample_date_summary2
        order by
            opsdate
        ;
        """
    )
    rows = cur.fetchall()
    return rows


def get_time_summary(cur):
    cur.execute(
        """
        select
            opstime
            ,value
        from
            sample_date_summary
        order by
            opstime
        ;
        """
    )
    rows = cur.fetchall()
    return rows


def get_date_stack_summary(cur):
    cur.execute(
        """
        select
            opstime::date as opsdate
            ,sum(value) as sum_value1
            ,(sum(value)*1.1)::integer as sum_value2
            ,(sum(value)*0.6)::integer as sum_value3
        from
            sample_date_summary
        group by
            opstime::date
        order by
            opsdate
        ;
        """
    )
    rows = cur.fetchall()
    return rows


def delete_id(conn, cur, id):
    cur.execute(f"delete from sample_date_summary2 where id = '{id}' ;")
    conn.commit()


def insert_data(conn, cur, input_id, input_opsdate, input_value):
    cur.execute(
        f"insert into sample_date_summary2 (id, opsdate, sum_value) values({input_id}, '{input_opsdate}', {input_value});"
    )
    conn.commit()


def get_json_data(cur):
    cur.execute(
        """
        select
            json_data
        from
            sample_date_summary2
        limit 1
        ;
        """
    )
    rows = cur.fetchall()
    return rows


def get_member_name_data(conn, cur, id):
    cur.execute(f"select name from members where member_id = {id};")
    rows = cur.fetchall()
    return rows


def get_user(cur):
    cur.execute(
        """
        select
        a.user_name
        ,a.user_id
        ,b.company_name
        from
        public.user as a
        inner join
        company as b
        on
            a.company_id = b.id
        ;
        """
    )
    rows = cur.fetchall()
    return rows


def get_user_role(cur):
    cur.execute(
        """
    with join_company as(
      select
        a.user_name
        ,b.company_name
        ,a.user_id
        ,a.company_id
      from
        public.user as a
        inner join
        company as b
        on
          a.company_id = b.id
    ),
    join_factory as(
      select
        a.user_id
        ,b.factory_id
        ,b.factory_name
      from
        join_company as a
        inner join
        factory as b
        on
          a.company_id = b.company_id
    )
    select
      a.user_id
      ,a.factory_name
      ,b.role
    from
      join_factory as a
      inner join
      role as b
      on
        a.user_id = b.user_id
        and
        a.factory_id = b.factory_id
    ;
    """
    )
    rows = cur.fetchall()
    return rows


def get_all_member(cur):
    cur.execute(f"select member_id, name from members order by member_id;")
    rows = cur.fetchall()
    return rows
