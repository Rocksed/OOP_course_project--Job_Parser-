from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from connector import Connector


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    @abstractmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):

    @staticmethod
    def get_request(url, params):
        """Метод для получения данных с сайта hh.ru"""

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_connector(file_name):
        """Возвращает экземпляр класса Connector"""
        return Connector(file_name)

    @staticmethod
    def get_vacancies(keywords, area=1, period=30):
        """Метод для получения списка вакансий с сайта hh.ru"""

        url = 'https://api.hh.ru/vacancies'
        params = {'text': keywords,
                  'area': area,
                  'period': period}
        vacancies = HH.get_request(url, params)['items']
        return vacancies



class SuperJob(Engine):
    """Парсер код сайта superjob.ru"""

    @staticmethod
    def get_request(url, headers=None, params=None):
        """Метод для получения данных с сайта superjob.ru"""

        headers = headers or {}
        headers.setdefault('User-Agent',
                           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.text

    @staticmethod
    def get_vacancies(keywords, area=1, period=30):
        """Метод для получения списка вакансий с сайта superjob.ru"""

        url = 'https://www.superjob.ru/vacancy/search/'
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        params = {'keywords': keywords,
                  'geo[t][0]': area,
                  'page': 1}
        html = SuperJob.get_request(url, headers=headers, params=params)
        soup = BeautifulSoup(html, 'html.parser')
        vacancies = []
        for vacancy in soup.find_all('div', {'class': 'f-test-vacancy-item'}):
            title = vacancy.find('a', {'class': 'icMQ_'})
            if title:
                vacancies.append(title.get('href'))
        return vacancies

if __name__ == '__main__':
    conn = HH.get_connector('vacancies.json')
    # получаем список вакансий
    vacancies = {'id': 1, 'title': 'tet'}
    for vacancy in vacancies:
        # сохраняем каждую вакансию в файл
        conn.insert(vacancy)
    # удаляем все вакансии
    all_vacancies = conn.delete(dict())


