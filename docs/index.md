# Superpipe - LLM pipelines for structured data extraction and classification

_A lightweight framework to build, evaluate and optimize LLM-based data transformation, extraction and classification pipelines._

<p align="center"><img src="./superpipe.png" style="width: 400px;" /></p>

<hr>

Superpipe helps developers build multi-step LLM pipelines, then evaluate and optimize them to find the right trade-off between **accuracy, cost, and speed**. It also helps deploy, monitor and improve them over time by easily testing new models or fine-tuning a custom model.

## The Problem

You have some unstructured data (text, website, pdf, image, etc.) You need to extract or classify the data into some known structure. You may have built a prototype using Langchain, LlamaIndex or another LLM library. Before you deploy this, you'll need to solve a few problems:

!!! note "Problem 1: How do I evaluate my prototype on real data?"

    To properly evaluate your pipeline, you need **high-quality labeled data**. It's not sufficient to evaluate on public benchmark data, you need to evaluate on **your own data** to truly evaluate accuracy.

Once you generate some labeled data and evaluate on it, you'll want to improve your prototype by trying different prompts, models and techniques.

!!! note "Problem 2: How do I improve my prototype across accuracy, cost and speed?"

    You can get pretty far by optimizing your prompts, trying smaller models, or changing various parameters of your pipeline. However, optimizing each piece in isolation isn't enough. **Pipelines need to be optimized end-to-end**.

Once you've optimized and deployed your pipeline in production, you'll need to know if it's actually performing well in production. When new models are released or new techniques are published, you'll want to take advantage of them to stay competitive.

!!! note "Problem 3: How do I monitor my pipeline in production and improve it over time?"

    You can get pretty far by optimizing your prompts, trying smaller models, or changing various parameters of your pipeline. However, optimizing each piece in isolation isn't enough. **Pipelines need to be optimized end-to-end**.

## The Solution

**Build your pipeline**

**Generate labeled data**

**Evaluate your pipeline**

**Optimize your pipeline**

While there are a number of general-purpose LLM libraries focused on different aspects of the above, Superpipe focuses on a specific problem (data extraction and classification) and the optimal workflow for the problem. It is designed with the following goals in mind:

!!! note "Superpipe design goals"

    - **Simplicity**: it's easy to get started because there aren't many abstractions to learn.
    - **Unopinionated**: it acts as the connective tissue and abstracts boilerplate but leaves you in control of logic.
    - **Works with datasets**: works natively with `pandas` dataframes so you can evaluate and optimize over datasets.
    - **Parametric**: every aspect of your pipeline is exposed as a parameter so you can easily try different models or run hyperparameter searches.
    - **Plays well with others**: use your favorite LLM library or tool, including langchain, LlamaIndex, DSpy, etc.

Read more about Superpipe's principles [here](/superpipe/principles).

## Next Steps

**Getting Started** &mdash; for installation and basic usage examples, see the [Getting Started](/superpipe/start) page.

**Concepts** &mdash; to understand the core concepts behind Superpipe, see the [Concepts](/superpipe/concepts) page.

**Why Superpipe?** &mdash; to understand whether Superpipe is right for you, see [Why Superpipe?](/superpipe/why)

**Advanced examples** &mdash; for more advanced examples and usage, see [Examples](/superpipe/examples)

## More Examples

Find more detailed examples and code walthroughs in the [Examples](./examples/) section of the docs. Or find jupyter notebooks in the [examples](./examples/) folder in GitHub.
