#!/usr/bin/env python3
import os.path


def main():
    days = int(input("Number of days: "))

    project_path = os.path.dirname(os.path.abspath(__file__))

    for i in range(1, days + 1):
        for part in "a", "b":
            part_path = os.path.join(project_path, f"day{i}_{part}")

            if os.path.exists(part_path):
                continue

            os.makedirs(part_path)

            for file in "main.py", "puzzle.txt":
                file_path = os.path.join(part_path, file)
                open(file_path, "w").close()


if __name__ == "__main__":
    main()
