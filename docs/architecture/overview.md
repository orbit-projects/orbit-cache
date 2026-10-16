# Orbit Cache: architecture and contract

## Package boundary

`orbit-cache` defines the provider-neutral asynchronous `AsyncCache` protocol and shared error
types. It has no runtime dependencies and does not connect to a cache server. Provider packages own
SDKs, credentials, transport, pooling, timeout settings, and backend failures.

```text
application code ───── AsyncCache ───── orbit-cache (contract and errors)
                          ▲
                          │ implementation
                   orbit-cache-redis ─── redis-py ─── Redis
```

Core can use `CACHE_DEPENDENCY_KEY` (`"orbit.cache"`) to make an application-scoped implementation
available through its container. Core does not install or choose a provider. The application or
provider plugin that creates the cache owns its lifecycle and calls `aclose()` during shutdown.

## Data and expiry semantics

Keys are non-empty strings and values are bytes. A missing or expired key returns `None`. `set`
replaces the existing value. `ttl=None` requests no expiration; a positive whole-second TTL
requests expiration after that duration, but normal cache eviction may remove the entry earlier.
`delete` returns whether the entry existed when deletion was applied.

Serialization is deliberately outside this package. Applications should encode structured data
with an explicit, versioned format and handle decode failures at their own boundary. Never treat a
cache as the durable source of truth for application data.

## Guarantees and non-guarantees

The shared interface is one-key CRUD only. It does not provide compare-and-set, atomic multi-key
transactions, key scans, eviction controls, cache-aside or write-through behavior, consistent
replicas, distributed locks, or durable persistence. Do not infer ordering, request coalescing, or
cross-instance coherence. Use a capability that explicitly defines those semantics when an
application depends on them.

Maximum key/value sizes, TTL ceilings, expiration precision, eviction, consistency, and connection
pool behavior are provider-specific. Adapters must document their bounds; applications should
choose limits suitable for their data and workload.

## Errors and cancellation

Invalid input should raise `CacheConfigurationError`. Backend failures, calls against a closed
instance, and shutdown failures should use `CacheOperationError`. Provider credentials and raw
backend messages must not appear in the public error message. Task cancellation propagates as
`asyncio.CancelledError` rather than being rewritten as an ordinary cache failure.

## Lifecycle

An implementation owns only the resources documented by that adapter. Successful `aclose()` calls
should be safe to repeat. Adapters should reject new operations after shutdown begins and document
whether close drains in-flight operations, how cancellation interacts with cleanup, and how a
failed close is surfaced. Register one application-scoped resource with Core instead of managing
duplicate cache clients from independent lifecycle hooks.

## Source layout and status

- `src/orbit_cache/contracts.py`: public protocol and dependency registration key.
- `src/orbit_cache/errors.py`: shared cache exception hierarchy.
- `src/orbit_cache/__init__.py`: supported package exports.

The distribution is in alpha and declares Python `>=3.11,<3.15`. Its API may change before a
stable release. See `pyproject.toml` for authoritative version and dependency metadata.
