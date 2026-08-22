"""Manual end-to-end smoke test for a running Flowlog API instance.

Start the API and configure a reachable database before running this script.
This is intentionally kept outside pytest because it depends on external
services and mutates application data.
"""

import uuid

import requests

BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT_SECONDS = 5


def check_response(response):
    try:
        print(response.status_code, response.json())
    except requests.exceptions.JSONDecodeError:
        print(f"Response parsing failed: {response.status_code} {response.text}")


def request(method, path, **kwargs):
    try:
        response = requests.request(
            method,
            f"{BASE_URL}{path}",
            timeout=REQUEST_TIMEOUT_SECONDS,
            **kwargs,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"{method} {path} request failed: {exc}") from exc

    check_response(response)
    if not response.ok:
        raise RuntimeError(f"{method} {path} failed with status {response.status_code}")

    return response


def main():
    run_id = uuid.uuid4().hex[:8]

    response = request(
        "POST",
        "/users/",
        json={
            "name": "Smoke Test User",
            "email": f"flowlog-smoke-{run_id}@example.com",
        },
    )
    user_id = response.json()["id"]

    response = request(
        "POST",
        "/activity-types/",
        json={"name": f"exercise-smoke-{run_id}"},
    )
    activity_type_id = response.json()["id"]

    for payload in (
        {"user_id": user_id, "emotion": "happy"},
        {"user_id": user_id, "free_text": "요즘 기분이 뭔가 우울하고 복잡해"},
    ):
        request("POST", "/emotions/", json=payload)

    request(
        "POST",
        "/activities/",
        json={
            "user_id": user_id,
            "activity_type_id": activity_type_id,
            "description": "Morning run",
        },
    )

    request(
        "POST",
        "/flow-curve/",
        json={"user_id": user_id, "time_spent": 1.5, "satisfaction": 4.5},
    )

    request("GET", "/users/")


if __name__ == "__main__":
    main()
