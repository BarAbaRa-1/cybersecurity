import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from shared.student import STUDENT_NAME, VARIANT_NUMBER 

users = {
    "ai_security_expert": {
        "role": "ai_security",
        "clearance": 4,
        "department": "AI Security",
        "active": True,
    },
    "ml_engineer": {
        "role": "ml_engineer",
        "clearance": 3,
        "department": "Machine Learning",
        "active": True,
    },
    "data_engineer": {
        "role": "data_engineer",
        "clearance": 2,
        "department": "Data Engineering",
        "active": True,
    },
    "research_assistant": {
        "role": "researcher",
        "clearance": 2,
        "department": "Research",
        "active": True,
    },
    "training_bot": {
        "role": "bot_account",
        "clearance": 1,
        "department": "Automation",
        "active": False,
    },
}

resources = [
    ("ai_models", 4),
    ("training_datasets", 3),
    ("data_pipelines", 2),
    ("research_notebooks", 2),
    ("model_artifacts", 4),
    ("synthetic_data", 1),
    ("adversarial_tests", 3),
    ("model_registry", 4),
    ("feature_stores", 2),
    ("public_models", 1),
]

security_levels = (
    "Open Source",
    "Internal Research",
    "Proprietary",
    "Trade Secret",
)
blocked_users = {"training_bot", "model_theft", "data_poisoning_acc"}


def check_access(username: str, resource_level: int) -> tuple[bool, str]:
    if username not in users:
        return False, "User not found"

    if username in blocked_users:
        return False, "User is blocked"

    user_info = users[username]
    if not user_info.get("active", False):
        return False, "Account inactive"

    if user_info.get("clearance", 0) >= resource_level:
        return True, "Access granted"

    return False, "Insufficient clearance"


def run_task2() -> None:
    print("\n" + "=" * 60)
    print(f"ЗАВДАННЯ 2 | Студент: {STUDENT_NAME} | Варіант: {VARIANT_NUMBER}")
    print("=" * 60)

    print("\n СПИСОК РЕСУРСІВ СИСТЕМИ:")
    print("-" * 45)
    for res_name, level_num in resources:
        level_text = security_levels[level_num - 1]
        print(f"Ресурс: {res_name:<20} | Рівень: {level_text}")

    print("\n ПЕРЕВІРКА ПРАВ ДОСТУПУ:")
    print("-" * 75)

    test_users = list(users.keys()) + ["unknown_user", "model_theft"]

    for user in test_users:
        for res_name, level_num in resources[:3]:
            allowed, reason = check_access(user, level_num)
            status = "ALLOW" if allowed else f"DENY ({reason})"
            print(f"user=[{user}] resource=[{res_name}] -> {status}")


if __name__ == "__main__":
    run_task2()