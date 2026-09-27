"""Головний файл запуску Лабораторної роботи №1."""

import sys
from pathlib import Path

# Додаємо корінь проекту та папку lab01 у шлях пошуку Python
BASE_DIR = Path(__file__).resolve().parents[2]  # Папка cybersecurity
LAB_DIR = Path(__file__).resolve().parent       # Папка lab01

sys.path.append(str(BASE_DIR))
sys.path.append(str(LAB_DIR))

from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER  # noqa: E402
from task1 import run_task1  # noqa: E402
from task2 import run_task2  # noqa: E402
from task3 import run_task3  # noqa: E402


def main() -> None:
    """Запуск усіх завдань лабораторної роботи."""
    print("*" * 65)
    print(" ЛАБОРАТОРНА РОБОТА №1")
    print(f" Студент: {STUDENT_NAME}")
    print(f" Група:   {GROUP_NAME}")
    print(f" Варіант: {VARIANT_NUMBER}")
    print("*" * 65)

    run_task1()
    run_task2()
    run_task3()


if __name__ == "__main__":
    main()