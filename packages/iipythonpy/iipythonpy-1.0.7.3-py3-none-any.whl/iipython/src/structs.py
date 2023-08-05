# Copyright 2021 iiPython

# Modules
import json
import secrets
from typing import Any
from datetime import datetime

class Dictionary(object):
    def __init__(self, data: dict = {}, default: Any = None) -> None:
        self.data = data
        self.default = None

    def __repr__(self, indent: int = 2) -> str:
        return str(self.data)

    def __getitem__(self, name: str) -> Any:
        return self.data[name]

    def __setitem__(self, name: str, value: Any) -> None:
        self.data[name] = value

    def __delitem__(self, name: str) -> Any:
        _d = self.data[name]
        del self.data[name]
        return _d

    def add(self, key: Any) -> None:
        self.fastAppend({key: self.default})

    def copy(self) -> dict:
        return self.data.copy()

    def dump(self, *args, **kwargs) -> str:
        return json.dumps(self.data, *args, **kwargs)

    def erase(self) -> dict:
        _d = self.data
        self.data = {}
        return _d

    def setdefault(self, default: Any) -> None:
        self.default = default

    def getKeysByValue(self, value: Any) -> Any:
        return [key for key in self.data if self.data[key] == value]

    def fastAppend(self, data: dict) -> None:
        self.data = self.data | data

class Timer(object):
    def __init__(self) -> None:
        self.tids = {}

    def start(self) -> str:
        tid = secrets.token_hex(16)
        self.tids[tid] = datetime.now()
        return tid

    def end(self, tid: str) -> datetime:
        if tid not in self.tids:
            raise KeyError("no such timer: {}".format(tid))

        start = self.tids[tid]
        del self.tids[tid]

        return datetime.now() - start

dict = Dictionary
timer = Timer()
