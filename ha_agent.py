from pydantic import BaseModel, Field
from cat.experimental.form import form, CatForm
import requests

class LightOnOffModel(BaseModel):
    light_name: str
    state: bool = Field(description="True for on, False for off")

@form
class LightOnForm(CatForm):
    description = "Turn on/off the light of the specified light name"
    model_class = LightOnOffModel
    start_examples = [
        "Turn on the kitchen light",
        "Turn on the bedroom light",
        "Turn off the kitchen light",
        "Turn off the bedroom light",
    ]
    stop_examples = []
    light_api_url = "/api/services/light/"
    
    def submit(self, form_data):
        settings = self.cat.mad_hatter.get_plugin().load_settings()

        headers = {
                "Authorization": f"Bearer {settings['ha_token']}"
        }

        # we need to retrieve the correct entity_id base on form_data["light_name"]
        body = {
            "entity_id": "light.light_entity_id",
        }
        if form_data["state"]:
            url = f"{settings['ha_instance']}{self.light_api_url}/turn_on"
        else:
            url = f"{settings['ha_instance']}{self.light_api_url}turn_off"
        

        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        return {
            "output": f"Light {form_data['light_name']} turned on" if form_data["state"] else f"Light {form_data['light_name']} turned off"
        }


