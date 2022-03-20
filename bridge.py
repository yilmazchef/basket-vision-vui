import requests

api_url = "http://localhost:8080/api/v1/basket"

response = requests.get(api_url)

print(response.json())
print(response.status_code)
