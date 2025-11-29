from collections import defaultdict
from tabulate import tabulate
from abc import ABC, abstractmethod
from typing import Union


class BaseReport(ABC):
    """
    Родительский класс для последующего наследование для создания отчетов
    """
    @abstractmethod
    def process_row(self, row: dict) -> None:
        ...

    @abstractmethod
    def render(self) -> str:
        ...


class PerformanceReport(BaseReport):
    """
    Класс для создания отчета о средней эффективности
    """
    def __init__(self) -> None:
        self.performance_by_position: dict[str, list[float]] = defaultdict(list)   # noqa: E501

    def process_row(self, row: dict) -> None:
        position = row["position"]
        performance = float(row["performance"])
        self.performance_by_position[position].append(performance)

    def render(self) -> str:
        table: list[list[Union[str, float]]] = []
        for position, values in self.performance_by_position.items():
            avg_perf = sum(values) / len(values)
            table.append([position, round(avg_perf, 2)])

        table.sort(key=lambda x: x[1], reverse=True)

        showindex = range(1, len(table) + 1)

        print(table)

        return tabulate(
            table,
            headers=["position", "performance"],
            showindex=showindex
        )


REPORTS = {
    "performance": PerformanceReport,
}
