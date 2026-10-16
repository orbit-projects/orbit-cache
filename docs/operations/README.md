# Orbit Cache: operations

`orbit-cache` contains no runtime cache service and has no provider configuration. Install a
separate adapter, such as `orbit-cache-redis`, and follow that package's connection, credential,
TLS, timeout, pool, and retry documentation. The capability package defines no `ORBIT_*` variables.

## Application wiring and ownership

Create one cache resource for the intended application scope. When using Orbit Core, register it
under `CACHE_DEPENDENCY_KEY` and use Core's managed-resource lifecycle so shutdown awaits
`aclose()`. For manual construction, the code that creates the provider owns closing it. Avoid
closing one client from both a plugin hook and an independent application hook.

Adapter docs should state whether operations can occur during startup, when the first network
connection is attempted, which calls are bounded by timeouts, and what happens to active calls when
shutdown starts. Confirm cleanup after startup failure as well as normal application shutdown.

## Cache data and capacity

The contract stores bytes, not Python objects. Define and version serialization at the caller
boundary. Avoid unbounded payloads and high-cardinality keys. Consult the provider for maximum key
and value sizes, TTL limits, connection pool capacity, eviction behavior, and memory policy.

A TTL requests expiration after a positive whole number of seconds; entries can be evicted earlier.
Without TTL, an entry has no contract-defined expiry. Do not use cache expiration as a substitute
for database retention or data deletion policy.

## Failure and recovery

Treat the cache as an optimization with a durable source of truth elsewhere. Design for a miss,
eviction, restart, failover, and complete cache unavailability. Set provider timeouts and pool
limits appropriate to request deadlines. Retry only when the operation and workload make the retry
safe; the contract does not provide idempotency keys or distributed consistency.

`CacheConfigurationError` indicates invalid caller configuration or input.
`CacheOperationError` indicates a failed backend operation or lifecycle use. Log a safe error
category and request context, not credentials, connection strings, raw backend text, or cached
values.

## Pre-release validation

In a disposable environment, exercise the selected adapter with backend restart, timeout, expired
and evicted entries, connection exhaustion, concurrent calls, cancellation during shutdown, and
credential rotation. Contract tests in this repository do not prove Redis or another backend's
availability, failover, or consistency behavior.
