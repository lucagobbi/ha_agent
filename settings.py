from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field
from typing import Optional

class HaAgentSettings(BaseModel):
    is_addon: bool = Field(
        title="Is the Cat installed as HA addon?",
        default=False
    )
    ha_instance: Optional[str] = Field(
        title="HA instance URL (only if not addon)",
        default="http://homeassistant.local:8123"
    )
    ha_token: Optional[str] = Field(
        title="HA Auth Token (only if not addon)",
        default="Bearer ..."
    )
    ha_lights: str = Field(
        title="List of lights configured in your HA (entity_id and friendly name)",
        default="[{\"entity_id\": \"light.your_light\", \"friendly_name\": \"friendly name for your light\"}]"
    )
    ha_intents: str = Field(
        title="List of intents configured in your HA (intent name, example trigger)",
        default="[{\"name\": \"intentName\", \"example\": \"Trigger sentence example\"}]"
    )

@plugin
def settings_model():
    return HaAgentSettings
