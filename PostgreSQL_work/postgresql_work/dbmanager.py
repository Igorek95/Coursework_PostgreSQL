from tabulate import tabulate
import psycopg2

from PostgreSQL_work.postgresql_work.vacancy import Vacancy


class DBManager:
    def __init__(self, host: str, database: str, user: str, password: int):
        """
        Инициализирует объект DBManager для работы с базой данных.

        :param host: Хост базы данных PostgreSQL.
        :param database: Имя базы данных.
        :param user: Имя пользователя для доступа к базе данных.
        :param password: Пароль для доступа к базе данных.
        """
        self.host = host
        self.database = database
        self.user = user
        self._password = password

    def create_database(self):
        """
        Создает новую базу данных и необходимые таблицы (company и vacancies).
        """
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
                        company_name varchar(70) NOT NULL,
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
                        name_job varchar(100) NOT NULL,
                        avr_salary int,
                        link_vacancy varchar(50),
                        address varchar(100),
                        company_id integer REFERENCES company(id_company) NOT NULL
                    )
                """)

                conn.commit()
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            conn.close()

    def add_db(self):
        """
        Добавляет данные о вакансиях в базу данных.
        """
        try:
            data_vacancies = [(v.name_company, v.name_job, v.avr_salary, v.link, v.address) for v in
                              Vacancy.data]

            # Подключаемся к базе данных
            with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                  password=self._password) as conn:
                with conn.cursor() as cur:
                    for vacancy in data_vacancies:
                        # Проверяем, существует ли компания с таким именем
                        cur.execute("SELECT id_company FROM company WHERE company_name = %s", (vacancy[0],))
                        company_id = cur.fetchone()

                        if company_id:
                            company_id = company_id[0]
                            # Обновляем количество вакансий у существующей компании
                            cur.execute("UPDATE company SET count_vacancy = count_vacancy + 1 WHERE id_company = %s",
                                        (company_id,))
                        else:
                            # Если компании нет, создаем новую и получаем ее ID
                            cur.execute(
                                "INSERT INTO company (company_name, count_vacancy) VALUES (%s, 1) RETURNING id_company",
                                (vacancy[0],))
                            company_id = cur.fetchone()[0]

                        # Создаем строку SQL для вставки данных о вакансии
                        vacancies_sql = ('INSERT INTO vacancies (company_id, name_job, avr_salary, link_vacancy, '
                                         'address) VALUES (%s, %s, %s, %s, %s)')
                        vacancies_data = (company_id, vacancy[1], vacancy[2], vacancy[3], vacancy[4])

                        # Вставляем данные о вакансии в базу данных
                        cur.execute(vacancies_sql, vacancies_data)

        except Exception as e:
            print(f"Ошибка при добавлении данных: {e}")
        finally:
            conn.close()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        try:
            # Подключаемся к базе данных
            with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                  password=self._password) as conn:
                with conn.cursor() as cur:
                    # Выполняем SQL-запрос, чтобы получить данные о вакансиях с названием компании, названием
                    # вакансии, зарплатой и ссылкой на вакансию
                    cur.execute("""
                        SELECT company_name, v.name_job, v.avr_salary, v.link_vacancy
                        FROM company 
                        INNER JOIN vacancies v ON company.id_company = v.company_id;
                    """)

                    # Извлекаем все строки результата
                    vacancies_data = cur.fetchall()

                    # Если есть результаты, выведите их в виде таблицы
                    if vacancies_data:
                        headers = ["Company Name", "Job Name", "Average Salary", "Link to Vacancy"]
                        print(tabulate(vacancies_data, headers, tablefmt="pretty"))
                    else:
                        print("Нет доступных данных о вакансиях.")

                    return vacancies_data

        except Exception as e:
            print(f"Ошибка при получении данных о вакансиях: {e}")
            return []

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.

        :return: Средняя зарплата по вакансиям.
        """
        try:
            # Подключаемся к базе данных
            with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                  password=self._password) as conn:
                with conn.cursor() as cur:
                    # Выполняем SQL-запрос для получения средней зарплаты по вакансиям
                    cur.execute("SELECT AVG(avr_salary) FROM vacancies")

                    # Извлекаем результат запроса
                    avg_salary = cur.fetchone()[0]

                    # Выводим результат
                    print(f"Средняя зарплата по вакансиям: {avg_salary:.2f} рублей")

                    return avg_salary

        except Exception as e:
            print(f"Ошибка при получении средней зарплаты: {e}")
            return None

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        try:
            # Подключаемся к базе данных
            with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                  password=self._password) as conn:
                with conn.cursor() as cur:
                    # Выполняем SQL-запрос для получения всех вакансий с зарплатой выше средней
                    cur.execute("SELECT company_name, name_job, avr_salary, link_vacancy FROM vacancies "
                                "INNER JOIN company ON vacancies.company_id = company.id_company "
                                "WHERE avr_salary > (SELECT AVG(avr_salary) FROM vacancies)")

                    # Извлекаем все строки результата
                    vacancies_data = cur.fetchall()

                    # Если есть результаты, выведите их в виде таблицы
                    if vacancies_data:
                        headers = ["Company Name", "Job Name", "Average Salary", "Link to Vacancy"]
                        print(tabulate(vacancies_data, headers, tablefmt="pretty"))
                    else:
                        print("Нет доступных данных о вакансиях с зарплатой выше средней.")

                    return vacancies_data

        except Exception as e:
            print(f"Ошибка при получении данных о вакансиях с высокой зарплатой: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.

        :param keyword: Ключевые слова для поиска вакансий.
        """
        try:
            # Подключаемся к базе данных
            with psycopg2.connect(host=self.host, database=self.database, user=self.user,
                                  password=self._password) as conn:
                with conn.cursor() as cur:
                    # Выполняем SQL-запрос для получения вакансий с указанным ключевым словом в названии
                    cur.execute("SELECT company_name, name_job, avr_salary, link_vacancy FROM vacancies "
                                "INNER JOIN company ON vacancies.company_id = company.id_company "
                                "WHERE name_job ILIKE %s", ('%' + keyword + '%',))

                    # Извлекаем все строки результата
                    vacancies_data = cur.fetchall()

                    # Если есть результаты, выведите их в виде таблицы
                    if vacancies_data:
                        headers = ["Company Name", "Job Name", "Average Salary", "Link to Vacancy"]
                        print(tabulate(vacancies_data, headers, tablefmt="pretty"))
                    else:
                        print(f"Нет доступных данных о вакансиях с ключевым словом '{keyword}'.")

                    return vacancies_data

        except Exception as e:
            print(f"Ошибка при получении данных о вакансиях с ключевым словом: {e}")
            return []
