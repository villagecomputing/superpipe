# Superpipe - LLM pipelines for structured data extraction and classification

_A lightweight framework to build, evaluate and optimize LLM-based data transformation, extraction and classification pipelines._

<hr>

Superpipe helps you build multi-step LLM pipelines, then evaluate and optimize them to find the right trade-off between **accuracy, cost, and speed**. It can also help deploy and monitor them in production (coming soon).

Superpipe was designed with the following goals in mind:

- **Simplicity**: it's easy to get started because there aren't many abstractions to learn.
- **Unopinionated**: it abstracts the boilerplate but lets you bring your own logic.
- **Works with datasets**: works natively with `pandas` dataframes so you can evaluate and optimize over large datasets.
- **Parametric**: every aspect of your pipeline is exposed as a parameter so you can easily try different models or run hyperparameter searches.
- **Plays well with others**: use your favorite LLM library or tool, including langchain, LlamaIndex, DSpy, etc.

## Getting Started

Make sure you have Python 3.10+ installed, then run

```
pip install superpipe-py
```

## Basic Usage

The example below shows a simple 2-step data extraction pipeline designed to extract some fields from a long and complex document.

```python
import pandas as pd
from superpipe import LLMStructuredStep, pipeline
from pydantic import BaseModel

df = pd.read_csv()
```

## Concepts

## Why Superpipe?

There are several great tools that help you chain together LLM calls or build agent workflows that make for great prototypes or demos. Superpipe is different for two reasons:

1. **It focuses exclusively on unstructured -> structured (extraction and classification) problems**. Though it can be used for generative use cases, that is not where it shines.
2. **It helps you build production-grade software that is reliably accurate, fast and cheap**. Accuracy, speed and cost don't matter for prototypes and demos, but they do when you're trying to solve real problems for real customers at scale.

### Building production-grade LLM pipelines

We recommend the following workflow, and Superpipe is designed to make this workflow easy:

1. Build the first version of your pipeline (usually using a powerful but expensive model like GPT-4)
2. Use it to create ground truth labels (your golden set) to evaluate performance on
3. Try different techniques and parameters and evaluate them against each other with a hyperparameter search
4. Pick the technique and parameters that maximize your objective function
5. (Coming soon) Use the ground truth to fine-tune a cheaper/faster model

## More Examples

Find more detailed examples and code walthroughs in the [Examples](/) section of the docs. Or find jupyter notebooks in the [examples](/) folder in GitHub.

## Contributing

## License

Superpipe is licensed under the terms of the MIT License.
