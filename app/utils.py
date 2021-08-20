from datetime import datetime

def send_datetime_to_client(dt):
  UTC_OFFSET_TIMEDELTA = datetime.now() - datetime.utcnow()
  if dt and isinstance(dt, datetime):
    return (dt + UTC_OFFSET_TIMEDELTA).strftime("%d.%m.%y %H:%M:%S")
  return None
