import json
import logging
from datetime import datetime, timedelta, timezone
from tempfile import NamedTemporaryFile

from freezegun import freeze_time
from pytest import CaptureFixture

import ollogger


def test_logging_default_settings(capsys: CaptureFixture[str]) -> None:
    logger = ollogger.get_logger(ollogger.LoggerSettings())
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    assert isinstance(logger.handlers[0].formatter, ollogger.core.AsciiJSONFormatter)
    assert logger.handlers[0].level == logging.INFO
    assert logger.name == "ollogger"
    dt = datetime(2021, 1, 1, 12, 0, 0, 587166, tzinfo=timezone.utc)
    with freeze_time(dt):
        logger.info("Hello")
    assert capsys.readouterr().err == '{"message": "Hello", "time": "2021-01-01T12:00:00.587166+00:00"}\n'
    dt += timedelta(seconds=1)
    with freeze_time(dt):
        logger.debug("World")
    assert capsys.readouterr().err == ""
    dt += timedelta(seconds=1)
    with freeze_time(dt):
        logger.warning("こんにちは")
    assert capsys.readouterr().err == '{"message": "こんにちは", "time": "2021-01-01T12:00:02.587166+00:00"}\n'
    dt += timedelta(seconds=1)
    with freeze_time(dt):
        logger.error("世界")
    assert capsys.readouterr().err == '{"message": "世界", "time": "2021-01-01T12:00:03.587166+00:00"}\n'


def test_logging_custom_settings(capsys: CaptureFixture[str]) -> None:
    with NamedTemporaryFile(mode="w+") as file:
        logger = ollogger.get_logger(
            ollogger.LoggerSettings(name="customname", level=logging.WARNING, file_path=file.name, verbose=True)
        )
        assert logger.level == logging.WARNING
        assert len(logger.handlers) == 2
        assert isinstance(logger.handlers[0], logging.StreamHandler)
        assert logger.handlers[0].level == logging.WARNING
        assert logger.name == "customname"
        dt = datetime(2021, 1, 1, 12, 0, 0, 587166, tzinfo=timezone.utc)
        with freeze_time(dt):
            logger.info("Hello")
        assert capsys.readouterr().err == ""
        dt += timedelta(seconds=1)
        with freeze_time(dt):
            logger.debug("Hello")
        assert capsys.readouterr().err == ""
        dt += timedelta(seconds=1)
        with freeze_time(dt):
            logger.warning("こんにちは")
        res0 = json.loads(capsys.readouterr().err)
        assert res0["message"] == "こんにちは"
        assert res0["time"] == "2021-01-01T12:00:02.587166+00:00"
        for k in (
            "filename",
            "funcName",
            "levelname",
            "lineno",
            "module",
            "name",
            "pathname",
            "process",
            "processName",
            "stack_info",
            "thread",
            "threadName",
        ):
            assert k in res0
        dt += timedelta(seconds=1)
        with freeze_time(dt):
            logger.error("World")
        res1 = json.loads(capsys.readouterr().err)
        assert res1["message"] == "World"
        assert res1["time"] == "2021-01-01T12:00:03.587166+00:00"
        file.seek(0)
        assert [json.loads(line) for line in file.readlines()] == [res0, res1]
