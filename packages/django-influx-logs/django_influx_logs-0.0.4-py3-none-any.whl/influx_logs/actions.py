from datetime import datetime

from django.conf import settings

from influx_logs.connexion import get_client
from influx_logs.settings import ACTION_MEASUREMENT_NAME

client = get_client()


def log_action(actor, verb, action_object="", target="", tags=None):
    if not client:
        return None
    if not tags:
        tags = {}
    tags["verb"] = verb
    action = [
        {
            "measurement": ACTION_MEASUREMENT_NAME,
            "tags": tags,
            "time": datetime.now(),
            "fields": {
                "actor": actor,
                "action_object": action_object,
                "target": target,
            },
        }
    ]
    client.write_points(action)
