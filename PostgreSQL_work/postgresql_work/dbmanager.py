from typing import List, Any

import psycopg2

from PostgreSQL_work.postgresql_work.vacancy import Vacancy


class DBManager:
    @staticmethod
    def add_db(name_table):
        try:
            data_tuple = [(v.name_company, v.name_job, v.salary_from, v.salary_to, v.link, v.address) for v in Vacancy.data]

            # Подключаемся к базе данных
            with psycopg2.connect(host='localhost', database='coursework_PostgreSQL', user='postgres', password='1234') as conn:
                with conn.cursor() as cur:
                    # Создаем строку SQL для вставки данных
                    columns = ', '.join(data_tuple)
                    placeholders = ', '.join(['%s'] * len(data_tuple))
                    sql = f'INSERT INTO {name_table} ({columns}) VALUES ({placeholders})'

                    # Вставляем данные в базу данных
                    cur.executemany(sql, data_tuple)

        finally:
            # Закрываем соединение с базой данных
            conn.close()

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки
        на вакансию.
        """
        pass

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        pass

    def get_vacancies_with_keyword(self):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        pass
