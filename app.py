import os
import requests
import time

def get_spin_result(btoken):
    headers = {
        "user-agent": "Dart/3.1 (dart:io)",
        "content-type": "application/json",
        "versionapp": "2008",
        "x-lang-mobile": "en",
        "x-tenantid": "tn",
        "x-lang": "en",
        "authorization": btoken
    }
    base_url = "https://krakend-bff.maxit.orange.tn/luckwheel"
    with requests.session() as s:
        response = s.post(f"{base_url}/params", headers=headers, json={})
        result = response.json()

    # Handle max attempts error
    if "code" in result and result["code"] == "5000":
        print(result["message"])
        return None

    token = result["token"]
    rewards = result["segmentValuesArray"]
    destinations = result["spinDestinationArray"]

    # Print all spin results
    for spin_index in destinations:
        reward_text = rewards[spin_index - 1]["resultText"]
        print(reward_text)

    # Filter rewards
    for idx, spin_index in enumerate(destinations):
        reward = rewards[spin_index - 1]
        if reward["resultText"] not in {"100Mo", "200Mo", "300Mo", "Perdu"}:
            print("You won a gift:", reward["resultText"])
            claim_data = {
                "token": token,
                "value": reward["resultText"],
                "spinNumber": idx + 1
            }
            with requests.session() as s:
                claim_response = s.post(f"{base_url}/update", headers=headers, json=claim_data, timeout=60).json()
            print(claim_response)
            return True

    return False


while True:
    token = "Bearer " + os.getenv("TOKEN")
    result = get_spin_result(token)
    if result is None:  # Exit on max attempts error
        break
    if result:  # Exit on successful claim
        print("Gift claimed successfully!")
        break
    time.sleep(5)
