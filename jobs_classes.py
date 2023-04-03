class Vacancy:
    __slots__ = ['comany_name', 'salary', 'link']

    def __init__(self, company_name, salary, link):
        self.comany_name = company_name
        self.salary = salary
        self.link = link

    def __str__(self):
        return f'{self.comany_name}, зарплата: {self.salary} руб/мес'


class CountMixin:

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        with open('vacancies.json', 'r') as f:
            count = int(f.read())
        return print(count)


class HHVacancy(Vacancy, CountMixin):
    """ HeadHunter Vacancy """

    def __str__(self):
        return f'HH: {super().__str__()}'

    def __gt__(self, other):
        return self.salary > other.salary

    def __lt__(self, other):
        return self.salary < other.salary


class SJVacancy(Vacancy, CountMixin):
    """ SuperJob Vacancy """

    def __str__(self):
        return f'SJ: {super().__str__()}'

    def __gt__(self, other):
        return self.salary > other.salary

    def __lt__(self, other):
        return self.salary < other.salary


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    vacancies.sort()
    return vacancies


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    sorted_vacancies = sorting(vacancies)
    return sorted_vacancies[:top_count]

