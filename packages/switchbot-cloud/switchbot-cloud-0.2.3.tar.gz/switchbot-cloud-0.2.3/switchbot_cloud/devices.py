from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, TypeVar, cast

import humps

if TYPE_CHECKING:
    from switchbot_cloud.client import SwitchBotClient


T = TypeVar("T")


def _all_annotations(cls: type) -> Dict[str, Any]:
    annotations = cast(Dict[str, Any], getattr(cls, "__annotations__", {}))
    for base_cls in cls.__bases__:
        annotations = {**annotations, **_all_annotations(base_cls)}
    return annotations


def _map_to_annotations(obj: T, data: Dict[str, Any]) -> T:
    for attr, value in data.items():
        if attr not in _all_annotations(obj.__class__):
            continue
        setattr(obj, attr, value)
    return obj


class Device:
    """A base class for modeling common device attributes."""

    client: "SwitchBotClient"
    device_id: str
    device_name: str
    device_type: str
    hub_device_id: str

    def __init__(
        self,
        client: "SwitchBotClient",
        **attributes: Any,
    ) -> None:
        self.client = client
        _map_to_annotations(self, attributes)

    def refresh(self) -> None:
        _map_to_annotations(self, self.client.device(**self.__dict__).__dict__)

    def command(self, action: str, parameter: Optional[str] = None) -> None:
        self.client.post(
            f"devices/{self.device_id}/commands",
            json=humps.camelize(
                {
                    "command_type": "command",
                    "command": humps.camelize(action),
                    "parameter": "default" if parameter is None else parameter,
                }
            ),
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(device_id={self.device_id})"


class Powerable(Device):

    power: Literal["on", "off"]

    def turn_on(self) -> None:
        self.command(f"turn_on")

    def turn_off(self) -> None:
        self.command(f"turn_off")

    def toggle_power(self) -> None:
        self.turn_on() if self.power == "off" else self.turn_off()


class HubMini(Device):
    pass


class Thermostat:

    temperature: int | float

    @property
    def temperature_fahrenheit(self) -> float:
        return (self.temperature * 9 / 5) + 32


class Hygrometer:

    humidity: int | float


class Bot(Powerable, Device):
    def press(self) -> None:
        self.command("press")


class Plug(Powerable, Device):
    pass


class Curtain(Device):

    calibrate: bool
    group: bool
    master: bool
    moving: bool
    open_direction: Literal["left", "right"]
    slide_position: int

    @property
    def slide_position_rounded(self) -> int:
        return 5 * round(self.slide_position / 5)

    @property
    def is_calibrated(self) -> bool:
        return self.calibrate

    @property
    def is_master(self) -> bool:
        return self.master

    @property
    def is_grouped(self) -> bool:
        return self.group

    @property
    def is_moving(self) -> bool:
        return self.moving

    @property
    def is_open(self) -> bool:
        return self.slide_position_rounded < 10

    @property
    def is_closed(self) -> bool:
        return self.slide_position_rounded > 90

    def set_position(self, position: int) -> None:
        self.command("set_position", f"0,ff,{position}")

    def open(self) -> None:
        self.set_position(0)

    def close(self) -> None:
        self.set_position(100)


class Meter(Thermostat, Hygrometer, Device):
    pass


class MotionSensor(Device):

    move_detected: bool
    brightness: Literal["bright", "dim"]

    @property
    def motion_detected(self) -> bool:
        return self.move_detected


class ContactSensor(Device):

    move_detected: bool
    brightness: Literal["bright", "dim"]
    open_state: Literal["open", "close", "timeOutNotClose"]

    @property
    def motion_detected(self) -> bool:
        return self.move_detected

    @property
    def is_closed(self) -> bool:
        return self.open_state == "close"

    @property
    def is_open(self) -> bool:
        return not self.is_closed


class Humidifier(Powerable, Thermostat, Hygrometer, Device):

    nebulization_efficiency: int | float
    auto: bool
    child_lock: bool
    sound: bool
    lack_water: bool

    @property
    def sound_on(self) -> bool:
        return self.sound

    def set_mode(self, mode: Literal["auto", "101", "102", "103"]) -> None:
        self.command("set_mode", mode)
