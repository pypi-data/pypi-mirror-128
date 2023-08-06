from naneos_backend.devices.naneos.partector2 import Partector2
from naneos_backend.devices.naneos.silentPump import SilentPump
from naneos_backend.devices.serial_device import SerialDevice
from naneos_backend.devices.third_party.defender import Defender510
from naneos_backend.logger import logger
from naneos_backend.port_scanning.device_mapping import DeviceMapping
from serial.tools import list_ports


class PortScan:
    def __init__(self) -> None:
        self._devices = []  # list for found devices
        self._free_ports = []  # list for free ports
        ign_ports = ["/dev/ttyAMA0"]  # AMA0 = raspi BLUETOOTH port

        # fetching all free ports from system (tested on linux and windows)
        self._free_ports = [p.device for p in list_ports.comports() if p.device not in ign_ports]
        logger.debug(f"Found possible ports: {self._free_ports}")

    def __serial_routine(self, serial_device: SerialDevice, device_name: str):
        serial_device._close_port()

        if serial_device._initialized:
            return DeviceMapping(name=device_name, serial_number=serial_device._serial_number, port=serial_device._port)
        else:
            return False

    def __manage_serial_ports_entries(self, devices: list):
        # appends the device to the list of devices if found in list
        [self._devices.append(d) for d in devices if type(d) == DeviceMapping]
        # removes the used ports from the free ports
        [self._free_ports.remove(p) for p in self._free_ports for d in self._devices if p in d.port]

    def scan_for_p2_serial(self):
        """Scans for a P2 device."""
        devices = [self.__serial_routine(Partector2(p, scanning=True), "P2") for p in self._free_ports]
        self.__manage_serial_ports_entries(devices)

    def scan_for_silent_pump(self):
        """Scans for a silent_pump."""
        devices = [self.__serial_routine(SilentPump(p, scanning=True), "silent_pump") for p in self._free_ports]
        self.__manage_serial_ports_entries(devices)

    def scan_for_defender(self):
        """Scans for defender510. Make sure that defender is running in constant mode."""
        devices = [self.__serial_routine(Defender510(p, scanning=True), "defender") for p in self._free_ports]
        self.__manage_serial_ports_entries(devices)

    def log_possible_devices(self):
        log_line = "\n" + DeviceMapping.get_header_str()
        log_line += "".join([d.get_specs_str() for d in self._devices])

        logger.info(log_line)

    def get_p2_com_ports(self):
        return [p.port for p in self._devices if p.name == "P2"]

    def get_silent_pump_ports(self):
        return [p.port for p in self._devices if p.name == "silent_pump"]

    def get_defender_ports(self):
        return [p.port for p in self._devices if p.name == "defender"]
