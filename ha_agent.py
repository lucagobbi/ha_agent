from cat.mad_hatter.decorators import tool, hook, plugin
from cat.plugins.ha_agent.settings import HaAgentSettings


@plugin
def settings_model():
    return HaAgentSettings





