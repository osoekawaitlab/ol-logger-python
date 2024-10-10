import json
from datetime import datetime
from logging import Formatter, LogRecord
from typing import Any, Callable, Dict, Protocol, Type, Union

class JSONLibProtocol(Protocol):
    def dumps(self, obj: Any, **kwargs: Any) -> str: ...

class JSONFormatter(Formatter):
    json_lib: JSONLibProtocol
    def json_record(
        self, message: str, extra: dict[str, Union[None, bool, int, str, float, datetime]], record: LogRecord
    ) -> dict[str, Union[None, bool, int, str, float, datetime]]: ...

class VerboseJSONFormatter(JSONFormatter): ...

_json_serializable: Callable[[Any], Union[Dict[str, Any], str]]
