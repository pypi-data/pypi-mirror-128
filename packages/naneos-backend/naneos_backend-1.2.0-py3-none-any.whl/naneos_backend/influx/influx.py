import pandas
from influxdb_client import InfluxDBClient

from .credentials import Credentials


def write_pandas_df(df: pandas.DataFrame, cred: Credentials, meas_name: str, tag_names: list = []):
    """Writes a dataframe into a defined bucket (credentials file).

    Args:
        df (pandas.DataFrame): Dataframe with values and tags (optional).
        cred (Credentials): Credential file.
        meas_name (str): String with the name of the measurement. Will be shown in influxDB
        tag_names (list, optional): List with the columns name of the tags (optional). Defaults to [].
    """
    with InfluxDBClient(url=cred.URL, token=cred.TOKEN, org=cred.ORG) as client:
        with client.write_api() as write_client:
            write_client.write(
                bucket=cred.BUCKET,
                org=cred.ORG,
                record=df,
                data_frame_measurement_name=meas_name,
                data_frame_tag_columns=tag_names,
            )
