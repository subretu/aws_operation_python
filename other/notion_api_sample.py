import requests


url = "https://api.notion.com/v1/pages"

headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Authorization": f"Bearer xxxxxxxxxxxxxx",
}

json_data = {
    "parent": {
        "type": "database_id",
        "database_id": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
    },
    "properties": {
        "title": {"title": [{"text": {"content": "sampleページ"}}]},
    },
    # ページ本文
    "children": [
        {
            "object": "block",
            "heading_2": {"rich_text": [{"text": {"content": "test"}}]},
        },
    ],
}

response = requests.post(url, json=json_data, headers=headers)
print(response.text)
