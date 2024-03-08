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
    ha_services: str = Field(
        title="HA Services you want the Cat to be able to call",
        default="[]",
        extra={"type": "TextArea"}
    )
