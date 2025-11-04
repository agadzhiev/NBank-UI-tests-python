from src.main.configs.config import Config


class BaseUITest:
    UI_BASE_URL = Config.get("UI_BASE_URL", "http://localhost:3000")