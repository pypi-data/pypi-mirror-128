from dataclasses import dataclass

# TODO update this class to handle all the given data (from serial port)


@dataclass
class naneosMeasurementData:
    timestamp: float = None
    serial_number: int = None
    ldsa: float = None
    number: int = None
    diameter: int = None
    temperature: int = None
    humidity: int = None
    battery_voltage: float = None
    particle_mass: float = None
    error: int = None
