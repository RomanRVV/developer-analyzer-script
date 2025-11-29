# developer-analyzer-script 

Скрипт для создания отчетов с анализом эффективности работы разработчиков по CSV файлам

## Как установить и запустить

Скачайте репозиторий к себе на локальную машину
```sh
git clone https://github.com/RomanRVV/developer-analyzer-script.git
```

Скачайте и установите [Poetry](https://python-poetry.org/)

После в проекте:
```sh
poetry install # Установит зависимости из pyproject.toml
```

## Запуск скрипта:

В репозитории хранятся, тестовые csv файлы для проверки работоспособности скрипта:
```sh
python script.py --files test_data/employees1.csv test_data/employees2.csv --report performance
```

## Добавление нового отчёта:

1. В `reports.py` создай класс, наследующий `BaseReport`:
```python
class SkillsReport(BaseReport):
    def process_row(self, row: dict) -> None:
        # логика обработки строки из CSV
        position = row["name"]
        skills = row["skills"]
        self.salary_by_position[position].append(skills)
    
    def render(self) -> str:
        # код для упаковки обработанных данных в формат для вывода
        ...
        return tabulate(...)
```

2. Добавь в `REPORTS` в конце `reports.py`:
```python
REPORTS = {
    "performance": PerformanceReport,
    "skills": SkillsReport,
}
```
