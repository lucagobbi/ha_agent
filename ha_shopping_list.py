from cat.mad_hatter.decorators import tool
from cat.plugins.ha_agent.utils import get_ha_client
from cat.looking_glass.cheshire_cat import CheshireCat
from ast import literal_eval

ccat = CheshireCat()
settings = ccat.mad_hatter.get_plugin().load_settings()
ha_client = get_ha_client(settings)
shopping_list = ha_client.get_domain("shopping_list")

@tool(return_direct=True)
def shopping_list_add(items, cat):
    """Useful to add an item or multiple items to the shopping list. User may say: "Add apples to the shipping list" or similar. Argument "items" is an array of items."""
    items = literal_eval(items)
    for item in items:
        shopping_list.add_item(name=str(item))
    return f"Added {', '.join(items)} to the shopping list"

@tool(return_direct=True)
def shopping_list_remove(items, cat):
    """Useful to remove an item or multiple items from the shopping list. User may say: "Remove apples from the shipping list" or similar. Argument "items" is an array of items."""
    items = literal_eval(items)
    for item in items:
        shopping_list.remove_item(name=str(item))
    return f"Removed {', '.join(items)} from the shopping list"

@tool(return_direct=True)
def shopping_list_mark_as_complete(items, cat):
    """Useful to mark an item or multiple items as complete. User may say: "Mark apples as complete in the shipping list" or similar. Argument "items" is an array of items."""
    items = literal_eval(items)
    for item in items:
        shopping_list.complete_item(name=str(item))
    return f"Marked {', '.join(items)} as complete"

@tool(return_direct=True)
def shopping_list_mark_as_incomplete(items, cat):
    """Useful to mark an item or multiple items as incomplete. User may say: "Mark apples as incomplete in the shipping list" or similar. Argument "items" is an array of items."""
    items = literal_eval(items)
    for item in items:
        shopping_list.incomplete_item(name=str(item))
    return f"Marked {', '.join(items)} as incomplete"

@tool(return_direct=True)
def get_shopping_list(tool_input, cat):
    """Useful to get the shopping list. User may ask: "give me the whole shopping list" or similar."""
    items = ha_client.request("shopping_list", "GET")
    return f"Here's the shopping list: {', '.join([item['name'] for item in items])}"

@tool(return_direct=True)
def clear_shopping_list(tool_input, cat):
    """Useful to clear the shopping list. User may ask: "clear the whole shopping list" or similar."""
    shopping_list.clear_completed_items()
    return "Cleared the shopping list"




