from src.main.api.models.base_model import BaseModel


class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    name: str
    role: str
    accounts: list[str]