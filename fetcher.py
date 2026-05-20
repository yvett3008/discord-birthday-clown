import os
from dotenv import load_dotenv

import requests
from icalendar import Calendar
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()
calendar_url = os.getenv("CALENDAR_URL")
timezone = os.getenv("ZONE_INFO")

def get_birthdays():
    """Fetch birthdays from a .cal file

    Returns:
        birthdays: array of birthdays
    """
    response = requests.get(calendar_url)
    calendar = Calendar.from_ical(response.text)
    today = datetime.now(ZoneInfo(timezone)).date()
    birthdays = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            event_date = component["DTSTART"].dt
            if event_date.month == today.month and event_date.day == today.day:
                birthdays.append(str(component["SUMMARY"]))
    return birthdays
