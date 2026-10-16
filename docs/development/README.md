# Orbit Cache: development

This repository defines the shared asynchronous cache contract, not a backend. Keep provider SDKs
and network behavior in provider adapter repositories. Contract changes affect every adapter, so
review the workspace consumers before changing method signatures or semantics.

## Local setup and checks

From this repository's root:

```bash
python -m pip install -e '.[dev]' build
pytest
ruff check src tests
ruff format --check src tests
mypy
python -m build
```

Tests in this repository check public typing, exports, and structural compatibility without a cache
service. They do not verify provider-specific TTL precision, resource cleanup, or network failure
handling. Run the corresponding adapter tests separately when changing a shared contract.

## Contract contribution guidance

- Keep values opaque `bytes` and avoid adding serialization assumptions to this layer.
- Document a guarantee only when every conforming adapter can meet it. Call out limits that vary by
  backend instead of implying uniform behavior.
- Preserve cancellation as cancellation and keep provider error details out of public exceptions.
- Add tests for protocol shape, exported names, defaults, and error inheritance when those change.
- Update the README, docstrings, architecture, operations, security, and development guides for a
  user-visible contract change. Include migration notes for every affected adapter.

Follow [CONTRIBUTING.md](../../CONTRIBUTING.md), project governance, code of conduct, and security
policy. Keep examples runnable and fixtures free of secrets or real cache contents. Distinguish
local validation from hosted CI and provider release evidence.
