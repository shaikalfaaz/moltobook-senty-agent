import time
import random
import sys

from moltbook_client import (
    heartbeat,
    get_comments,
    reply_to_comment,
    verify,
    get_feed,
    comment_on_post
)

from llm_engine import (
    generate_reply,
    generate_post_comment,
    solve_verification
)

from rate_limiter import can_interact, record_interaction

from memory import (
    load_memory,
    add_processed_comment,
    add_processed_post
)

from config import AGENT_NAME

memory = load_memory()


def handle_verification(response):

    verification = response.get("comment", {}).get("verification")

    if not verification:
        return True

    challenge = verification["challenge_text"]
    code = verification["verification_code"]

    print("Verification challenge:", challenge)
    print("Verification code:", code)

    answer = solve_verification(challenge)

    if not answer:
        print("Verification solver failed")
        return False

    print("Submitting answer:", answer)

    result = verify(code, answer)

    return result


def process_notifications(post):

    interacted = False

    post_id = post["post_id"]
    post_title = post["post_title"]

    comments_data = get_comments(post_id)
    comments = comments_data.get("comments", [])

    for comment in comments:

        comment_id = comment["id"]

        if comment_id in memory["processed_comments"]:
            continue
        if comment.get("is_spam"):
            continue

        author = comment["author"]["name"]
        if author == AGENT_NAME:
            continue

        text = comment["content"]

        if not can_interact():
            print("Rate limit reached")
            return interacted

        reply = generate_reply(post_title, text)

        print("Reply:", reply)

        response = reply_to_comment(post_id, comment_id, reply)
        add_processed_comment(memory, comment_id)

        success = handle_verification(response)

        if not success:
            print("Verification failed skipping interaction")
            sys.exit(1)

        record_interaction()
        interacted = True

        time.sleep(20)

    return interacted


def explore_feed():

    print("Exploring feed...")
    feed = get_feed(25)
    posts = feed.get("posts", [])
    print("Fetched posts:", len(posts))

    for post in posts:

        if random.random() > 0.15:
            continue

        post_id = post["id"]

        if post_id in memory["processed_posts"]:
            continue

        if not can_interact():
            print("Rate limit reached")
            return

        title = post["title"]
        content = post.get("content", "")

        comment = generate_post_comment(title, content)

        print("Generated comment:", comment)

        response = comment_on_post(post_id, comment)
        add_processed_post(memory, post_id)

        success = handle_verification(response)

        if not success:
            print("Verification failed stopping agent")
            sys.exit(1)

        record_interaction()

        time.sleep(20)


def agent_loop():

    while True:

        print("Heartbeat check...")
        data = heartbeat()

        posts = data.get("activity_on_your_posts", [])
        print("Activity posts:", len(posts))

        interacted = False

        if posts:
            for post in posts:
                if process_notifications(post):
                    interacted = True

        if not interacted:
            explore_feed()

        time.sleep(60)


if __name__ == "__main__":
    agent_loop()