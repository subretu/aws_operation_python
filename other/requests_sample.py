import requests

url = "https://www.google.co.jp/search"

# requestsは引数を2つ以上指定する必要あり
params = {
    "q": "日本代表",
}

response = requests.get(url, params=params)

print(response.text)
print(response.headers)
