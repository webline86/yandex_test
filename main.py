import datetime as dt


class Record:
    # Если дата не определена лучше передать специальный объект None
    # он более явно указывает что значение пока не заданно
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Все выражение справа от знака = написано в скобках, без них код
        # будет работать так же. Лучше их удалить. Без них будет легче читать.
        self.date = (
            # Если написать if not date на одной строке код будет легче читать
            # Лучше развернуть выражение, что бы поменять if not на просто if
            # получится: если date, то поставить дату иначе установить now()
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Переменные принято называть с маленькой буквы используя snake case
        # https://ru.wikipedia.org/wiki/Snake_case. Это прописано в pep8
        # Вместо цикла for можно использовать генератор списков, который
        # вернет список amount. Внутри генераторов можно использовать if.
        # Получившийся список можно сложить функцией sum()
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Можно использовать конструкцию +=
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        # Как в примере выше можно заменить цикл на генератор списков
        for record in self.records:
            # Внешние скобки лишние
            # В python использовать конструкцию 0 < days < 7
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Для описания функции используется docstring
    # https://www.python.org/dev/peps/pep-0257/
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Лучше переменным давать названия, которые показывают, что в ней
        # храниться. Тогда код будет легче читать x -> calories_remained
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Скобки лишние
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Аргументы функции пишутся используя snake case
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Много блоков if ... elif. Лучше использовать if ... return
        # Можно сделать приватную функцию, которая будет принимать
        # аргументы сумму и валюту, а возвращать форматированную строку
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Это ошибка, нам не надо вместо суммы возвращать 1.00
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # Лишние скобки
            return (
                # Если сумма < 0 мы тоже возвращаем текст с суммой. Там
                # значение форматируется другим способом. Лучше сделать метод
                # класса, который будет правильно выводить деньги в тексте
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # Если денег нет, остальные проверки можно не выполнять, а вернуть
        # строку сразу. Хорошей идеей было бы написать if ... return в начале
        # функции. Такой подход называется Guard Block
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Код ниже не нужен. Класс и без него унаследует этот метод
    def get_week_stats(self):
        super().get_week_stats()
