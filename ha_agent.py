from cat.mad_hatter.decorators import tool, plugin, hook
from cat.looking_glass.cheshire_cat import CheshireCat
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from homeassistant_api import Client
from typing import List
import json
import uuid

ccat = CheshireCat()


@hook(priority=5)
def agent_allowed_tools(allowed_tools, cat):
    allowed_tools = ["call_ha"]
    return allowed_tools

@tool
def call_ha(tool_input, cat):
    """Useful to call an home device or service"""
    settings = ccat.mad_hatter.get_plugin().load_settings()
    ha_client = Client(settings["ha_instance"], settings["ha_token"])
    user_message = cat.working_memory["user_message_json"]["text"]
    user_message_vector = cat.embedder.embed_query(user_message)

    qclient = cat.memory.vectors.vector_db
    search_results = qclient.search(
        "intent_examples",
        user_message_vector,
        with_payload=True,
        limit=1
    )
    print(f"search_results: {search_results}")
    most_similar_intent = search_results[0].payload["intent"]
    print(f"most_similar_intent: {most_similar_intent}")
    payload = {
        "name": most_similar_intent
    }
    response = ha_client.request("intent/handle", "POST", json=payload)
    return response["speech"]["plain"]["speech"]


@plugin
def save_settings(settings):
    ha_intents = json.loads(settings["ha_intents"])
    print(ha_intents)
    load_intents_examples_in_memory(
        [{"name": intent["name"], "examples": intent["examples"]} for intent in ha_intents])
    settings_file_path = "./settings.json"
    old_settings = ccat.mad_hatter.get_plugin().load_settings()
    updated_settings = { **old_settings, **settings }
    try:
        with open(settings_file_path, "w") as json_file:
            json.dump(updated_settings, json_file, indent=4)
        return updated_settings
    except Exception as e:
        ccat.log.error(f"Unable to save plugin {ccat.mad_hatter.get_plugin()._id} settings: {e}")
        return {}


def load_intents_examples_in_memory(intent_scripts: List[dict]):
    qclient = ccat.memory.vectors.vector_db
    intent_collection = "intent_examples"

    embedder_size = len(ccat.embedder.embed_query("hello world"))

    qclient.recreate_collection(
        collection_name=intent_collection,
        vectors_config=VectorParams(
            size=embedder_size,
            distance=Distance.COSINE
        )
    )

    points = []
    for intent in intent_scripts:
        for i, example in enumerate(intent["examples"]):
            vector = ccat.embedder.embed_query(example)
            points.append(PointStruct(id=uuid.uuid4().int, vector=vector, payload={"intent": intent["name"]}))

    result = qclient.upsert(
        collection_name=intent_collection,
        wait=True,
        points=points,
    )
    print(result)