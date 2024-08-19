import logging
import re

import pytest
from labgrid import Target
from labgrid.driver import ShellDriver
from labgrid.driver.consoleexpectmixin import ConsoleExpectMixin
from labgrid.driver.exception import ExecutionError

UART_LINE = re.compile(r"(\d+) Hello, UART")


def test_serial(target: Target) -> None:
    serial: ConsoleExpectMixin = target.get_driver("SerialDriver", name="primary")
    data = serial.read(timeout=1)
    logging.info(f"Read data: {data}")
    result = serial.expect(UART_LINE)
    count = int(result[2].group(1))  # type: ignore
    logging.info(f"{count}")


def test_shell(target: Target) -> None:
    shell: ShellDriver = target.get_driver(
        "ShellDriver"
    )  # only a single ShellDriver exists, thus no name provided
    assert shell
    output = shell.run_check("ls -la")
    assert output
    logging.info(f"Output: {output}")
    with pytest.raises(ExecutionError, match="asdf: not found"):
        output = shell.run_check("asdf")
