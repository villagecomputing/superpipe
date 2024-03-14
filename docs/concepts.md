# Concepts

### Steps

At a high level Superpipe works by taking input data and transforming it in steps to get the desired output. Each step takes in an input dataframe or Python dictionary and returns a new dataframe or dictionary with the outputs of the step appended.

```python
from superpipe.steps import SimpleLLMStep

joke_prompt = lambda row: f"""
Tell me a joke about {row['topic']}
"""

JokesStep = SimpleLLMStep(
  prompt=joke_prompt,
  model=models.gpt35,
  name="joke"
)
```

??? question "Why steps?"

    When doing data transformation, extraction or classification using LLMs, it's crucial to think in steps.

    - **Increased accuracy** &mdash;

    - **Separation of concerns** &mdash;

    - **Interpretability and debugging** &mdash;

    - **Modularity** &mdash;

For more details see the [steps](/) section.

### Pipelines

Steps are chained together to create a pipeline. Similar to a step, a pipeline also takes an input dataframe or dictionary and returns a new dataframe or dictionary with all the outputs of all the steps appended.

```python
from superpipe.pipeline import Pipeline

serp_step = ...
top3_codes_step = ...
top1_code_step = ...

pipeline = Pipeline(
  steps=[
    serp_step,
    top3_codes_step,
    top1_code_step]
)
```

For more details see the [pipelines](/) section.

## Evaluation

Pipelines can and should be evaluated to ensure they work well. Without proper evaluation, there's no way to know if the pipeline will perform well in the wild. There are two ways to do this - you can pass in an evaluation function when initializing the pipeline or call the `evaluate` method after the pipeline has run.

## Parameters

## Optimization
