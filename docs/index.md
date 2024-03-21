# Superpipe - LLM pipelines for structured data extraction and classification

_A lightweight framework to build, evaluate and optimize LLM-based pipelines for data labeling, extraction, classification, and tagging._

<p align="center"><img src="./assets/superpipe_venn.png" style="width: 400px;" /></p>

<hr>

Superpipe helps developers build multi-step LLM pipelines, then evaluate and optimize them to find the right trade-off between **accuracy, cost, and speed**. It also helps deploy, monitor and improve them over time by easily testing new models or fine-tuning a custom model.

See [Getting Started](./start) or read on to see if Superpipe is right for you.

## The Problem

It's easier than ever to build an LLM pipeline, thanks to many great libraries and tools. When going from prototype to production, however, you will face these problems:

**Problem 1: You have no idea how your pipeline will perform on real data**

To properly evaluate your extraction/classification pipelines, you need <u>_high-quality labeled data_</u>. It's not sufficient to evaluate on public benchmark data, you need to evaluate on <u>_your own data_</u> to reflect true accuracy.

**Problem 2: You need to optimize your pipeline end-to-end across accuracy, cost and speed**

You can get pretty far by optimizing your prompts, trying smaller models, or changing various parameters of your pipeline. However, optimizing each piece in isolation isn't enough. <u>_Pipelines need to be optimized end-to-end_</u>.

**Problem 3: You need to monitor your pipeline in production and improve it over time**

Once your pipeline is serving production traffic, you still need to know how it's doing. Data and models drift over time. As cheaper, faster and better models come out, you need to easily try them and swap them out when it makes sense.

## The Solution

Superpipe helps you build & generate labeled data, then evaluate and optimize your pipeline.

**Step 1: Build your pipeline**

Superpipe makes it easy to build extraction and classification pipelines. You can also use langchain, LlamaIndex or your favorite LLM library. Superpipe acts as the glue between components and leaves you fully in control of the logic.

One of our [principles](./principles) is to <u>_abstract the boilerplate, not the logic_</u>. Using superpipe to build your pipeline, however, makes the following steps easier.

**Step 2: Generate labeled data**

Use your superpipe pipeline to create <u>_candidate labels_</u>. If you use a powerful model combined with powerful techniques you can generate reasonably accurate labels. Then you can manually inspect these labels with [Superpipe Studio](./studio) and fix the wrong ones. This is an important and often overlooked step. Without labeled data you can't evaluate your pipeline and without evaluation you're flying blind.

**Step 3: Evaluate your pipeline**

Armed with labeled data, you can build and evaluate cheaper and faster pipelines. You may want to combine open-source models with more complex techniques (like multi-step prompting, chain-of-though, etc.). You may want to iterate between Steps 1 & 3 by trying multiple approaches and comparing them on accuracy, cost and speed.

**Step 4: Optimize your pipeline**

A pipeline usually has many parameters - foundation models, prompts, structured outputs, k-values, etc. Superpipe lets you easily find the best combination of parameters by running a [grid search](./using/grid_search) over the parameter space. You can compare different approaches against each other and track your experiments with [Studio](./studio).

**Step 5: Deploy, monitor and further optimize**

Once you've deployed the winning pipeline to production, [Studio](./studio) helps monitor the accuracy, cost and speed of the pipeline. It helps you run auto-evaluations on a sub-sample of production data to make sure model drift or data drift aren't hurting. It also lets you easily backtest the newest models and techniques and compare them to production.

<br>
<p align="center"><b>The 5-step Superpipe workflow</b></p>
<p align="center"><img src="./overview.png" style="width: 800px;" /></p>

<hr>

While there are a number of general-purpose LLM libraries focused on different aspects of the above, Superpipe focuses on a specific problem (data extraction and classification) and the optimal workflow for the problem. It is designed with the following goals in mind:

!!! note "Superpipe design goals"

    - **Simplicity**: easy to get started because there few abstractions to learn.
    - **Unopinionated**: acts as connective tissue and abstracts boilerplate but leaves you in control of logic.
    - **Works with datasets**: works natively with `pandas` dataframes so you can evaluate and optimize over datasets.
    - **Parametric**: every aspect of the pipeline is exposed as a parameter, you can easily try different models or run hyperparameter searches.
    - **Plays well with others**: use your favorite LLM library or tool, including langchain, LlamaIndex, DSpy, etc.

## Next Steps

[**Getting Started**](./start) &mdash; for installation and basic usage examples.

[**Concepts**](./concepts) &mdash; to understand the core concepts behind Superpipe.

[**Why Superpipe?**](./why) &mdash; to understand whether Superpipe is right for you.

[**Examples**](./examples) &mdash; for more advanced examples and usage.
