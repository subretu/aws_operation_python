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


class Role(BaseModel):
    user_id: str
    factory_name: str
    role: str


class UserForm(BaseModel):
    last_name: str
    first_name:str
    email: str
    company_name: str
    role: Role
