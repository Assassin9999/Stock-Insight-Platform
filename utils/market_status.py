from datetime import datetime, time
from zoneinfo import ZoneInfo


def get_market_status(history):
    eastern = ZoneInfo("America/New_York")
    now = datetime.now(eastern)

    latest_timestamp = history.index[-1]
    try:
        latest_timestamp = latest_timestamp.tz_convert(eastern)
    except Exception:
        try:
            latest_timestamp = latest_timestamp.tz_localize(eastern)
        except Exception:
            pass

    is_weekday = now.weekday() < 5
    is_regular_hours = time(9, 30) <= now.time() <= time(16, 0)
    is_open = is_weekday and is_regular_hours

    return {
        "status": "Market Open" if is_open else "Market Closed / After Hours",
        "status_type": "open" if is_open else "closed",
        "current_time": now.strftime("%B %d, %Y %I:%M:%S %p %Z"),
        "latest_data_time": latest_timestamp.strftime("%B %d, %Y %I:%M:%S %p %Z"),
    }
