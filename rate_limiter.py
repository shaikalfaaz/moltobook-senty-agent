import time
import json
import os

FILE = "interactions.json"
MAX_PER_HOUR = 4


def load():
    if not os.path.exists(FILE):
        return []

    with open(FILE) as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


def can_interact():

    now = time.time()
    data = load()

    data = [t for t in data if now - t < 3600]

    save(data)

    return len(data) < MAX_PER_HOUR


def record_interaction():

    data = load()
    data.append(time.time())
    save(data)