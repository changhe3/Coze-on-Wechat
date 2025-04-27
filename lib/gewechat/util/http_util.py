import requests
import traceback
import io
from ..util.terminal_printer import print_red, print_yellow

def post_json(base_url, route, token, data):
    headers = {
        'Content-Type': 'application/json'
    }
    if token:
        headers['X-GEWE-TOKEN'] = token

    url = base_url + route

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()

        if result.get('ret') == 200:
            return result
        else:
            raise RuntimeError(response.text)
    except Exception as e:
        print_red(e)
        tb = io.StringIO()
        traceback.print_stack(file=tb)
        print_yellow(tb.getvalue())
        return {
            'ret': 500,
            'error': e,
        }
