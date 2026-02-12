import requests
import time
import re
import certifi
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MAILSAC_API_KEY = "k_obajR8EYFTeBm3HR0LwhT3fS7PbdcfF5y324ylmGz"  # Replace with your key
createdaccount = createaccount()
INBOX = "stagestack123987666@mailsac.com"   # Replace with the inbox you watch

def get_latest_email(inbox, api_key, wait_seconds=120, poll_interval=5):
    """
    Polls Mailsac and returns the newest email content (read OR unread).
    """
    headers = {"Mailsac-Key": api_key}
    list_url = f"https://mailsac.com/api/addresses/{inbox}/messages"

    end_time = time.time() + wait_seconds
    while time.time() < end_time:
        resp = requests.get(list_url, headers=headers, verify=False)
        resp.raise_for_status()
        messages = resp.json()

        if messages:
            print("✅ Messages found")

            # Newest message is first (Mailsac sorts newest first)
            newest = messages[0]
            message_id = newest["_id"]

            # Fetch full email body
            body_url = f"https://mailsac.com/api/text/{inbox}/{message_id}"
            body_resp = requests.get(body_url, headers=headers, verify=False)
            body_resp.raise_for_status()

            return body_resp.text

        time.sleep(poll_interval)

    return None


def extract_otp(email_body, regex_pattern=r"\b\d{4,8}\b"):
    """
    Extract OTP from email body using regex.
    """
    match = re.search(regex_pattern, email_body)
    if match:
        return match.group(0)
    return None


if __name__ == "__main__":

    email_body = get_latest_email(INBOX, MAILSAC_API_KEY)

    if not email_body:
        print("❌ No email received within timeout.")
    else:
        otp = extract_otp(email_body)
        if otp:
            print("✅ OTP found:", otp)
        else:
            print("⚠️ OTP not found in email content.")