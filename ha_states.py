from pydantic import BaseModel, Field
from cat.experimental.form import form, CatForm
from cat.looking_glass.cheshire_cat import CheshireCat
from cat.plugins.ha_agent.utils import get_ha_client
from homeassistant_api.models.states import State
import json
from typing import Literal

ccat = CheshireCat()

def get_ha_entities_friendly_names():
    settings = ccat.mad_hatter.get_plugin().load_settings()
    if settings["ha_entities"] == "":
        return []
    entities = json.loads(settings["ha_entities"])
    return [entity["friendly_name"] for entity in entities]

def get_entity_id(friendly_name: str):
    settings = ccat.mad_hatter.get_plugin().load_settings()
    entities = json.loads(settings["ha_entities"])
    for entity in entities:
        if entity["friendly_name"] == friendly_name:
            return entity["entity_id"]
        
def get_examples_from_entities(get_or_set: Literal["Get", "Set"]):
    settings = ccat.mad_hatter.get_plugin().load_settings()
    if settings["ha_entities"] == "":
        return []
    entities = json.loads(settings["ha_entities"])
    return [f"{get_or_set} the state of {entity['friendly_name']}" for entity in entities]


class GetStateModel(BaseModel):
    entity_name: str = Field(description=f"Must be one of the following: {get_ha_entities_friendly_names()}. ")

@form
class GetStateForm(CatForm):
    description = f"Useful to get the state of an entity"
    model_class = GetStateModel
    start_examples = get_examples_from_entities("Get")
    stop_examples = []
    
    def submit(self, form_data):
        settings = self.cat.mad_hatter.get_plugin().load_settings()
        ha_client = get_ha_client(settings)
        state = ha_client.get_state(entity_id=get_entity_id(form_data["entity_name"]))
        
        return {
            "output": state.state
        }
    
class SetStateModel(BaseModel):
    entity_name: str = Field(description=f"Must be one of the following: {get_ha_entities_friendly_names()}. ")
    new_state: str = Field(description=f"New state that the user wants to be set for the entity")
    
@form
class SetStateForm(CatForm):
    description = f"Useful to set the state of an entity"
    model_class = SetStateModel
    start_examples = get_examples_from_entities("Set")
    stop_examples = []

    def submit(self, form_data):
        settings = self.cat.mad_hatter.get_plugin().load_settings()
        ha_client = get_ha_client(settings)
        new_state = State(
            entity_id=get_entity_id(form_data["entity_name"]),
            state=form_data["new_state"],
        )
        changed_state = ha_client.set_state(new_state)

        return {
            "output": f"The state of {form_data['entity_name']} has been changed to {changed_state.state}"
        }