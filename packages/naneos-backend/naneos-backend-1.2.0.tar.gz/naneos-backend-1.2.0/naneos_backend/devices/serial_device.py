from .device import Device

import time
from serial import Serial
from naneos_backend.logger import logger


class SerialDevice(Device):
    # empty method -> implement on device bases
    def _separate_line_to_list(self, raw_line: str) -> list:
        pass

    def _scan_ports(self):
        pass

    ####################################################################################
    def __init__(self, com_port: str = None, baud: int = None) -> None:
        super().__init__()

        self._name = "template_serial_device"
        self._port = com_port
        self._serial_number = None
        self._baud = baud
        self._timeout = 2

    ####################################################################################
    # serial methods
    def _open_port(self) -> bool:
        # error_flag = None
        for _ in range(10):
            try:
                self._serial = Serial(self._port, self._baud, timeout=self._timeout)
                if self._serial.isOpen():
                    return True
            except IOError:  # triggers when port is used by another application.
                error_flag = "IOError"
            except Exception as e:
                error_flag = e

        # Error handling / output
        if error_flag == "IOError":
            logger.error(
                f"Too many connection attempts to port {self._port}. "
                + f"Port seems to be used by another application."
            )
        else:
            logger.error(
                f"Too many connection attempts to port {self._port}. "
                + f"\nError Message: {error_flag}"
            )

        return False

    def _close_port(self) -> None:
        self._serial.close()

    def _readline(self) -> list:
        return self._serial.readline().decode("ASCII")

    def _writeline(self, line: str):
        self._serial.write(line.encode())
        time.sleep(30e-3)

    ####################################################################################
    # implementation of empty parent methods
    def _read_device_raw(self) -> list:
        raw_line = self._readline()
        return self._separate_line_to_list(raw_line)

    def send_cmd(self, cmd: str):
        self._writeline(cmd)

        cmd_str = cmd.replace("\r", "").replace("\n", "")
        logger.debug(f"CMD: {cmd_str}, ANSW: -")

    def send_cmd_with_answer(self, cmd: str) -> str:
        answer = ""
        i = 3

        while i >= 0 and answer == "":
            self._writeline(cmd)

            old_timeout = self._serial.timeout
            self._serial.timeout = 25e-3  # makes cmds much faster
            answer = self._readline()
            i -= 1
        self._serial.timeout = old_timeout

        cmd_str = cmd.replace("\r", "").replace("\n", "")
        answer = answer.replace("\r", "").replace("\n", "")
        logger.debug(f"CMD: {cmd_str}, ANSW: {answer}")

        return answer
