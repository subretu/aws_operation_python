from pydantic import BaseModel


class UserList(BaseModel):
    user_name: str
    user_id: int
    company_name: str


class RoleList(BaseModel):
    user_id: int
    factory_name: str
    role: str


class MemberList(BaseModel):
    member_id: int
    name: str
