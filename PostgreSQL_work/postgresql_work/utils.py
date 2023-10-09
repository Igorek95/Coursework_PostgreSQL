from PostgreSQL_work.postgresql_work.dbmanager import DBManager
from PostgreSQL_work.postgresql_work.api_hh import HeadHunterAPI
from PostgreSQL_work.postgresql_work.vacancy import Vacancy


def greet_user():
    print("Добро пожаловать в программу для работы с вакансиями компаний!")
    print("Эта программа поможет вам получить информацию о вакансиях интересующих вас компаний.")
    print("Вы можете запросить данные о вакансиях и выполнить различные операции с ними.")


def get_interesting_companies():
    companies = []
    print("""Пожалуйста, укажите интересующие вас компании (минимум 1, максимум 10)
Если выбрали менее 10, напишите 'стоп'
    """)

    while True:
        company_name = input(f"Введите название компании (или 'стоп' для завершения): ")
        if len(companies) > 10:
            break
        else:
            if company_name.lower() == 'стоп':
                break
            elif company_name:
                companies.append(company_name)
            else:
                print("Вы не указали ни одной компании. Пожалуйста, укажите хотя бы одну.")

    return companies


def print_menu():
    print("\nВыберите действие:")
    print("1. Получить данные о вакансиях интересующих вас компаний.")
    print("2. Получить среднюю зарплату по всем вакансиям.")
    print("3. Получить список вакансий с зарплатой выше средней.")
    print("4. Получить список вакансий с ключевым словом в названии.")
    print("5. Завершить программу.")


def get_user_choice():
    while True:
        choice = input("Введите номер действия: ")
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        else:
            print("Некорректный выбор. Попробуйте снова.")


def handle_user_choice(choice, db_manager):
    if choice == "1":
        db_manager.get_all_vacancies()
    elif choice == "2":
        db_manager.get_avg_salary()
    elif choice == "3":
        db_manager.get_vacancies_with_higher_salary()
    elif choice == "4":
        keyword = input("Введите ключевое слово для поиска в названиях вакансий: ")
        db_manager.get_vacancies_with_keyword(keyword)
    elif choice == "5":
        print("Программа завершена.")
        exit()


def run_utils():
    greet_user()

    # Получаем список интересующих компаний от пользователя
    companies = get_interesting_companies()

    # Создаем объект HeadHunterAPI для взаимодействия с API HeadHunter
    headhunter_api = HeadHunterAPI()

    # Создаем объект DBManager для работы с базой данных
    db_manager = DBManager('localhost', 'coursework_postgresql', 'postgres', 1234)

    db_manager.create_database()
    if companies:
        for company in companies:
            headhunter_api.get_vacancies(company)
            db_manager.add_db()
            Vacancy.clean_data()
        while True:
            print_menu()
            choice = get_user_choice()
            handle_user_choice(choice, db_manager)
    else:
        exit
