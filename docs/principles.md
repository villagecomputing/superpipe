# Principles

**Principle 1: Your LLM pipeline is only as good as your data.** &mdash; This is why Superpipe is designed from the ground up to work with datasets, not just single inputs.

**Principle 2: Abstract the boilerplate and the glue (chaining, evaluating, inspecting), NOT the logic.** &mdash; Superpipe abstracts away tedious things like calculating cost, speed, and accuracy. It lets you glue together existing building blocks from other libraries and your own logic.

**Principle 3: You can't optimize what you can't evaluate. You can't evaluate without ground truth.**

**Principle 4: You can't optimize what you can't inspect.** &mdash; Losses can happen at any step, you need to quickly understand which step caused the loss.

**Principle 5: Build once, experiment many times.**

**Principle 6: Spend your time learning new ML techniques, not new Python abstractions.**

**Principle 7: Don't f\* with my prompts.**
