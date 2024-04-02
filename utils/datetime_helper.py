import datetime


def timestamp_int_2_str(timestamp: int, timestamp_format='%Y-%m-%d %H:%M:%S') -> str:
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    formatted_dt = dt_object.strftime(timestamp_format)
    return formatted_dt
