import datetime
from typing import Optional

import pytz


def get_datetime_for_event(
    date: datetime.date,
    time: str,
    format: str = "%H:%M",
    tz: Optional[pytz.BaseTzInfo] = pytz.UTC,
) -> datetime.datetime:
    dt = datetime.datetime.combine(
        date, datetime.datetime.strptime(time, format).time()
    )

    if tz is not None:
        return tz.localize(dt)

    return dt
