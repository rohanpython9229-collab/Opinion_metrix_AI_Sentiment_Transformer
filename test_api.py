import requests

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={
        "review": "This product is amazing and works perfectly!"
    }
)

print("Status:", response.status_code)
print("Response:", response.json())