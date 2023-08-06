from typing import Any, Dict, List, Sequence, Union

import json
import humps
import requests

from switchbot_cloud import devices as device_types


class SwitchBotClient(requests.Session):

    API_ROOT = "https://api.switch-bot.com"
    API_VERSION = "v1.0"

    def __init__(self, token: str) -> None:
        super().__init__()

        self.headers["Authorization"] = token
        self.hooks = {"response": [self.decamelize_content]}

    @staticmethod
    def decamelize_content(
        response: requests.Response, *args: Any, **kwargs: Any
    ) -> requests.Response:
        response._content = json.dumps(humps.decamelize(response.json())).encode()
        return response

    def request(
        self, method: str, url: Union[str, bytes], *args: Any, **kwargs: Any
    ) -> requests.Response:
        url = "/".join([self.API_ROOT, self.API_VERSION, str(url).strip("/")])
        response = super().request(method, url, **kwargs)

        # Raise an exception for non-successful status codes.
        response.raise_for_status()

        json_response = response.json()

        # Check the returned status_code in the payload and raise an error for
        # anything other than 100 (success).
        status_code = json_response["status_code"]
        if status_code != 100:
            raise RuntimeError(
                f"The SwitchBot API returned an unsuccessful status code {status_code}:"
                f'{json_response["message"]}'
            )

        return response

    def devices(
        self,
        ignore_uncalibrated: bool = False,
        ignore_grouped: bool = False,
    ) -> Sequence[device_types.Device]:
        device_list: List[device_types.Device] = []
        for device in self.get("devices").json()["body"]["device_list"]:
            print(device)
            calibrated = device.get("calibrate", True)
            master = device.get("master", True)
            grouped = device.get("group", False) and not master

            if ignore_uncalibrated and not calibrated:
                continue

            if ignore_grouped and grouped:
                continue

            device_list.append(self.device(**device))

        return device_list

    def device(self, device_id: str, **device_attrs: Any) -> device_types.Device:
        if not device_attrs:
            device_attrs = next(
                device
                for device in self.get("devices").json()["body"]["device_list"]
                if device["device_id"] == device_id
            )
        status_attrs = self.get(f"devices/{device_id}/status").json()["body"]

        device_cls = device_types.Device
        try:
            device_member = getattr(
                device_types, device_attrs["device_type"].replace(" ", "")
            )
            if issubclass(device_member, device_types.Device):
                device_cls = device_member
        except (TypeError, AttributeError):
            pass

        return device_cls(**{"client": self, 'device_id': device_id, **device_attrs, **status_attrs})
