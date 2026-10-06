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
    key returns ``None``. ``delete`` reports whether a key existed. Implementations should raise
    ``CacheConfigurationError`` for invalid arguments and ``CacheOperationError`` for backend
    failures, while allowing task cancellation to propagate unchanged.
    """

    async def get(self, key: str) -> bytes | None:
        """Return the stored bytes, or ``None`` when the key does not exist."""

    async def set(self, key: str, value: bytes, *, ttl: int | None = None) -> None:
        """Store bytes, optionally expiring them after ``ttl`` seconds."""

    async def delete(self, key: str) -> bool:
        """Remove a key and return whether it existed."""

    async def aclose(self) -> None:
        """Release resources owned by this cache instance; repeated calls should be safe."""


__all__ = ["AsyncCache", "CACHE_DEPENDENCY_KEY"]
