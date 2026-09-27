import csv
import functools
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from shared.student import STUDENT_NAME, VARIANT_NUMBER 

MIN_PASSWORD_LEN = 14
DATA_DIR = Path(__file__).parent / "data"
CSV_PATH = DATA_DIR / "users.csv"
LOG_PATH = DATA_DIR / "log.json"


class ValidationError(Exception):

    pass


def log_event(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        username = kwargs.get("username") or (args[0] if args else "unknown")
        result_flag = False
        error_msg = None

        try:
            result_flag = func(*args, **kwargs)
            return result_flag
        except Exception as e:
            error_msg = str(e)
            raise e
        finally:
            log_entry = {
                "event": "login",
                "user": username,
                "result": "success" if result_flag else "failure",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "args": [str(a) for a in args],
                "kwargs": {k: str(v) for k, v in kwargs.items()},
            }
            if error_msg:
                log_entry["error"] = error_msg

            logs = []
            if LOG_PATH.exists() and os.path.getsize(LOG_PATH) > 0:
                try:
                    with open(LOG_PATH, "r", encoding="utf-8") as f:
                        logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []

            logs.append(log_entry)

            with open(LOG_PATH, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)

    return wrapper


def generate_hash(password: str, salt: str = "00000") -> str:
    """Генерує sha3_256 хеш від пароля із сіллю."""
    if not password or not salt:
        raise ValueError("Пароль або сіль не можуть бути порожніми.")

    if len(password) < MIN_PASSWORD_LEN:
        raise ValidationError(
            f"Пароль коротший за мінімальну довжину ({MIN_PASSWORD_LEN} символів)."
        )

    salted_input = (password + salt).encode("utf-8")
    return hashlib.sha3_256(salted_input).hexdigest()


def get_personal_salt() -> str:
    """Створює персональну сіль у форматі 5 символів з нулями зліва."""
    return str(VARIANT_NUMBER).zfill(5)


def create_user(username: str, password: str) -> tuple[str, str]:
    """Створює кортеж (username, hash_value)."""
    salt = get_personal_salt()
    hash_val = generate_hash(password, salt)
    return (username, hash_val)


def create_users(users_list: tuple[tuple[str, str], ...]) -> None:
    """Записує базу користувачів у CSV файл."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    prepared_users = []
    for u, p in users_list:
        try:
            prepared_users.append(create_user(u, p))
        except (ValidationError, ValueError) as e:
            print(f"[Помилка створення користувача {u}]: {e}")

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password_hash"])
        writer.writerows(prepared_users)


def read_users_db() -> list[dict[str, str]]:
    """Зчитує користувачів з CSV-файлу."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Файл {CSV_PATH} не знайдено.")

    users_db = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users_db.append(row)
    return users_db


@log_event
def login(username: str, password: str) -> bool:
    """Спроба авторизації користувача."""
    if not username or not password:
        raise ValueError("Логін та пароль є обов'язковими.")

    users_db = read_users_db()
    salt = get_personal_salt()

    try:
        input_hash = generate_hash(password, salt)
    except ValidationError:
        return False

    for record in users_db:
        if record["username"] == username:
            return record["password_hash"] == input_hash

    return False


def run_task3() -> None:
    print("\n" + "=" * 60)
    print(f"ЗАВДАННЯ 3 | Студент: {STUDENT_NAME} | Варіант: {VARIANT_NUMBER}")
    print("=" * 60)

    users_to_register = (
        ("admin", "SuperSecurePass123!"),
        ("analyst", "DataAnalyst2026#"),
        ("dev1", "Short1!"),
        ("user2", "ComplexPass999#"),
        ("user3", "SecureUserPass_77"),
        ("user4", "AnotherStrongPass1!"),
        ("user5", "ValidPassword_1234"),
        ("user6", "GoodPassphrase_2026"),
        ("user7", "RobustPassword#123"),
        ("user8", "FinalTestPassword99"),
    )

    try:
        print("\n1. Реєстрація користувачів...")
        create_users(users_to_register)

        print("\n2. База даних користувачів з CSV:")
        db = read_users_db()
        print(f"{'Логін':<15} | {'Хеш пароля (sha3_256)':<64}")
        print("-" * 82)
        for row in db:
            print(f"{row['username']:<15} | {row['password_hash']:<64}")

        print("\n3. Перевірка авторизації (Логування в JSON):")
        res1 = login("admin", "SuperSecurePass123!")
        print(f"Вхід admin (вірно): {res1}")
        res2 = login("admin", "WrongPassword12345!")
        print(f"Вхід admin (невірно): {res2}")

    except (
        FileNotFoundError,
        PermissionError,
        IOError,
        ValidationError,
        ValueError,
    ) as e:
        print(f"\n[Перехоплено виняток]: {e}")


if __name__ == "__main__":
    run_task3()