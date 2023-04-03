from engine_classes import HHVacancyAPI, SuperJobVacancyAPI, JSONVacancyManager, Vacancy
import json


def interact_with_user():
    api_choice = input('Выберите API для поиска вакансий:\n1. HeadHunter\n2. SuperJob\n')
    if api_choice == '1':
        api = HHVacancyAPI()
    elif api_choice == '2':
        app_id = input('Введите X-Api-App-Id: ')
        api = SuperJobVacancyAPI(app_id)
    else:
        print('Выбор некорректен.')
        return

    search_text = input('Введите название вакансий: ')
    per_page = int(input('Введите количество вакансий на странице (целое число): '))
    api.per_page = per_page

    vacancies = api.get_vacancies(search_text)

    manager = JSONVacancyManager('vacancies.json')

    for vacancy_data in vacancies:
        title = vacancy_data.get('name')
        url = vacancy_data.get('alternate_url')
        salary = vacancy_data.get('salary')
        description = vacancy_data.get('description')
        vacancy = Vacancy(title, url, salary, description)
        try:
            vacancy.validate_salary()
            manager.add_vacancy(vacancy)
        except ValueError as e:
            print(f'Вакансия {title} не была добавлена: {e}')

        search_result = manager.get_vacancies(search_text=search_text)

        if not search_result:
            print('По вашему запросу ничего не найдено.')

    while True:
        print('1. Просмотреть список вакансий')
        print('2. Очистить список вакансий')
        print('3. Выход')
        choice = input('Выберите действие: ')
        if choice == '1':
            with open('vacancies.json', 'r', encoding='utf-8') as file:
                jobs = json.load(file)
            search_result = jobs

            for vacancy in search_result:
                if vacancy["salary"] is not None:
                    salary_from = vacancy["salary"]["from"]
                    salary_to = vacancy["salary"]["to"]
                else:
                    salary_from = None
                    salary_to = None
                print(f"{vacancy['title']}, Зарплата от {salary_from} до {salary_to}, {vacancy['url']}")
        elif choice == '2':
            confirm = input('Вы действительно хотите очистить список вакансий? (да/нет): ')
            if confirm == 'да':
                jobs = []
                with open('vacancies.json', 'w', encoding='utf-8') as file:
                    json.dump(jobs, file, ensure_ascii=False)
                    print('Список вакансий очищен.')
            else:
                print('Отменено.')

        elif choice == '3':
            print('Выход')
            break


if __name__ == '__main__':
    interact_with_user()
