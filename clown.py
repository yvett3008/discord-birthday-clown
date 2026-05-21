import os
from dotenv import load_dotenv

from fetcher import get_birthdays
import requests
import random

from wishes import wishes_single, wishes_double, wishes_multiple, emojis, gifs

load_dotenv()
ping_role = os.getenv("BIRTHDAY_PING_ROLE")
env = os.getenv("ENV")
webhook = ""
if env == "dev":
    webhook = os.getenv("DEV_WEBHOOK_URL")
elif env == "prod":
    webhook = os.getenv("WEBHOOK_URL")
else:
    print("Careful! ENV is not set yet, defaulting to `dev`")
    webhook = os.getenv("DEV_WEBHOOK_URL")

fetch = get_birthdays()  # { birthdays: ["array", "of", "names"], date}
birthdays = fetch["birthdays"]  # returns an array of people who have a birthday

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

    emoji_str = " ".join(emoji_content)
    requests.post(
        webhook,
        json={
            "content": "test",
            "embeds": [
                {
                    "title": f"{content} {emoji_str}",
                    "description": f"{fetch["date"].strftime("%d %B %Y")}",
                    "color": 0xD5730C,
                    "image": {"url": random.choice(gifs)},
                }
            ],
        },
    )
else:
    print("No one is having a birthday today")
