from django.conf import settings

from influxdb import InfluxDBClient


def get_client():
    """
    Get influxdb client.
    """
    if not getattr(settings, "INFLUX_LOGS_ENABLE", False):
        return None
    client = InfluxDBClient(
        settings.INFLUX_LOGS_HOST,
        settings.INFLUX_LOGS_PORT,
        settings.INFLUX_LOGS_USERNAME,
        settings.INFLUX_LOGS_PASSWORD,
        settings.INFLUX_LOGS_DATABASE,
        timeout=getattr(settings, "INFLUX_LOGS_TIMEOUT", 10),
        ssl=getattr(settings, "INFLUX_LOGS_SSL", False),
        verify_ssl=getattr(settings, "INFLUX_LOGS_VERIFY_SSL", False),
    )
    return client
