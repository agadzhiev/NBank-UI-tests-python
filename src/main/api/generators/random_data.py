import random
import string
from faker import Faker

faker = Faker()


class RandomData:
    @staticmethod
    def get_username(length: int = 10) -> str:
        return ''.join(faker.random_letters(length))

    @staticmethod
    def get_password() -> str:
        upper = [random.choice(string.ascii_uppercase) for _ in range(3)]
        lower = [random.choice(string.ascii_lowercase) for _ in range(3)]
        digits = [random.choice(string.digits) for _ in range(2)]
        special = [random.choice("!@#$%^&*()_+-=")]
        all_chars = upper + lower + digits + special
        random.shuffle(all_chars)
        return ''.join(all_chars) + '$'
