# Principles

To be expanded upon.

1. Your LLM pipeline is only as good as your data. This is why Superpipe is designed from the ground up to work with datasets, not just single inputs.
2. Abstract the boilerplate (cost, speed, accuracy calculation) and the glue (chaining, evaluating, inspecting), NOT the logic.
3. You can't optimize what you can't evaluate. You can't evaluate without ground truth.
4. You can't optimize what you can't inspect. Losses can happen at any step, you need to quickly understand which step caused the loss.
5. Build once, experiment many times.
6. Spend your time learning new ML techniques, not new Python abstractions.
7. We don't f\* with your prompts.
