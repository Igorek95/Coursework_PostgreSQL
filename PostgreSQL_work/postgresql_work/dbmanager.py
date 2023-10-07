from typing import List, Any

import psycopg2

from PostgreSQL_work.postgresql_work.vacancy import Vacancy



class DBManager:
    def __init__(self, host: str, database: str, user: str, password: int):
        self.host = host
        self.database = database
        self.user = user
        self._password = password

    def create_database(self):
        try:
            # Подключаемся к базе данных PostgreSQL (по умолчанию "postgres")
            conn = psycopg2.connect(host=self.host, database="north", user=self.user, password=self._password)
            cur = conn.cursor()
            conn.autocommit = True

            cur.execute(f"DROP DATABASE IF EXISTS {self.database}")
            cur.execute(f"CREATE DATABASE {self.database}")

            conn.close()

            # Повторно подключаемся к созданной базе данных
            conn = psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                    password=self._password)

            # Создаем таблицу company
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE company (
                        id_company serial PRIMARY KEY,
                        company_name varchar(30) NOT NULL,
                        count_vacancy int
                    )
                """)

                # Создаем уникальное ограничение на поле company_name
                cur.execute("""
                    ALTER TABLE company
                    ADD CONSTRAINT company_name_unique UNIQUE (company_name);
                """)

            # Создаем таблицу vacancies
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE vacancies (
                        id_vacancy serial PRIMARY KEY,
                        name_job varchar(50) NOT NULL,
                        avr_salary int,
                        link_vacancy varchar(30),
                        address varchar(100),
                        company_id integer REFERENCES company(id_company) NOT NULL
                    )
                """)

                conn.commit()
                conn.close()
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            conn.close()

    def add_db(self):
        try:
            data_vacancies = [(v.name_company, v.name_job, v.avr_salary, v.link, v.address) for v in
                              Vacancy.data]

            # Подключаемся к базе данных
            with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                  password=self._password) as conn:
                with conn.cursor() as cur:
                    for vacancy in data_vacancies:
                        # Создаем строку SQL для вставки информации о компании
                        company_sql = 'INSERT INTO company (company_name, count_vacancy) VALUES (%s, 1) ON CONFLICT (company_name) DO UPDATE SET count_vacancy = company.count_vacancy + 1 RETURNING id_company'
                        company_values = (vacancy[0],)

                        # Вставляем информацию о компании и получаем ID компании
                        cur.execute(company_sql, company_values)
                        company_id = cur.fetchone()[0]

                        # Создаем строку SQL для вставки данных о вакансии
                        vacancies_sql = 'INSERT INTO vacancies (company_id, name_job, avr_salary, link_vacancy, address) VALUES (%s, %s, %s, %s, %s)'
                        vacancies_data = (company_id, vacancy[1], vacancy[2], vacancy[3], vacancy[4])

                        # Вставляем данные о вакансии в базу данных
                        cur.execute(vacancies_sql, vacancies_data)

        except Exception as e:
            print(f"Ошибка при добавлении данных: {e}")

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
