import random
import uuid

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
    
    @staticmethod
    def generate():
        username = "user_" + str(uuid.uuid4())[:8]
        password = "pass_" + str(uuid.uuid4())[:8]
        role = random.choice(list(UserRole))
        return CreateUserRequest(username=username, 
                                 password=password, 
                                 role=role)

