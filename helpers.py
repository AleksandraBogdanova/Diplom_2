import random
import string

from faker import Faker

fake = Faker()


def random_email() -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{suffix}@yandex.ru"


def random_password(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def random_name() -> str:
    return fake.first_name()


def build_user_payload(email: str | None = None,
                       password: str | None = None,
                       name: str | None = None) -> dict:
    payload = {}
    if email is not None:
        payload["email"] = email
    if password is not None:
        payload["password"] = password
    if name is not None:
        payload["name"] = name
    return payload