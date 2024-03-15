# Concepts

### Steps

At a high level Superpipe works by taking input data and transforming it in steps to get the desired output. Each step takes in an input dataframe or Python dictionary and returns a new dataframe or dictionary with the outputs of the step appended. For example, here's how you'd invoke the built-in `LLMStep`.

```python
from superpipe.steps import SimpleLLMStep

joke_prompt = lambda row: f"""
Tell me a joke about {row['topic']}
"""

joke_step = SimpleLLMStep(
  prompt=joke_prompt,
  model=models.gpt35,
  name="joke"
)
joke_step.apply(dataframe)
```

??? question "Why steps?"

    When doing data transformation, extraction or classification using LLMs, it's crucial to think in steps.

    - **Increased accuracy** &mdash;

    - **Separation of concerns** &mdash;

    - **Interpretability and debugging** &mdash;

    - **Modularity** &mdash;

Superpipe comes with a handful of built-in steps but it's easy (and recommended) to create your own steps by subclassing `CustomStep`. This allows you to do pretty much anything inside a step - call a third party api, lookup a DB, etc.

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

You can provide any arbitrary evaluation function, as long as it takes in a `row` argument and returns a boolean. The simplest type of evaluation is a string comparison, but you can use arbitrarily complex eval functions including LLM calls.

```python
evaluator = lambda row: row['code'].lower() == row['code_groundtruth'].lower()

# option 1
pipeline = Pipeline(
  steps=[
    serp_step,
    top3_codes_step,
    top1_code_step],
  evaluation_fn=evaluator
)

# option 2
pipeline.evaluate(evaluator)
```

## Parameters

One of the design goals of Superpipe is to make pipelines and steps fully parametric - meaning every aspect of both is exposed as a parameter and can be changed even after the pipeline has been defined and run.

For example in the `joke_step` defined above, the `model` and `prompt` that were passed in during initialization are parameters that can be easily update afterwards using the `update_params` function.

```python
from superpipe import models

joke_step.update_params({
  "model": models.gpt4
})
```

The same applies to pipelines as well, but since pipelines themselves don't have parameters, only steps do, the `params` dict needs to contain the step parameters dict as the values and step names as the keys.

```python
pipeline.update_params({
  "joke": {
    "model": models.gpt4
  }
})
```

## Optimization

Building and evaluating your pipeline is a good start, but you rarely get the best accuracy-cost-speed tradeoff on the first attempt, and there's a lot of low-hanging fruit to optimize. There are two ways to optimize your solution:

1. Tune the parameters of your pipeline
2. Try a different technique (ie. build a different pipeline)

For 1, Superpipe lets you run a [hyperparameter grid search](/). This means you can try different models, values of K, prompts, etc. on the same pipeline and dataset. Then you can compare the results across accuracy, cost, speed and pick the one that's best for your situation.

For 2, we're working on a AI-powered copilot that lets you experiment with different techniques.
