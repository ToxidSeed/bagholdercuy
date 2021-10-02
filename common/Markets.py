from pytz import HOUR, timezone
from datetime import datetime, time

def is_intraday():
    eastern = timezone('US/Eastern')
    us_market_datetime = datetime.now(eastern)
    us_open_hour = time(9,30,0)
    us_close_hour = time(16,0,0)

    if us_market_datetime.weekday() in [5,6]:
        return False

    if not (us_market_datetime.time() >=  us_open_hour and 
        us_market_datetime.time() <= us_close_hour):
        return False

    return True

