from openai import OpenAI
from labelkit.models import *

# TODO: add support for non-openai providers

openai_client = None
client_for_model = {}


def init_openai(api_key=None, base_url=None):
    global openai_client
    openai_client = OpenAI(api_key=api_key, base_url=base_url)
    client_for_model[gpt35] = openai_client
    client_for_model[gpt4] = openai_client


def get_client(model):
    if openai_client is None:
        init_openai()
    return client_for_model.get(model)


def set_client_for_model(model, api_key, base_url):
    client_for_model[model] = OpenAI(api_key=api_key, base_url=base_url)
