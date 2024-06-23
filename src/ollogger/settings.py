from logging import INFO
from typing import Optional, TypeAlias

from oltl import NewOrExistingFilePath
from oltl.settings import BaseSettings
from pydantic import Field

LoggerLevelT: TypeAlias = int


class LoggerSettings(BaseSettings):
    """
    Logger settings

    level: int = INFO
        Logging level

    file_path: Optional[NewOrExistingPath] = None
        File path to write logs to. Set if you want to write logs to a file.

    verbose: bool = False
        Verbose flag

    >>> LoggerSettings()
    LoggerSettings(level=20, file_path=None, verbose=False)
    >>> LoggerSettings(level=10, file_path="logs.log", verbose=True)
    LoggerSettings(level=10, file_path=PosixPath('logs.log'), verbose=True)
    """  # noqa: E501

    level: LoggerLevelT = Field(default=INFO)
    file_path: Optional[NewOrExistingFilePath] = Field(default=None)
    verbose: bool = Field(default=False)
