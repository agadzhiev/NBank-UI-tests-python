from src.main.models.base_model import BaseModel


class LoginUserRequest(BaseModel):
    username: str
    password: str