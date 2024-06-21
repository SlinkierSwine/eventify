import datetime


def get_tomorrow_date() -> datetime.date:
    return datetime.date.today() + datetime.timedelta(days=1)


def get_yesterday_date() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)
