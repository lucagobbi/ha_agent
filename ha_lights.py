from pydantic import BaseModel, Field
from cat.experimental.form import form, CatForm
from cat.looking_glass.cheshire_cat import CheshireCat
from cat.plugins.ha_agent.utils import get_ha_client
import json

ccat = CheshireCat()

def get_ha_light_names():
 settings = ccat.mad_hatter.get_plugin().load_settings()
 lights = json.loads(settings["ha_lights"])
 return [light["friendly_name"] for light in lights]


class LightOnOffModel(BaseModel):
    light_name: str = Field(description=f"Must be one of the following: {get_ha_light_names()}. ")
    state: bool = Field(description="True for on, False for off")

@form
class LightOnForm(CatForm):
    description = "Turn on/off the light of the specified light name"
    model_class = LightOnOffModel
    start_examples = [
        "Turn on the kitchen light",
        "Turn off the kitchen light",
    ]
    stop_examples = []
    
    def submit(self, form_data):
        settings = self.cat.mad_hatter.get_plugin().load_settings()
        ha_client = get_ha_client(settings)
        light_service = ha_client.get_domain("light")
        entity_id = self.get_entity_id(form_data["light_name"])
        if form_data["state"]:
            light_service.turn_on(entity_id=entity_id)
        else:
            light_service.turn_off(entity_id=entity_id)
        
        return {
            "output": f"Light {form_data['light_name']} turned on" if form_data["state"] else f"Light {form_data['light_name']} turned off"
        }
    
    def get_entity_id(self, light_name: str):
        settings = self.cat.mad_hatter.get_plugin().load_settings()
        lights = json.loads(settings["ha_lights"])
        for light in lights:
            if light["friendly_name"] == light_name:
                return light["entity_id"]
    


