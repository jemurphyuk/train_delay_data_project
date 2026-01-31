from datetime import datetime
from dateutil.parser import isoparse

def parse_tfl_datetime(value):
    if value is None:
        return None
    return isoparse(value)

def timestamp():
    return datetime.utcnow().isoformat()