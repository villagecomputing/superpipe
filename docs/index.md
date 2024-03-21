# Superpipe - optimized LLM pipelines for structured data

_A lightweight framework to build, evaluate and optimize LLM pipelines for structured outputs: data labeling, extraction, classification, and tagging. Evaluate your pipelines on your own data and easily optimize models, prompts and other parameters for the best accuracy, cost, and speed._

<p align="center"><img src="./assets/grid_search.gif" style="width: 600px;" /></p>

<hr>

## Installation

Make sure you have Python 3.10+ installed, then run

```
pip install superpipe-py
```

## Build, eval, optimize

There are three stages of using Superpipe.

1. [**Build**](./build) &mdash; use your favorite LLM library (langchain, LlamaIndex) and combine with Superpipe's building blocks.
2. [**Evaluate**](./evaluate) &mdash; your pipeline needs to be evaluated on _your_ data. Your data and use case are unique, so benchmarks are insufficient.
3. [**Optimize**](./optimize) &mdash; build once, experiment many times. Easily try different models, prompts, and parameters to optimize end-to-end.

**To see the code, keep reading. If you're ready to give Superpipe a try, visit [Step 1: Build](./build)**

### Build

Any multistep LLM workflow can be converted to a Superpipe pipeline.

Take a look at our [concepts page](../concepts) for a better understanding of Superpipe concepts.

Before you can start using Superpipe you need:

- **A well defined task** - Superpipe is designed well defined tasks like categorization, tagging, and extraction. You should know your goal before you get started.
- **Input Data** - the dataset you want to transform with your pipeline. Superpipe acts over Pandas Dataframes or dictionaries.

With that in hand, you will use Superpipe to build:

- **[Steps](../concepts/steps/)** - each step takes in an input dataframe or Python dictionary and returns a new dataframe or dictionary with the outputs of the step appended.
- **[Pipeline](../concepts/pipelines)** - steps are chained together to create a pipeline.

### Evaluate

Once you've built your pipeline it's time to see how well it works. This requires:

- **Evaluation function** - a function that defines what "correct" is. In many cases this is a string comparison with your ground truth labels but could be any arbitrary function, including a call to an LLM to evaluate generative outputs.
- **Ground truth labels** - the _correct_ label for each row in your data. You can use an early version of your pipeline to generate _candidate labels_ and manually inspect and correct to generate your ground truth.

### Optimize

The last step in using Superpipe is trying out many combinations of parameters to optimize your pipeline along **cost, accuracy, and speed**.

For example, you may want to try:

- GPT-4 vs. Mixtral
- 3, 5, 7 retrieval chunks
- Chain of thought vs. direct prompting
- Few shot prompts

One of the core principles of Superpipe is that you should build once, experiment many times. By building your pipeline in Superpipe steps, testing out every parameter combination is trivial.

Pipeline optimization is done via a [grid search](../concepts/grid_search).

A common usecase of Superpipe is understanding if you can "get away" with using an open source model. See the [models](../concepts/models) to learn how to use Superpipe with any LLM model from any provider.

## Use Cases

Superpipe is useful for any data labeling, extraction, classification, or tagging task where the output is structured and the structure is known.

### Extraction

- **Document extraction** &mdash; Extract entities and facts from PDFs, emails, websites, etc.

- **Product Catalog tagging** &mdash; Enrich your product catalog with AI-generated tags to power search, filtering and recommendations.

- **Query analysis** &mdash; Extract filter arguments from natural language search queries.

### Classification

- **Product Categorization** &mdash; Categorize your product catalog into your custom taxonomy to power search, filtering and merchandising.

- **Sentiment analysis** &mdash; Analyze sentiment of customer reviews, customer support interactions and flag important themes.

- **Customer & Business classification** &mdash; Classify your customers or businesses into government classification codes (NAICS/SIC) or your custom internal categories.

- **Content moderation** &mdash; Detect harmful or policy-violating content.

## Next Steps

[**Step 1: Build**](./build) &mdash; to get started building with Superpipe.

[**Concepts**](./concepts) &mdash; to understand the core concepts behind Superpipe.

[**Why Superpipe?**](./why) &mdash; to understand whether Superpipe is right for you.

[**Workflow**](./workflow) &mdash; to understand the full workflow we suggest for building pipelines.

[**Examples**](./examples) &mdash; for more advanced examples and usage.
