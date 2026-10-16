# Copyright 2026-present Orbit Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Typed asynchronous cache contract for Orbit applications and backend adapters."""

from typing import Protocol, runtime_checkable

CACHE_DEPENDENCY_KEY = "orbit.cache"


@runtime_checkable
class AsyncCache(Protocol):
    """Minimal async key/value cache interface with explicit resource ownership.

    Keys are non-empty strings, values are bytes, and TTLs are positive whole seconds. A missing
    or expired key returns ``None``. ``set`` replaces a key's prior value; when ``ttl`` is omitted,
    the replacement has no expiry. A supplied TTL requests expiration after that many whole
    seconds; cache eviction may still remove the entry earlier. ``delete`` reports whether the key
    existed at the time of deletion.

    Implementations should raise ``CacheConfigurationError`` for invalid arguments and
    ``CacheOperationError`` for backend failures, closed-resource use, or shutdown failures. Those
    errors must not expose credentials or raw provider messages. Task cancellation propagates
    unchanged. This contract does not promise durability, atomic multi-key operations, ordering,
    serialization, cache-aside behavior, eviction policy, consistency across replicas, or
    distributed locking. Callers must treat cache contents as disposable and use a database or
    other durable store as the source of truth.

    The creator owns the cache instance and must call ``aclose`` during shutdown. Implementations
    should stop accepting new operations, finish or safely cancel in-flight work according to their
    documented policy, and make successful repeated close calls safe. Resource limits and maximum
    key/value sizes are provider-specific and must be documented by each implementation.
    """

    async def get(self, key: str) -> bytes | None:
        """Return the stored bytes, or ``None`` when the key is missing or expired.

        Implementations reject an empty or non-string key with ``CacheConfigurationError``. A
        returned ``bytes`` value is the value stored by ``set``; serialization belongs to the
        caller or a higher-level capability.
        """

    async def set(self, key: str, value: bytes, *, ttl: int | None = None) -> None:
        """Replace a key with bytes, optionally requesting expiry after whole seconds.

        Reject empty/non-string keys, non-bytes values, booleans, and non-positive TTL values with
        ``CacheConfigurationError``. ``ttl=None`` means no expiry. Backend size limits and actual
        expiry precision are implementation-specific and should be documented by the adapter.
        """

    async def delete(self, key: str) -> bool:
        """Remove a key and return whether it existed when the deletion was applied.

        Reject empty or non-string keys with ``CacheConfigurationError``. The return value does
        not imply coordination with concurrent operations on other cache instances.
        """

    async def aclose(self) -> None:
        """Release resources owned by this cache instance.

        After a successful close, repeated calls should be safe. Operations attempted after close
        should raise ``CacheOperationError``. Concrete adapters must document whether shutdown
        drains active operations and how cancellation or provider cleanup failures are reported.
        """


__all__ = ["AsyncCache", "CACHE_DEPENDENCY_KEY"]
