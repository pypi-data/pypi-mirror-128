import requests
from naneos_backend.devices.naneos.naneos_measurement_dataclass import naneosMeasurementData
from naneos_backend.ble.ble import BleScannerPartector2
import time
from naneos_backend.logger import logger


def ble_upload_continous_failsafe_blocking(api_url: str):
    while True:
        try:
            ble_upload_continous_blocking(api_url)
        except Exception as e:
            print(e)
            time.sleep(3)


def ble_upload_continous_blocking(api_url: str):
    ble_scanner = BleScannerPartector2()
    ble_scanner.start_scanning()

    data_list = []
    while True:  # TODO: detect stop condition
        time.sleep(5)

        data_list.extend(ble_scanner.get_decoded_data_list())
        post_status = upload_from_ble_scanner(api_url, data_list)

        if post_status == 204:
            logger.info(f"Successfully uploaded {len(data_list)} measurements, Return Code: {post_status}")
            data_list = []
        elif post_status is False:
            logger.info("No data to upload. Check BLE setting on your partector!")
        else:
            logger.error(
                f"Error during HTTP-Post. Return Code: {post_status}. {len(data_list)} measurements in buffer."
            )


def upload_from_ble_scanner(api_url, measurement_list: list) -> int:
    post_status = False

    json_post = __create_json_post_message(measurement_list)
    if json_post is not False:
        post_status = post_to_lambda_api(api_url, json_post)

    return post_status


def post_to_lambda_api(api_url, json_values: dict) -> int:
    x = requests.post(url=api_url, json=json_values)

    return x.status_code


def __create_json_post_message(data_list: list) -> dict:
    empty_json = True
    body = __create_empty_body()

    for d in (x for x in data_list if type(x) == naneosMeasurementData):
        empty_json = False
        body["values"].append(__create_values_entry(d))

    if empty_json:
        return False
    else:
        return body


# TODO create Gateway ID and type
def __create_empty_body() -> dict:
    message = {
        "staticGateway": {
            "deviceID": 0,
            "firmwareVersion": 0,
            "type": "app",
        },
        "values": [],
    }

    return message


# TODO add GPS signal, cellular signal strength
def __create_values_entry(data: naneosMeasurementData) -> dict:
    message = {
        "deviceName": "P2",
        "gatewayData": {"battery": 0, "cellularSignal": 0, "freeMemory": 0},
        "locationData": {"latitude": 0.0, "longitude": 0.0},
        "partectorData": {
            "average_particle_diameter": data.diameter,
            "battery_voltage": data.battery_voltage,
            "device_status": data.error,
            "ldsa": data.ldsa,
            "particle_mass": data.particle_mass,
            "particle_number_concentration": data.number,
            "relative_humidity": data.humidity,
            "serial_number": data.serial_number,
            "temperature": data.temperature,
        },
        "timestamp": int(data.timestamp),
    }

    return message
