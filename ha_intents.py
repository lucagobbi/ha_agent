from pydantic import BaseModel, Field
from cat.experimental.form import form, CatForm
from cat.looking_glass.cheshire_cat import CheshireCat
from cat.plugins.ha_agent.utils import get_ha_client
import json

ccat = CheshireCat()

def get_examples_from_settings():
    settings = ccat.mad_hatter.get_plugin().load_settings()
    ha_intents = json.loads(settings["ha_intents"])
    return [intent["example"] for intent in ha_intents]

def format_intent(intent: dict):
    return f"{intent['name']} (e.g. \"{intent['example']}\")"

def format_intents(intents: list):
    return "\n".join([format_intent(intent) for intent in intents])

def get_formatted_intents():
    settings = ccat.mad_hatter.get_plugin().load_settings()
    ha_intents = json.loads(settings["ha_intents"])
    return format_intents(ha_intents)

class IntentModel(BaseModel):
    intent_name: str = Field(description=f"Must be one of the following: {get_formatted_intents()}. ")

@form
class IntentForm(CatForm):
    description = f"Useful to pursue an action given an intent - Examples: {get_examples_from_settings()}"
    model_class = IntentModel
    start_examples = get_examples_from_settings()
    stop_examples = []
    
    def submit(self, form_data):
        settings = self.cat.mad_hatter.get_plugin().load_settings()
        ha_client = get_ha_client(settings)
        res = ha_client.request("intent/handle", method="POST", json={"name": form_data["intent_name"]})
        
        return {
            "output": res["speech"]["plain"]["speech"]
        }
