from abc import ABC, abstractmethod
import json
import requests


class AbstractVacancyAPI(ABC):
    """AbstractVacancyAPI - абстрактный базовый класс для API, который определяет метод """
    @abstractmethod
    def get_vacancies(self, search_text):
        """get_vacancies() для получения списка вакансий."""
        pass


class HHVacancyAPI(AbstractVacancyAPI):
    """HHVacancyAPI - класс, который реализуют метод get_vacancies() для получения списка вакансий с использованием конкретных API."""
    BASE_URL = 'https://api.hh.ru/vacancies'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/58.0.3029.110 Safari/537.3'}

    def __init__(self, per_page=100):
        self.per_page = per_page

    def get_vacancies(self, search_text):
        params = {'text': search_text, 'per_page': self.per_page}
        response = requests.get(self.BASE_URL, headers=self.HEADERS, params=params)
        response.raise_for_status()
        vacancies = response.json()['items']
        return vacancies


class SuperJobVacancyAPI(AbstractVacancyAPI):
    """SuperJobVacancyAPI - класс, который реализуют метод get_vacancies() для получения списка вакансий с использованием конкретных API."""
    BASE_URL = 'https://api.superjob.ru/2.0/vacancies/'
    HEADERS = {'X-Api-App-Id': 'YOUR_APP_ID', 'User-Agent': 'Mozilla/5.0'}

    def __init__(self, per_page=100):
        self.per_page = per_page

    def get_vacancies(self, search_text):
        params = {'keyword': search_text, 'count': self.per_page}
        response = requests.get(self.BASE_URL, headers=self.HEADERS, params=params)
        response.raise_for_status()
        vacancies = response.json()['objects']
        return vacancies


class Vacancy:
    """Vacancy - класс, который представляет собой модель вакансии. Он имеет поля, такие как title, url, salary и description,
     а также методы, такие как __str__(), __repr__(), __eq__() и __lt__()"""
    def __init__(self, title, url, salary, description):
        self.title = title  # Название вакансии
        self.url = url  # Ссылка на вакансию
        self.salary = salary # Заработная плата вакансии
        self.description = description  # Описание вакансии

    def __str__(self):
        salary_text = ""
        if self.salary:
            if self.salary.get('from') is not None and self.salary.get('to') is not None:
                salary_text = f"{self.salary.get('from')} - {self.salary.get('to')} {self.salary.get('currency')}"
            elif self.salary.get('from') is not None:
                salary_text = f"от {self.salary.get('from')} {self.salary.get('currency')}"
            elif self.salary.get('to') is not None:
                salary_text = f"до {self.salary.get('to')} {self.salary.get('currency')}"
        return f'{self.title}, {salary_text}, {self.url}'

    def __repr__(self):
        return f'Vacancy({self.title}, {self.url}, {self.salary}, {self.description})'

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self.salary.get('from', 0) < other.salary.get('from', 0)

    def validate_salary(self):
        if self.salary and not isinstance(self.salary, dict):
            raise ValueError('Salary must be a dictionary')


class AbstractVacancyManager(ABC):
    """AbstractVacancyManager - абстрактный базовый класс менеджера вакансий, который определяет методы add_vacancy(),
    get_vacancies() и delete_vacancy() для управления вакансиями."""
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **kwargs):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONVacancyManager(AbstractVacancyManager):
    """JSONVacancyManager - класс, который реализует методы менеджера вакансий для хранения и поиска вакансий в формате JSON файлов."""
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies = []
        self.load()

    def add_vacancy(self, vacancy):
        if vacancy in self.vacancies:
            return
        self.vacancies.append(vacancy)
        self.save()

    def get_vacancies(self, **kwargs):
        search_text = kwargs.get('search_text')
        min_salary = kwargs.get('min_salary')
        vacancies = self.vacancies
        if search_text:
            vacancies = [v for v in vacancies if search_text.lower() in v.title.lower() or
                         (v.description and search_text.lower() in v.description.lower())]
        if min_salary:
            vacancies = [v for v in vacancies if v.salary and v.salary.isdigit() and int(v.salary) >= min_salary]
        return vacancies

    def delete_vacancy(self, vacancy):
        self.vacancies.remove(vacancy)
        self.save()

    def save(self):
        with open(self.file_name, 'w') as f:
            json.dump([vars(v) for v in self.vacancies], f, indent=4)

    def load(self):
        try:
            with open(self.file_name, 'r') as f:
                vacancy_data = json.load(f)
                self.vacancies = [Vacancy(**data) for data in vacancy_data]
        except FileNotFoundError:
            pass

    def clear(self):
        self.vacancies = []
        self.save()
