from typing import Any

import humps
import requests


class SwitchBotClient:

    API_ROOT = 'https://api.switch-bot.com/v1.0'

    def __init__(self, token: str) -> None:
        self.session = requests.Session()
        self.session.headers['Authorization'] = token

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f'{self.API_ROOT}/{path}'
        response = self.session.request(method, url, **kwargs)

        # Raise an exception for non-successful status codes.
        response.raise_for_status()

        json_response = humps.decamelize(response.json())
        status_code = json_response['status_code']

        if status_code != 100:
            raise RuntimeError(
                f'The SwitchBot API returned an unsuccessful status code {status_code}:'
                f'{json_response["message"]}')

        return json_response

    def get(self, path: str, **kwargs) -> Any:
        return self.request('GET', path, **kwargs)

    def post(self, path: str, **kwargs) -> Any:
        return self.request('POST', path, **kwargs)

    def put(self, path: str, **kwargs) -> Any:
        return self.request('PUT', path, **kwargs)

    def delete(self, path: str, **kwargs) -> Any:
        return self.request('DELETE', path, **kwargs)
