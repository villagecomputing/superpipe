from openai import OpenAI
from labelkit.models import *

# TODO: add support for non-openai providers

openai_client = OpenAI()

client_for_model = {
    gpt35: openai_client,
    gpt4: openai_client,
}


def get_client(model):
    return client_for_model.get(model)


def set_client_for_model(model, api_key, base_url):
    client_for_model[model] = OpenAI(api_key=api_key, base_url=base_url)
