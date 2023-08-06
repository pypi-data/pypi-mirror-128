from datetime import timedelta

from django.conf import settings
from django.utils.timezone import is_aware, make_aware, is_naive, make_naive


def fix_timezone(value, timezone=None, is_dst=None):
    if settings.USE_TZ:
        if not is_aware(value):
            return make_aware(value, timezone=timezone, is_dst=is_dst)
    elif not is_naive(value):
        return make_naive(value, timezone=timezone)
    return value


def get_weekdays_between(start, end):
    dt = start

    dates = []

    while dt <= end:

        weekday = dt.isoweekday()
        if weekday > 5:
            dt += timedelta(days=8 - weekday)

        dates.append(dt)

        dt += timedelta(days=1)

    return dates
