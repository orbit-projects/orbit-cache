# Orbit Cache: security

The cache protocol does not authenticate callers or encrypt values. Security for a connected cache
is determined by the provider adapter, backend configuration, application authorization, and
network policy.

## Keys, values, and logs

Treat keys and values as potentially sensitive. Do not put access tokens, passwords, session
secrets, or personal data in keys. Minimize sensitive cached fields and set an explicit TTL where
retention should be bounded. Encrypt sensitive values at the application boundary when the
deployment's trust model requires it; the shared API stores opaque bytes and applies no encryption.

Never log cache values. Avoid logging full keys if they contain user identifiers or tenant data.
Provider errors must be normalized so messages do not reveal passwords, URLs, raw backend details,
or payloads. Task cancellation should remain cancellation rather than being hidden as a cache
failure.

## Backend access

Use a dedicated cache identity with only required commands and keyspace access. Keep credentials in
a secret manager and rotate them without committing them to source or build artifacts. Use TLS
with certificate verification when the backend is remote, isolate the cache on a private network,
and configure firewall or network policy to restrict access to approved workloads. Review
provider-specific ACLs, pool limits, persistence, backup, and failover settings independently.

Cache contents are disposable but can still contain sensitive data. Apply appropriate backend
encryption, retention, eviction, and access logging controls; do not infer deletion or durability
guarantees from TTL alone.

## Vulnerability reporting

Follow the repository [security policy](../../SECURITY.md) for private reporting. This guidance
describes the capability boundary and is not an audit of a provider or deployment.
