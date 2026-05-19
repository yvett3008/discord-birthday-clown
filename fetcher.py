import os
from dotenv import load_dotenv

import requests
from icalendar import Calendar
from datetime import datetime

load_dotenv()
calendar_url = os.getenv("CALENDAR_URL")

def get_birthdays():
    """Fetch birthdays from a .cal file

    Returns:
        birthdays: array of birthdays
    """
    response = requests.get(calendar_url)
    calendar = Calendar.from_ical(response.text)
    today = datetime.today().date()
    birthdays = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            event_date = component["DTSTART"].dt
            if event_date.month == today.month and event_date.day == today.day:
                birthdays.append(str(component["SUMMARY"]))
    return birthdays
