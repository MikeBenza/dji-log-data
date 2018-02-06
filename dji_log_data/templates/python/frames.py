from enum import Enum
from abc import ABC, abstractmethod
import datetime
import math
import struct


def default_enum_value(enum_cls, value):
    try:
        return enum_cls(value)
    except ValueError:
        return enum_cls._default


class FrameType(Enum):
    UnrecognizedFrame = -1
    {% for frame_data in data.frame_types %}
    {{ frame_data.type }} = {{ frame_data.id }}
    {% endfor %}


class Frame(ABC):
    def __init__(self, body, version):
        super(Frame, self).__init__()
        self.body = body
        self.version = version

    @abstractmethod
    def unpack_fields(self):
        pass

    @abstractmethod
    def load_fields(self):
        pass


class UnrecognizedFrame(Frame):
    def unpack_fields(self):
        pass

    def load_fields(self):
        pass

{% for frame_data in data.frame_types %}

{% include 'python/frame.py' %}

{% endfor %}

TYPE_CLASS_MAP = {
    FrameType.UnrecognizedFrame: UnrecognizedFrame,
    {% for frame_data in data.frame_types %}
    FrameType.{{ frame_data.type }}: {{ frame_data.type }},
    {% endfor %}
}
