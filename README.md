# Orbit Cache

`orbit-cache` is a small, provider-neutral asynchronous cache capability. It defines the API an
application can depend on without requiring a cache server or vendor SDK. The separate
`orbit-cache-redis` package adapts Redis to this contract; installing Orbit Core does not install either
package. The distribution requires Python 3.11 through 3.14 and is currently pre-alpha.

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

## Documentation

The package-specific guides cover [architecture](docs/architecture/overview.md), [operations and security](docs/operations/README.md), and [development](docs/development/README.md), with [security guidance](docs/security/overview.md). The [documentation index](docs/README.md) links to the full package overview and project policies.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
mypy
```

Licensed under Apache-2.0.

