import asyncio
import subprocess
import sys
import time
from threading import Thread

from bleak import BleakScanner
from naneos_backend.devices.naneos.naneos_measurement_dataclass import naneosMeasurementData


class BleScannerPartector2:
    def __init__(self) -> None:
        self.__thread = None
        self.__async_loop = None

        self.__next_scanning_time = time.time() - 1.0  # starts directly

        self.__scanned_list = []
        self.decoded_data_list = []

    def start_scanning(self):
        self.__async_loop = asyncio.get_event_loop()
        self.__async_loop.create_task(self.__scan_in_background())
        self.__async_loop.create_task(self.__decode_beacon_data())

        self.__thread = Thread(target=self.__async_loop.run_forever)
        self.__thread.start()

    def stop_scanning(self):
        self.__async_loop.call_soon_threadsafe(self.__async_loop.stop)
        self.__thread.join()

    async def __scan_in_background(self):
        while True:
            self.__wait_until_trigger()
            self.__update_next_scanning_time()

            tmp_devices = await BleakScanner.discover(timeout=0.7)
            timestamp = time.time()
            for d in (x for x in tmp_devices if x.name == "P2"):
                self.__scanned_list.append([timestamp, d])

            # handles blueZ error on raspberry pi's (20.11.2021)
            if "linux" in sys.platform:
                self.__clean_bluez_cache()

    def __update_next_scanning_time(self):
        if abs(time.time() - self.__next_scanning_time) < 0.1:
            self.__next_scanning_time += 1.0
        else:
            self.__next_scanning_time = time.time() + 1

    def __wait_until_trigger(self):
        # sleep until the specified datetime
        dt = self.__next_scanning_time - time.time()

        if dt > 0.0 and dt < 1.0:
            time.sleep(dt)

    # method is linux (+ maybe macos) only
    def __clean_bluez_cache(self):
        # get str with all cached devices from shell
        cached_str = subprocess.check_output("bluetoothctl devices", shell=True).decode(sys.stdout.encoding)

        # str manipulating and removing the apropreate P2 mac-addresses
        cached_list = cached_str.splitlines()
        for line in (x for x in cached_list if "P2" in x):
            # line format: "Device XX:XX:XX:XX:XX:XX P2"
            line = line.replace("Device", "").replace("P2", "").replace(" ", "")
            subprocess.check_output(f"bluetoothctl -- remove {line}", shell=True)
            # other possibility would be the use of subprocess.run or os.system which are both verbose

    async def __decode_beacon_data(self):
        while True:
            for d in self.__scanned_list:
                timestamp = d[0]
                scan_result = d[1]

                beac_meta = scan_result.metadata["manufacturer_data"]
                beac_bytes = list(beac_meta.keys())[0].to_bytes(2, byteorder="little")
                beac_bytes += list(beac_meta.values())[0]

                # if first byte is no X there is something wrong
                if chr(beac_bytes[0]) == "X" and len(beac_bytes) == 22:
                    measurement = self.__parse_mesurment_data(timestamp, beac_bytes)
                    self.decoded_data_list.append(measurement)

            self.__scanned_list = []

            await asyncio.sleep(3)

    def __parse_mesurment_data(self, timestamp, beac_bytes: bytes) -> naneosMeasurementData:
        measurement = naneosMeasurementData()

        measurement.timestamp = timestamp
        measurement.ldsa = (int(beac_bytes[1]) + (int(beac_bytes[2]) << 8) + (int(beac_bytes[3]) << 16)) / 100
        measurement.diameter = int(beac_bytes[4]) + (int(beac_bytes[5]) << 8)
        measurement.number = int(beac_bytes[6]) + (int(beac_bytes[7]) << 8) + (int(beac_bytes[8]) << 16)
        measurement.temperature = int(beac_bytes[9])
        measurement.humidity = int(beac_bytes[10])
        measurement.error = (
            int(beac_bytes[11]) + (int(beac_bytes[11]) << 8) + (((int(beac_bytes[20]) >> 1) & 0b01111111) << 16)
        )
        measurement.battery_voltage = (int(beac_bytes[13]) + (int(beac_bytes[14]) << 8)) / 100
        measurement.serial_number = int(beac_bytes[15]) + (int(beac_bytes[16]) << 8)
        measurement.particle_mass = (
            int(beac_bytes[17]) + (int(beac_bytes[18]) << 8) + (int(beac_bytes[19]) << 16)
        ) / 100

        return measurement

    def get_decoded_data_list(self):
        data_list_copy = self.decoded_data_list.copy()
        self.decoded_data_list = []

        return data_list_copy
