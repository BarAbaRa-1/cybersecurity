import random
import string
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER 

passwords = [
    "Compli4nc3@Check",
    "12345678",
    "weak",
    "Risk@Ass3ssment",
    "guest",
    "Vulner4bility@Scan",
    "temp",
    "P3netration@Test",
    "demo",
    "S3curity@Audit",
    "trial",
]
criteria = {
    "min_length": 8,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}
forbidden_passwords = {"weak", "guest", "temp", "demo", "trial", "password"}


def check_password_strength(
    password: str,
    all_passwords: list[str],
    criteria_dict: dict,
    forbidden_set: set[str],
) -> str:
    min_length = criteria_dict["min_length"]

    if password in forbidden_set or len(password) < min_length:
        return "Заборонений"

    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_special = any(char in string.punctuation for char in password)

    matches = [has_digit, has_upper, has_lower, has_special]
    if sum(matches) == 1:
        return "Слабкий"

    all_criteria_met = (
        len(password) >= min_length
        and (not criteria_dict.get("require_digits") or has_digit)
        and (not criteria_dict.get("require_upper") or has_upper)
        and (not criteria_dict.get("require_special") or has_special)
        and has_lower
    )
    is_unique = all_passwords.count(password) == 1
    if all_criteria_met and len(password) >= (min_length + 4) and is_unique:
        return "Дуже сильний"
    if all_criteria_met and len(password) < (min_length + 4):
        return "Сильний"
    return "Середній"


def run_task1() -> None:
    print("=" * 60)
    print(f"ЗАВДАННЯ 1 | Студент: {STUDENT_NAME} | Варіант: {VARIANT_NUMBER}")
    print("=" * 60)

    random.seed(42)
    duplicated_passwords = passwords.copy()
    random_indices = random.sample(range(len(passwords)), 3)
    for idx in random_indices:
        duplicated_passwords.append(passwords[idx])

    print(f"{'Пароль':<25} | {'Рівень надійності':<20}")
    print("-" * 50)
    for pwd in duplicated_passwords:
        strength = check_password_strength(
            pwd, duplicated_passwords, criteria, forbidden_passwords
        )
        print(f"{pwd:<25} | {strength:<20}")


if __name__ == "__main__":
    run_task1()
