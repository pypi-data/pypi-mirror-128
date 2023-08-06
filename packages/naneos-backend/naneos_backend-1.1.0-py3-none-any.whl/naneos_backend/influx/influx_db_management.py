from datetime import datetime

from influxdb_client import InfluxDBClient
from naneos_backend.influx.credentials import Credentials


def delete_bucket(cred: Credentials, delete_measurement: str):
    """Deletes the choosen measurement completely from the bucket.

    Args:
        cred (Credentials): Dataclass with data to connect to influxDB.
        delete_measurement (str): Name of the measurement to delete.
    """
    stop_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    start_time = datetime(2000, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ")

    with InfluxDBClient(url=cred.URL, token=cred.TOKEN, org=cred.ORG) as client:
        delete_api = client.delete_api()
        delete_api.delete(
            start_time,
            stop_time,
            f'_measurement="{delete_measurement}"',
            bucket=cred.BUCKET,
            org=cred.ORG,
        )
