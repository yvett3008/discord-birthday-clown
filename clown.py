import os
from dotenv import load_dotenv

from fetcher import get_birthdays
import requests
import random

from wishes import wishes_single, wishes_double, wishes_multiple, emojis, gifs

load_dotenv()
webhook = os.getenv("WEBHOOK_URL")
ping_role = os.getenv("BIRTHDAY_PING_ROLE")

birthdays = get_birthdays() # returns an array of people who have a birthday

if len(birthdays) > 0:
    emoji_content = []

    emoji_content = [random.choice(emojis) for _ in range(random.randint(0, 3))]

    if len(birthdays) == 1:
        content = random.choice(wishes_single).format(nama=birthdays[0])
    elif len(birthdays) == 2:
        # example: "Double the celebration! Happy birthday to {nama[0]} and {nama[1]}!"
        content = random.choice(wishes_double).format(nama=birthdays)
    elif len(birthdays) >= 3:
        # example: "Rame yah. Selamat ulang tahun untuk {multiple_nama}, dan {last_nama}!"
        multiple_nama = ", ".join(birthdays[:-1])
        last_nama = birthdays[-1]
        content = random.choice(wishes_multiple).format(
            multiple_nama=multiple_nama, last_nama=last_nama
        )

    emoji_str = "".join(emoji_content)
    requests.post(webhook, json={"content": f"{ping_role}\n{content} {emoji_str}"})
    requests.post(webhook, json={"content": random.choice(gifs)})
else:
    print("No one is having a birthday today")
