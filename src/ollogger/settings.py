from logging import INFO
from typing import Optional, TypeAlias

from oltl import NewOrExistingFilePath, NonEmptyStringMixIn
from oltl.settings import BaseSettings
from pydantic import Field

LoggerLevelT: TypeAlias = int


class LoggerName(NonEmptyStringMixIn):
    """
    Logger name

    >>> from pydantic import TypeAdapter
    >>> ta = TypeAdapter(LoggerName)
    >>> ta.validate_python("ollogger")
    LoggerName('ollogger')
    >>> ta.validate_python("")
    Traceback (most recent call last):
     ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for function-after[LoggerName(), function-before[_proc_str(), constrained-str]]
      String should have at least 1 character [type=string_too_short, input_value='', input_type=str]
     ...
    """  # noqa: E501


class LoggerSettings(BaseSettings):
    """
    Logger settings

    name: str = "ollogger"
        Logger name

    level: int = INFO
        Logging level

    file_path: Optional[NewOrExistingPath] = None
        File path to write logs to. Set if you want to write logs to a file.

    verbose: bool = False
        Verbose flag

    >>> LoggerSettings()
    LoggerSettings(config_path=None, name=LoggerName('ollogger'), level=20, file_path=None, verbose=False)
    >>> LoggerSettings(name="custom", level=10, file_path="logs.log", verbose=True)
    LoggerSettings(config_path=None, name=LoggerName('custom'), level=10, file_path=PosixPath('logs.log'), verbose=True)
    """  # noqa: E501

    name: LoggerName = Field(default=LoggerName.from_str("ollogger"))
    level: LoggerLevelT = Field(default=INFO)
    file_path: Optional[NewOrExistingFilePath] = Field(default=None)
    verbose: bool = Field(default=False)
