from .port_scan import PortScan
from naneos_backend.logger import logger


def scan_for_single_p2() -> str:
    """Scans blocking for P2 until found one."""
    while True:
        try:
            scanner = PortScan()
            scanner.scan_for_p2_serial()

            if scanner.get_p2_com_ports():
                scanner.log_possible_devices()
                return scanner.get_p2_com_ports()[0]
            else:
                logger.warning("P2 not found. Retrying.")
        except Exception as e:
            logger.error(e)


def scan_for_single_silent_pump() -> str:
    """Scans blocking for silent-pump until found one."""
    while True:
        try:
            scanner = PortScan()
            scanner.scan_for_silent_pump()

            if scanner.get_silent_pump_ports():
                scanner.log_possible_devices()
                return scanner.get_silent_pump_ports()[0]
            else:
                logger.warning("Silent-pump not found. Retrying.")
        except Exception as e:
            logger.error(e)


def scan_for_single_defender() -> str:
    """Scans blocking for defender until found one."""
    while True:
        try:
            scanner = PortScan()
            scanner.scan_for_defender()

            if scanner.get_defender_ports():
                scanner.log_possible_devices()
                return scanner.get_defender_ports()[0]
            else:
                logger.warning("Defender not found. Retrying.")
        except Exception as e:
            logger.error(e)


def scan_for_single_p2_and_silent_pump() -> list:
    """Scans blocking for silent-pump and p2 until found one of both."""
    while True:
        try:
            scanner = PortScan()
            scanner.scan_for_p2_serial()
            scanner.scan_for_silent_pump()

            if scanner.get_silent_pump_ports() and scanner.get_p2_com_ports():
                return [scanner.get_p2_com_ports()[0], scanner.get_silent_pump_ports()[0]]
            else:
                if not scanner.get_p2_com_ports():
                    logger.warning("P2 not found. Retrying.")
                if not scanner.get_silent_pump_ports():
                    logger.warning("Silent-pump not found. Retrying.")
        except Exception as e:
            logger.error(e)
