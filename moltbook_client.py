import requests
from config import MOLTBOOK_API_KEY, BASE_URL

headers = {
    "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
    "Content-Type": "application/json"
}


def heartbeat():
    r = requests.get(f"{BASE_URL}/home", headers=headers)
    r.raise_for_status()
    return r.json()


def get_comments(post_id):

    r = requests.get(
        f"{BASE_URL}/posts/{post_id}/comments?sort=new&limit=20",
        headers=headers,
    )

    r.raise_for_status()

    return r.json()


def reply_to_comment(post_id, parent_id, content):

    payload = {
        "content": content,
        "parent_id": parent_id
    }

    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=headers,
        json=payload
    )

    r.raise_for_status()

    return r.json()


def verify(verification_code, answer):

    print("Submitting verification answer:", answer)

    payload = {
        "verification_code": verification_code,
        "answer": answer
    }

    r = requests.post(
        f"{BASE_URL}/verify",
        headers=headers,
        json=payload
    )

    print("VERIFY RESPONSE:", r.status_code, r.text)

    return r.json() if r.status_code == 200 else None

def get_feed(limit=25):
    r = requests.get(
        f"{BASE_URL}/feed?sort=new&limit={limit}",
        headers=headers
    )
    r.raise_for_status()
    return r.json()


def comment_on_post(post_id, content):

    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=headers,
        json={"content": content}
    )

    r.raise_for_status()
    return r.json()