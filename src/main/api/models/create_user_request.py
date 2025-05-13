from src.main.api.models.base_model import BaseModel
from src.main.api.models.user_role import UserRole


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: UserRole

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data['role'] = self.role.value
        return data
