gpt4 = "gpt-4-turbo-preview"
gpt35 = "gpt-3.5-turbo-0125"
mixtral = "mistralai/Mixtral-8x7B-Instruct-v0.1"
mistral = "mistralai/Mistral-7B-Instruct-v0.1"
codellama = "togethercomputer/CodeLlama-34b-Instruct"
llama270b = "meta-llama/Llama-2-70b-chat-hf"
stripedhyena = "togethercomputer/StripedHyena-Nous-7B"
discomixtral = "DiscoResearch/DiscoLM-mixtral-8x7b-v2"

# Define a dictionary with model pricing information
model_pricing = {
    gpt4: {"input_cost_per_1000": 0.01, "output_cost_per_1000": 0.03, "provider": "openai"},
    gpt35: {"input_cost_per_1000": 0.0005, "output_cost_per_1000": 0.0015, "provider": "openai"},
    mixtral: {"input_cost_per_1000": 0.0006, "output_cost_per_1000": 0.0006, "provider": "togetherai"},
    mistral: {"input_cost_per_1000": 0.0002, "output_cost_per_1000": 0.0002, "provider": "togetherai"},
    codellama: {"input_cost_per_1000": 0.000776, "output_cost_per_1000": 0.000776, "provider": "togetherai"},
    llama270b: {"input_cost_per_1000": 0.0009, "output_cost_per_1000": 0.0009, "provider": "togetherai"},
    stripedhyena: {"input_cost_per_1000": 0.0002, "output_cost_per_1000": 0.0002, "provider": "togetherai"},
    discomixtral: {"input_cost_per_1000": None, "output_cost_per_1000": None, "provider": None},
}