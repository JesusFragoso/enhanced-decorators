from pydantic import BaseModel
from pydantic import Field
import uuid


class User(BaseModel):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    age: int


class AccountUser(User):
    bank_account_mount: float
    is_alive: bool