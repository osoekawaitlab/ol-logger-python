from logging import FileHandler, Formatter, Logger, StreamHandler, getLogger
from pathlib import Path
from typing import Any

from json_log_formatter import JSONFormatter, VerboseJSONFormatter, _json_serializable

from .settings import LoggerSettings

LoggerLevelT = int


class AsciiJSONFormatter(JSONFormatter):
    def to_json(self, record: Any) -> str:
        try:
            return self.json_lib.dumps(record, default=_json_serializable, ensure_ascii=False)
        except (TypeError, ValueError, OverflowError):
            try:
                return self.json_lib.dumps(record, ensure_ascii=False)
            except (TypeError, ValueError, OverflowError):
                return "{}"


class VerboseAsciiJSONFormatter(VerboseJSONFormatter, AsciiJSONFormatter):
    pass


def _create_formatter(verbose: bool) -> Formatter:
    """
    Create a formatter for a logger.

    :param verbose: Verbose flag
    :return: Formatter

    """
    if verbose:
        return VerboseAsciiJSONFormatter()
    return AsciiJSONFormatter()


def get_logger(settings: LoggerSettings) -> Logger:
    """
    Get a logger with the given settings.

    :param settings: Logger settings
    :return: Logger

    """
    logger = getLogger(str(settings.name))
    logger.setLevel(level=settings.level)
    formatter = _create_formatter(verbose=settings.verbose)

    stream_handler = None
    file_handler = None
    for handler in logger.handlers:
        if isinstance(handler, FileHandler):
            file_handler = handler
            continue
        if isinstance(handler, StreamHandler):
            stream_handler = handler
            continue
    if stream_handler is not None and stream_handler.stream.closed:
        logger.removeHandler(stream_handler)
        stream_handler = None
    if stream_handler is None:
        stream_handler = StreamHandler()
        logger.addHandler(stream_handler)
    else:
        if stream_handler.stream.closed:
            stream_handler
    if settings.file_path is None:
        if file_handler is not None:
            logger.removeHandler(file_handler)
            file_handler.close()
            file_handler = None
    else:
        if file_handler is None:
            file_handler = FileHandler(filename=settings.file_path)
            logger.addHandler(file_handler)
        else:
            if Path(file_handler.baseFilename) != settings.file_path:
                logger.removeHandler(file_handler)
                file_handler.close()
                file_handler = FileHandler(filename=settings.file_path)
                logger.addHandler(file_handler)
    stream_handler.setLevel(level=settings.level)
    stream_handler.setFormatter(formatter)
    if file_handler is not None:
        file_handler.setLevel(level=settings.level)
        file_handler.setFormatter(formatter)
    return logger
