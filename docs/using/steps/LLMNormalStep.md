# Normal LLM Step

The `LLMNormalStep` is used to create generative responses.

The output of `LLMNormalStep` is added to the dataframe as a column that can be referenced by the step name. 

## Statistics
`LLMNormalStep` returns useful statistics about the LLM call for each row.  
| Stat name       | Description 
|-------------|----------|
|input_tokens | Number of input token used.
|output_tokens | Number of output tokens used.
|input_cost| Input cost of running the LLM call.
|output_cost | Output cost of running the LLM call.
|num_success | Number of succesful calls.
|num_failure | Number of unsuccesful calls.
|total_latency | Latency for the LLM call.



## Example
In this example, we provide information about a business and three potential codes to choose from and we expect two structured fields in return, `reasoning` and `code`.

```python
joke_prompt = lambda row: f"""
Tell me a joke about {row['topic']}
"""

JokesStep = steps.SimpleLLMStep(
  prompt=joke_prompt,
  model=models.gpt35,
  name="joke"
)
```

When used in a pipeline, this creates a column called "joke". 