import random
import httpx

BASE_URL = "http://127.0.0.1:8000"

ERRORS = [
    {
        "name": "ZeroDivisionError",
        "payload": {
            "user_id": "user_div0",
            "feature": "chat",
            "session_id": "sess_div0",
            "message": "trigger_zero_division",
        },
    },
    {
        "name": "KeyError",
        "payload": {
            "user_id": "user_key",
            "feature": "chat",
            "session_id": "sess_key",
            "message": "trigger_key_error",
        },
    },
    {
        "name": "TypeError",
        "payload": {
            "user_id": "user_type",
            "feature": "chat",
            "session_id": "sess_type",
            "message": "trigger_type_error",
        },
    },
]


def main():
    error = random.choice(ERRORS)
    print(f"Injecting: {error['name']}")
    
    with httpx.Client() as client:
        try:
            r = client.post(
                f"{BASE_URL}/chat",
                json=error["payload"],
                timeout=30.0,
            )
            print(f"Response: {r.status_code} - {r.text}")
        except Exception as e:
            print(f"Exception: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
