import pandas
from naneos_backend.logger import logger
from numpy import pi

from .credentials import Credentials
from .influx import write_pandas_df


def write_p2_data_to_naneos_influx(
    df: pandas.DataFrame,
    credentials: Credentials,
    serial_number: str,
    customer_id: str,
):
    """Writes a dataframe from p2 object to the choosen InfluxDB.

    Args:
        df (pandas.DataFrame): The dataframe from the p2 object.
        credentials (Credentials): Credentials with write permissions.
        serial_number (str): The serial number as string (for influx tag).
        customer_id (str): The customer id as string (for influx tag).
    """

    # manipulate df
    df = __extract_p2_influx_data(df)
    df = __rename_columns_to_naneos_influx_style(df)
    df["particle_mass"] = __calculate_particle_mass(
        df["particle_number_concentration"],
        df["average_particle_diameter"],
    )
    # add new columns with tags
    df = __add_p2_tags(df, serial_number, customer_id)

    # upload to database
    write_pandas_df(df, credentials, "v6_sensor", __get_p2_tags_list())
    logger.debug(f"Wrote {len(df)} values to influxDB!")


def __extract_p2_influx_data(df: pandas.DataFrame) -> pandas.DataFrame:
    """Returns dataframe without unused columns."""
    return df[
        [
            "Diameter_nm",
            "Battery_V",
            "Status",
            "LDSA",
            "Number_perCm3",
            "RelativeHumidity_percent",
            "Temperature_Celsius",
        ]
    ].copy()


def __rename_columns_to_naneos_influx_style(df: pandas.DataFrame) -> pandas.DataFrame:
    """Returns dataframe with renamed columns."""
    df.columns = [
        "average_particle_diameter",
        "battery_voltage",
        "device_status",
        "ldsa",
        "particle_number_concentration",
        "relative_humidity",
        "temperature",
    ]

    return df


def __calculate_particle_mass(number: pandas.Series, diameter: pandas.Series) -> pandas.Series:
    """Calculates the particle_mass from number and diameter.

    Due to Martin the obtained values are very uncertain.
    """
    return number * pi * 6.38 / 6.0 * pow(diameter, 3) * 1.2e-9


def __add_p2_tags(df: pandas.DataFrame, serial_number: str, customer_id: str) -> pandas.DataFrame:
    """Adds the v6_sensor tags as new columns to the dataframe."""
    df["device_name"] = "P2"
    df["serial_number"] = serial_number
    df["customer_id"] = customer_id

    return df


def __get_p2_tags_list() -> list:
    """List is used in the influxdb-client for separating tags from values."""
    return ["device_name", "serial_number", "customer_id"]
