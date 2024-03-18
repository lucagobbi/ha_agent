from homeassistant_api import Client
import os


def get_ha_api_url(settings: dict) -> str:
    if settings["is_addon"]:
        return "http://supervisor/core/api"
    else:
        return f"{settings['ha_instance']}/api"


def get_ha_token(settings: dict) -> str:
    if settings["is_addon"]:
        return os.getenv("SUPERVISOR_TOKEN")
    else:
        return settings["ha_token"]
    
def get_ha_client(settings: dict) -> Client:
    ha_client = Client(get_ha_api_url(settings), get_ha_token(settings))
    return ha_client
