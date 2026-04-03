---
name: "testing"
description: "How to write tests"
---

We use Python unittest framework.

Assess what type of test is expected :

- e2e test will run the actual CLI tool which costs money, run only if needed
- display test will simply print messages in the console (the current project is a CLI tool), do not add assertion
- unit test ar using the unittest framework, not pytest
