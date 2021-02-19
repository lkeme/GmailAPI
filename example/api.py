import json

import requests


def test():
    url = 'http://127.0.0.1:5000/fetch_mail'
    data = {
        'email': 'example@gmail.com'
    }
    headers = {
        'Content-type': 'application/json'
    }
    # {'code': 404, 'data': {}, 'msg': 'no_data'}
    response = requests.post(url, headers=headers, json=data).json()
    print(json.dumps(response, sort_keys=True, indent=2,ensure_ascii=False))
    return response


if __name__ == '__main__':
    test()
