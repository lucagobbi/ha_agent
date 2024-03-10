from cat.mad_hatter.decorators import tool, hook, plugin
from cat.plugins.ha_agent.settings import HaAgentSettings
from pydantic import BaseModel
from cat.experimental.form import form, CatForm

# data structure to fill up
class LightOnModel(BaseModel):
    light_name: str


# forms let you control goal oriented conversations
@form
class LightOnForm(CatForm):
    description = "Turn on the light of the specified light name"
    model_class = LightOnModel
    start_examples = [
        "Turn on the kitchen light",
        "Turn on the bedroom light"
    ]
    stop_examples = []
    ask_confirm = False

    def submit(self, form_data):
        
        # do the actual order here!

        # return to convo
        return {
            "output": f"Pizza order on its way: {form_data}"
        }


