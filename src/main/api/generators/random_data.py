import random
from faker import Faker

faker = Faker()


class RandomData:
    @staticmethod
    def get_username(length: int = random.randint(3, 15)) -> str:
        return ''.join(faker.random_letters(length))
    
    @staticmethod
    def get_password() -> str:
        upper = [letter.upper() for letter in faker.random_letters(length=3)]
        lower = [letter.lower() for letter in faker.random_letters(length=3)]
        digits = [str(faker.random_digit()) for _ in range(3)]
        special = [random.choice('!@#$%^&')]
        password = upper + lower + digits + special
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def get_amount(min_value: float = 0.01, max_value: float = 9999.9, precision: int = 2) -> float:
        return round(random.uniform(min_value, max_value), precision)

    @staticmethod
    def get_full_name() -> str:
        return f"{faker.first_name()} {faker.last_name()}"