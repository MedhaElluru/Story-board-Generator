import os
import requests

def get_credit_balance() -> int:
    response = requests.get(
        "https://api.dev.runwayml.com/v1/organization",
        headers={
            "Authorization": f"Bearer {os.getenv('RUNWAYML_API_SECRET')}",
            "X-Runway-Version": "2024-11-06",
        },
    )
    data = response.json()
    return data["creditBalance"]