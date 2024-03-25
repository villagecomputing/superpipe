from typing import Dict, Tuple

gpt4 = "gpt-4-turbo-preview"
gpt35 = "gpt-3.5-turbo-0125"
mixtral = "mistralai/Mixtral-8x7B-Instruct-v0.1"
mistral = "mistralai/Mistral-7B-Instruct-v0.1"
codellama = "togethercomputer/CodeLlama-34b-Instruct"
llama270b = "meta-llama/Llama-2-70b-chat-hf"
stripedhyena = "togethercomputer/StripedHyena-Nous-7B"
discomixtral = "DiscoResearch/DiscoLM-mixtral-8x7b-v2"
claude3_opus = "claude-3-opus-20240229"
claude3_sonnet = "claude-3-sonnet-20240229"
claude3_haiku = "claude-3-haiku-20240307"

# model cost per 1M tokens in $ (input_cost, output_cost)
_pricing = {
    gpt4: (10, 30),
    gpt35: (0.5, 1.5),
    mixtral: (0.6, 0.6),
    mistral: (0.2, 0.2),
    codellama: (0.776, 0.776),
    llama270b: (0.9, 0.9),
    stripedhyena: (0.2, 0.2),
    claude3_opus: (15, 75),
    claude3_sonnet: (3, 15),
    claude3_haiku: (.25, 1.25)
}


def update_pricing(pricing: Dict[str, Tuple[float, float]]):
    global _pricing
    _pricing.update(pricing)


def get_cost(prompt_tokens: int, completion_tokens: int, model: str):
    """
    Return the cost of a completion based on the number of tokens in the prompt and completion.
    """
    pricing = _pricing.get(model)
    if not pricing or prompt_tokens is None or completion_tokens is None:
        return None
    return (pricing[0]*prompt_tokens/1e6, pricing[1]*completion_tokens/1e6)
