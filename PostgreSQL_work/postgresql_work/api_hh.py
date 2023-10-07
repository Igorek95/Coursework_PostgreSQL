import pprint

import requests

from PostgreSQL_work.postgresql_work.dbmanager import DBManager
from PostgreSQL_work.postgresql_work.vacancy import Vacancy


class HeadHunterAPI:
    """
    Класс для взаимодействия с API HeadHunter и получения информации о вакансиях компаний.

    Attributes:
        base_url (str): Базовый URL для запросов к API HeadHunter.
    """

    def __init__(self):
        """
        Инициализирует объект HeadHunterAPI и устанавливает базовый URL API HeadHunter.

        """
        self.base_url = "https://api.hh.ru/employers"

    def get_vacancies(self, search_query=''):

        params = {
            "area": 1,
            'per_page': 100,
            'host': 'hh.ru',
            'only_with_vacancies': True
        }
        if search_query:
            params['text'] = search_query
        response = requests.get(self.base_url, params)
        if response.status_code == 200:
            data = response.json()
            response.close()
            data_vacancy = requests.get(data.get('items')[0].get('vacancies_url')).json()
            self.data_vacancies(data_vacancy)

        else:
            print("Ошибка получения данных")
            return []

    @staticmethod
    def data_vacancies(data):
        """
        Обрабатывает данные о вакансиях и создает объекты класса Vacancy.

        Args:
            vacancies (list): Список данных о вакансиях, полученных из API HeadHunter.
            :param data:
        """
        vacancies = data.get("items", [])
        for vacancy in vacancies:
            name_company = vacancy.get('employer').get('name')
            name_job = vacancy.get('name')
            salary_from = (vacancy.get('salary') or {}).get('from', 0)
            salary_to = (vacancy.get('salary') or {}).get('to', 0)
            link = vacancy.get('alternate_url', 'Не указана')
            address = vacancy['area'].get('name')
            Vacancy(name_company, name_job, salary_from, salary_to, link, address)


hh = HeadHunterAPI()
hh.get_vacancies('CoMagic')
# pprint.pprint(Vacancy.data)
db = DBManager('localhost', 'coursework_postgresql', 'postgres', 1234)
db.create_database()
db.add_db()
