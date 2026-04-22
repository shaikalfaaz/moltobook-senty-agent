from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_post_comment(title, content):

    prompt = f"""
        You are participating in a Moltbook discussion.

        Post title:
        {title}

        Post content:
        {content}

        Write a thoughtful comment that adds value.
        Avoid generic responses.
        Keep it under 3 sentences.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


def generate_reply(post_title, comment_text):

    prompt = f"""
        You are a thoughtful participant on Moltbook.

        Post title:
        {post_title}

        Comment from another user:
        {comment_text}

        Write a natural reply that:
        - adds value to the conversation
        - asks a thoughtful follow-up question if appropriate
        - avoids generic phrases
        - stays under 80 words
        """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

    

def solve_verification(challenge_text):
    clean_stream = "".join(char.lower() for char in challenge_text if char.isalnum() or char.isspace())
    
    prompt = f"""
    Decode and solve the math in this text: "{clean_stream}"
    
    CRITICAL INSTRUCTION: 
    Output ONLY the numerical result. 
    No words. No explanation. No units.
    Format: XX.00
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a cold, robotic calculator. You never speak. You only output numbers in XX.00 format."},
            {"role": "user", "content": prompt}
        ],
        temperature=0 
    )

    # Directly take the string and clean it
    ans_string = response.choices[0].message.content.strip()
    print("LLM raw output:", ans_string)
    
    # Optional: Safety cast to float just to ensure it's a valid number
    try:
        final_ans = f"{float(ans_string):.2f}"
        print(f"Formatted Output: {final_ans}")
        return final_ans
    except ValueError:
        print(f"Error: LLM returned non-numeric value: {ans_string}")
        return None


challenge_text = "A] LoBbS tEr ClAw^ ExErTs~ ThIiR.ty FiV e NoOtOnS| AnD/ iTs AnTeNnAe~ SeNsE- TwElVe NoOtOnS< MoRe, WhAtS} ToTaL^ FoRcE?"


solve_verification(challenge_text)