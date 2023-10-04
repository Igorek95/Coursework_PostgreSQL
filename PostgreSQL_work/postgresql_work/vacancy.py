
class Vacancy:

    data = []

    def __init__(self, name_company, name_job, salary_from, salary_to,  link, address, responsibilities):
        """
        Инициализирует объект вакансии.

        Args:
            name_company (str) : Название компании.
            name_job (str): Название вакансии.
            salary_from (int): Минимальная зарплата.
            salary_to (int): Максимальная зарплата.
            link (str): Ссылка на вакансию.
            address (str): Место работы.
            responsibilities (str): Описание обязанностей.
        """
        self.name_company = name_company
        self.name_job = name_job
        self.salary_from = salary_from if salary_from else 0
        self.salary_to = salary_to if salary_to else 0
        self.link = link
        self.address = address
        self.responsibilities = responsibilities
        self._avr_salary = self.calc_salary(self.salary_from, self.salary_to)
        Vacancy.data.append(self)

    def __repr__(self):
        return f"""Компания:{self.name_company}
 Должность: {self.name_job}
 Средняя зарплата: {self._avr_salary}
 Адрес: {self.address}
 Условия: {self.responsibilities}
 Ссылка: {self.link}
    """

    @staticmethod
    def calc_salary(salary_min: int, salary_max: int) -> int:
        """
        Вычисляет среднюю зарплату на основе минимальной и максимальной зарплаты.

        Args:
            salary_min (int): Минимальная зарплата.
            salary_max (int): Максимальная зарплата.

        Returns:
            int: Средняя зарплата.
        """
        if salary_min == 0 or salary_min is None:
            return salary_max
        elif salary_max == 0 or salary_max is None:
            return salary_min
        else:
            avr_salary = (salary_min + salary_max) // 2
            return avr_salary

    @property
    def avr_salary(self):
        """
        Свойство, возвращающее среднюю зарплату.

        Returns:
            int: Средняя зарплата.
        """
        return self._avr_salary



    @classmethod
    def clean_data(cls):
        """
        Метод для очистки списка объектов вакансий.
        """
        cls.data.clear()
