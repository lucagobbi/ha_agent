def get_base_ha_url(settings: dict):
    if settings["is_addon"]:
        return "http://supervisor/core/api"
    else:
        return f"{settings['ha_instance']}/api"


def get_ha_token(settings: dict):
    if settings["is_addon"]:
        return os.getenv("SUPERVISOR_TOKEN")
    else:
        return settings["ha_token"]
