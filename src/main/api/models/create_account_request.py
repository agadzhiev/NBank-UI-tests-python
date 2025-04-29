from src.main.api.models.base_model import BaseModel


class CreateAccountRequest(BaseModel):
    username: str
    password: str