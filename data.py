import json


def save_data(data):
    with open('user_data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
