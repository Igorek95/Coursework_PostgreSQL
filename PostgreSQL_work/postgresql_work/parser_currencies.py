import requests
from bs4 import BeautifulSoup


class CurrencyParser:
    def __init__(self):
        self.base_url = "https://www.cbr.ru"
        self.currency_url = f"{self.base_url}/currency_base/daily/"

    def parse_currency(self):
        try:
            # Отправляем GET-запрос на страницу с курсом валют
            response = requests.get(self.currency_url)

            if response.status_code == 200:
                # Используем BeautifulSoup для парсинга HTML-страницы
                soup = BeautifulSoup(response.text, 'html.parser')

                # Находим таблицу с курсами валют
                table = soup.find("table", {"class": "data"})

                # Извлекаем данные о курсах валют
                currencies = {}
                rows = table.find_all("tr")
                for row in rows[1:]:  # Пропускаем первую строку с заголовками
                    columns = row.find_all("td")
                    if len(columns) >= 5:
                        code = columns[0].text.strip()
                        name = columns[1].text.strip()
                        rate = float(
                            columns[4].text.replace(",", "."))  # Заменяем запятую на точку и преобразуем в число

                        # Извлекаем количество единиц валюты
                        units = int(columns[2].text.strip())  # Преобразуем количество единиц валюты в целое число

                        currencies[code] = {"Name": name, "Rate": rate, "Units": units}

                        # Добавляем аббревиатуры и альтернативные имена валюты
                        alt_names = [name, name.lower()]
                        alt_names.extend(
                            [x.strip() for x in name.split('/')])  # Разбиваем по "/" на альтернативные имена
                        alt_names = list(set(alt_names))  # Убираем дубликаты
                        for alt_name in alt_names:
                            currencies[alt_name] = {"Code": code, "Rate": rate, "Units": units}

                return currencies
            else:
                print("Ошибка получения данных")
                return {}

        except Exception as e:
            print(f"Ошибка при парсинге курса валют: {e}")
            return {}

    def get_exchange_rate(self, currency_code):
        currencies = self.parse_currency()
        if currency_code in currencies:
            return currencies[currency_code]["Rate"]

    def convert_to_rub(self, currency_code, amount):
        exchange_rate = self.get_exchange_rate(currency_code)
        if exchange_rate is not None:
            units = self.parse_currency().get(currency_code, {}).get("Units", 1)
            rub_amount = (amount * exchange_rate) / units
            return rub_amount
