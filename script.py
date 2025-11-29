import argparse
from argparse import Namespace
import csv
from reports import REPORTS


def read_csv(paths: list) -> list:
    data = []
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"По этому пути файл не найден: {path}")
    return data


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(
        description="Генерация отчета о сотрудниках"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Путь к файлом для отчета",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=REPORTS.keys(),
        help="Тип отчета",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    report_class = REPORTS[args.report]
    report = report_class()

    data = read_csv(args.files)
    for row in data:
        report.process_row(row)

    print(report.render())


if __name__ == "__main__":
    main()
