# SuperPipe - build, evaluate and optimize LLM pipelines

_A lightweight framework for building, evaluating and optimizing data transformation and data extraction pipelines using LLMs. Designed for simplicity, rapid prototyping, evaluation and optimization._

---

[Star us on Github!](https://github.com/villagecomputing/superpipe) &nbsp; [Read the docs](https://villagecomputing.github.io/superpipe/)

[![Twitter Follow](https://img.shields.io/twitter/follow/villagecompute?style=social)](https://twitter.com/villagecompute)
[![Downloads](https://img.shields.io/pypi/dm/superpipe-py.svg)](https://pypi.python.org/pypi/superpipe-py)

🚧 This readme and the docs are under construction 🚧

LLMs can make your treasure trove of unstructured data useful if only you could transform it into structured, or extract key fields from it. Today, building LLM-powered pipelines is difficult because LLMs are unpredictable. Unlike traditional software, you can't simply write unit and integration tests that confirm the correctness of your code.

With LLMs you need a different approach: you need to evaluate your code on a dataset, and tune the code to find the right tradeoff between:

- Accuracy
- Cost
- Latency

SuperPipe is an extremely lightweight framework that helps you build these pipelines such that you can:

- Easily run them on a dataset (not just a single data point)
- Keep track of token usage, cost and latency
- Evaluate accuracy against ground truth
- Evaluate the correctness of each step in the pipeline
- Easily parametrize each step (eg. model choice) so you can tune the parameters to optimize performance

## Get Started

Installing SuperPipe is a breeze. Simply run `pip install superpipe-py` in your terminal.

## License

This project is licensed under the terms of the MIT License.

# Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

<a href="https://github.com/villagecomputing/superpipe/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=villagecomputing/superpipe" />
</a>
