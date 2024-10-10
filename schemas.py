from pydantic import BaseModel
from typing import List, Optional

class UserResponse(BaseModel):
    id: int
    username: str
    number: Optional[int] = None


class UserGroupResponse(BaseModel):
    id: int
    name: str


class UserDetail(UserResponse):
    groups: List[UserGroupResponse] = []


class UserCreate(BaseModel):
    username: str
    number: Optional[int] = None
    group_ids: Optional[List[int]] = []


class UserUpdate(BaseModel):
    username: Optional[str] = None
    number: Optional[int] = None


class GroupCreate(BaseModel):
    name: str
    user_ids: Optional[List[int]] = []
    

class GroupUpdate(BaseModel):
    add_users: Optional[List[int]] = None
    remove_users: Optional[List[int]] = None


class GroupResponse(BaseModel):
    id: int
    name: str
    users: List[UserResponse]
