from starlette.requests import Request
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from main.connection import get_connection
from main.query import (
    get_date_summary,
    get_time_summary,
    delete_id,
    insert_data,
    get_json_data,
    get_member_name_data,
    get_user,
    get_user_role,
    get_all_member_data,
)
from main.logger.my_logger import logging_function, set_logger
import main.schemas as schemas
import psycopg2.extras


logger = set_logger("uvicorn")

router = APIRouter()


@router.get("/day")
@logging_function(logger)
def get_day(request: Request):
    conn = get_connection()
    cur = conn.cursor()
    result_data_day = get_date_summary(cur)

    response_data = []

    for item, item1, item2 in result_data_day:
        response_data.append(
            {"id": item, "label": item1.strftime("%Y-%m-%d"), "data": item2}
        )

    cur.close()
    conn.close()

    # logger.info(response_data)

    return JSONResponse(content=response_data)


@router.get("/time")
def get_time(request: Request):
    conn = get_connection()
    cur = conn.cursor()
    result_data_time = get_time_summary(cur)

    labels1, values1 = [], []

    for item1, item2 in result_data_time:
        labels1.append(item1.strftime("%Y-%m-%d %H:%M:%S"))
        values1.append(item2)

    cur.close()
    conn.close()

    return JSONResponse(
        content={
            "label": labels1,
            "data": values1,
        }
    )


@router.get("/delete/{id}")
def detele(request: Request, id):
    conn = get_connection()
    cur = conn.cursor()
    delete_id(conn, cur, id)

    cur.close()
    conn.close()


@router.post("/insertdata")
def insertdata(input_data: dict):
    conn = get_connection()
    cur = conn.cursor()

    input_id = int(input_data["id"])
    input_opsdate = input_data["opsdate"]
    input_value = int(input_data["value"])

    print(input_id)
    print(input_opsdate)
    print(input_value)

    insert_data(conn, cur, input_id, input_opsdate, input_value)

    cur.close()
    conn.close()


@router.get("/task/{is_first}")
@logging_function(logger)
def get_task(request: Request, is_first):
    if is_first == "1":
        response_data = [{"id": 1, "task": "ローソンに行く", "limitd": "2022-10-01"}]
    else:
        response_data = [{"id": 2, "task": "ファミマに行く", "limitd": "2022-11-01"}]

    return JSONResponse(content=response_data)


@router.get("/jsondata")
@logging_function(logger)
def get_json(request: Request):
    conn = get_connection()
    cur = conn.cursor()
    result_json = get_json_data(cur)

    return JSONResponse(content=result_json)


@router.get("/get_member/{id}")
@logging_function(logger)
def get_member_name(request: Request, id):
    conn = get_connection()
    cur = conn.cursor()
    result_json = get_member_name_data(conn, cur, id)

    cur.close()
    conn.close()

    if len(result_json) == 0:
        raise HTTPException(status_code=400, detail="存在しないIDです。")

    return JSONResponse(content=result_json)


@router.get("/userinfo")
@logging_function(logger)
def get_user_info(request: Request):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # ユーザー情報を格納
    result_get_user = [schemas.UserList(**x) for x in get_user(cur)]
    user_list = []
    for item in result_get_user:
        user_list.append(item.dict())

    # ロール情報を格納
    result_get_user_role = [schemas.RoleList(**x) for x in get_user_role(cur)]
    role_list = []
    for item in result_get_user_role:
        role_list.append(item.dict())

    response_data = []

    for row_a in user_list:
        user_id_a = row_a["user_id"]
        row_a.setdefault("role", {})

        for row_b in role_list:
            if row_b["user_id"] == user_id_a:
                if row_b["factory_name"] not in row_a["role"]:
                    row_a["role"][row_b["factory_name"]] = row_b["role"]

        response_data.append(row_a)

    cur.close()
    conn.close()

    return JSONResponse(content=response_data)


@router.get("/all_member")
@logging_function(logger)
def get_all_member(request: Request):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    result = [schemas.MemberList(**x) for x in get_all_member_data(cur)]
    response_data = []
    for item in result:
        response_data.append(item.dict())

    cur.close()
    conn.close()

    return JSONResponse(content=response_data)


@router.post("/uploadcsv")
def upload_csv(input_data: dict):
    input_id = int(input_data["id"])

    print(input_id)
