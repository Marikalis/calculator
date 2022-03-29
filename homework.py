import datetime as dt


class Calculator:
    PERIOD = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record_class):
        self.records.append(record_class)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(
            record.amount
            for record in self.records
            if record.date == today
        )

    def get_week_stats(self):
        today = dt.date.today()
        last_week = today - self.PERIOD
        return sum(
            record.amount
            for record in self.records
            if last_week < record.date <= today
        )


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


class CaloriesCalculator(Calculator):
    AVAILABLE = ('Сегодня можно съесть что-нибудь ещё, но с общей '
                 'калорийностью не более {about_remainder} кКал')
    UNAVAILABLE = 'Хватит есть!'

    def get_calories_remained(self):
        remainder = self.limit - self.get_today_stats()
        if remainder > 0:
            return (self.AVAILABLE.format(about_remainder=remainder))
        return self.UNAVAILABLE


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    CURRENCYS = {
        'rub': ('руб', 1.00),
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE)
    }
    NONE_CURRENCY = ('Валюта {currency} не поддерживается. '
                     'Поддерживаемые валюты: {currencys}')
    LACK_MONEY = 'Денег нет, держись'
    HAVE_MONEY = 'На сегодня осталось {remainder} {currency}'
    DEBT_MONEY = ('Денег нет, держись: твой долг - {remainder} '
                  '{currency}')

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCYS:
            raise ValueError(
                self.NONE_CURRENCY.format(
                    currency=currency,
                    currencys=self.CURRENCYS.keys()
                )
            )
        remainder = self.limit - self.get_today_stats()
        if remainder == 0:
            return self.LACK_MONEY
        name, rate = self.CURRENCYS[currency]
        remainder_change = remainder / rate
        rounded_remainder_change = round(remainder_change, 2)
        if remainder > 0:
            return self.HAVE_MONEY.format(
                remainder=rounded_remainder_change,
                currency=name
            )
        return self.DEBT_MONEY.format(
            remainder=abs(rounded_remainder_change),
            currency=name
        )
