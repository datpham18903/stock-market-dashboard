from datetime import datetime, time, timedelta
import pytz

def get_market_close_string():
    est_tz = pytz.timezone("US/Eastern")
    current_time = datetime.now(est_tz)
    current_date = current_time.date()

    current_date = get_last_business_day(current_date)
    market_open, market_close = get_market_hours(current_date, est_tz)

    if market_open <= current_time <= market_close:
        return f"As of {current_time.strftime('%I:%M:%S %p')} EST"

    if current_time < market_open:
        prev_date = get_last_business_day(current_date - timedelta(days=1))
        market_close = est_tz.localize(datetime.combine(prev_date, time(16, 0)))

    return f"At close: {market_close.strftime('%B %d at %I:%M:%S %p')} EST"

def get_last_business_day(date):
    while date.weekday() in [5, 6]:
        date -= timedelta(days=1)
    return date


def get_market_hours(date, timezone):
    market_open = timezone.localize(datetime.combine(date, time(9, 30)))
    market_close = timezone.localize(datetime.combine(date, time(16, 0)))
    return market_open, market_close