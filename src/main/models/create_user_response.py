from typing import Optional, List, Dict, Any

from src.main.models.base_model import BaseModel


class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    name: Optional[str]
    role: str
    accounts: List[Dict[str, Any]]