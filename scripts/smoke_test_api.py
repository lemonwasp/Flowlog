"""Manual end-to-end smoke test for a running Flowlog API instance.

Start the API and configure a reachable database before running this script.
This is intentionally kept outside pytest because it depends on external
services and mutates application data.
"""

import requests

BASE_URL = "http://127.0.0.1:8000"


def check_response(response):
    try:
        print(response.status_code, response.json())
    except requests.exceptions.JSONDecodeError:
        print(f"Response parsing failed: {response.status_code} {response.text}")


def main():
    response = requests.post(
        f"{BASE_URL}/users/",
        json={"name": "Smoke Test User", "email": "flowlog-smoke@example.com"},
    )
    check_response(response)

    if response.status_code != 200:
        raise RuntimeError("User creation failed")
    user_id = response.json()["id"]

    response = requests.post(
        f"{BASE_URL}/activity-types/",
        json={"name": "exercise"},
    )
    check_response(response)

    if response.status_code != 200:
        raise RuntimeError("Activity type creation failed")
    activity_type_id = response.json()["id"]

    for payload in (
        {"user_id": user_id, "emotion": "happy"},
        {"user_id": user_id, "free_text": "요즘 기분이 뭔가 우울하고 복잡해"},
    ):
        response = requests.post(f"{BASE_URL}/emotions/", json=payload)
        check_response(response)

    response = requests.post(
        f"{BASE_URL}/activities/",
        json={
            "user_id": user_id,
            "activity_type_id": activity_type_id,
            "description": "Morning run",
        },
    )
    check_response(response)

    response = requests.post(
        f"{BASE_URL}/flow-curve/",
        json={"user_id": user_id, "time_spent": 1.5, "satisfaction": 4.5},
    )
    check_response(response)

    response = requests.get(f"{BASE_URL}/users/")
    check_response(response)


if __name__ == "__main__":
    main()
