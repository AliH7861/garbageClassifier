from datetime import datetime
import pytz

# Toronto timezone
toronto_tz = pytz.timezone("America/Toronto")

timeNow = datetime.now(toronto_tz)

# Obtain current time
current_time = timeNow


dt_simple = current_time.replace(microsecond=0, tzinfo=None)
print(dt_simple)

# Obtain current date (as a date object)
current_date = current_time.date()

# If you want it as a string (YYYY-MM-DD):
current_date_str = current_date.isoformat()
# OR
current_date_str = str(current_date)

print("Current Time:", current_time)
print("Current Date (date object):", current_date)
print("Current Date (string):", current_date_str)


 