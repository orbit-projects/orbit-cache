# Orbit Cache: architecture and boundaries

## Responsibility

`orbit-cache` is a small, provider-neutral asynchronous cache capability. It defines the API an
application can depend on without requiring a cache server or vendor SDK. The separate
`orbit-cache-redis` package adapts Redis to this contract; installing Orbit Core does not install either
package. The distribution requires Python 3.11 through 3.14 and is currently pre-alpha.

## Declared dependencies

The following dependency declarations come from the checked-in manifests. Optional groups and development dependencies are called out separately.

### `pyproject.toml`
- No dependencies declared.
- Optional `dev` group: `pytest>=8,<10`, `pytest-asyncio>=0.24,<2`, `ruff>=0.8,<1`, `mypy>=1.13,<2`.

Declared dependencies do not mean that optional providers or services are bundled with this package.

## Implementation layout

Representative implementation files in this checkout:

- `src/orbit_cache/__init__.py`
- `src/orbit_cache/contracts.py`
- `src/orbit_cache/errors.py`

## Public contract and scope

## Contract

Install the capability only when an application or adapter needs its shared API:

```bash
python -m pip install orbit-cache
```

`AsyncCache` defines `get`, `set`, `delete`, and `aclose`. Keys are non-empty strings and values
are bytes. A missing key returns `None`; `delete` reports whether the key existed. A TTL is either
omitted or a positive integer number of seconds. The contract intentionally does not define
serialization, cache-aside behavior, eviction, consistency, or distributed locking.

Application code can depend on the protocol instead of a provider implementation:

```python
from orbit_cache import AsyncCache


async def load_profile(cache: AsyncCache, user_id: str) -> bytes | None:
    return await cache.get(f"profile:{user_id}")
```

Resolve an application-registered implementation with `CACHE_DEPENDENCY_KEY` when using Orbit's
container. The application or adapter that creates a cache owns its lifetime and must call
`aclose()` during shutdown; a provider plugin can register and close that resource for the app.

Implementations should raise `CacheConfigurationError` for invalid arguments and
`CacheOperationError` for backend failures. Do not expose provider exceptions or credentials through
these errors, and allow task cancellation to propagate unchanged. `orbit-cache-redis` is one optional
adapter; it is not installed as a dependency of this capability package.

## Boundary rules

Keep provider SDKs, credentials, transports, and provider-specific error translation in provider adapters. Keep reusable capability contracts in the matching capability package and lifecycle orchestration in Core. Apply the relevant layer for this repository and preserve the dependency direction shown above.
