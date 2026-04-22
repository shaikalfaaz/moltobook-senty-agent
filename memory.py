import json
import os

MEMORY_FILE = "memory.json"
MAX_MEMORY = 500


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {
            "processed_comments": [],
            "processed_posts": []
        }

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

            # ensure keys exist
            data.setdefault("processed_comments", [])
            data.setdefault("processed_posts", [])

            return data

    except Exception:
        # if file corrupted reset safely
        return {
            "processed_comments": [],
            "processed_posts": []
        }


def save_memory(memory):

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def add_processed_comment(memory, comment_id):

    if comment_id not in memory["processed_comments"]:
        memory["processed_comments"].append(comment_id)

        # keep only latest N
        memory["processed_comments"] = memory["processed_comments"][-MAX_MEMORY:]

        save_memory(memory)


def add_processed_post(memory, post_id):

    if post_id not in memory["processed_posts"]:
        memory["processed_posts"].append(post_id)

        # keep only latest N
        memory["processed_posts"] = memory["processed_posts"][-MAX_MEMORY:]

        save_memory(memory)