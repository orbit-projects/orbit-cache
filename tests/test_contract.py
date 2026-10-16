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
"""Sanity checks for the public capability's type and error boundaries."""

from orbit_cache import (
    CACHE_DEPENDENCY_KEY,
    AsyncCache,
    CacheConfigurationError,
    CacheError,
    CacheOperationError,
)


class _StructuralCache:
    """Minimal object showing that adapters need not inherit a framework implementation."""

    async def get(self, key: str) -> bytes | None:
        raise NotImplementedError

    async def set(self, key: str, value: bytes, *, ttl: int | None = None) -> None:
        raise NotImplementedError

    async def delete(self, key: str) -> bool:
        raise NotImplementedError

    async def aclose(self) -> None:
        raise NotImplementedError


def test_cache_contract_is_runtime_checkable() -> None:
    """Adapters can be structurally checked without inheriting a framework base class."""
    assert getattr(AsyncCache, "_is_runtime_protocol", False)
    assert isinstance(_StructuralCache(), AsyncCache)


def test_dependency_key_is_public_and_stable() -> None:
    """Core containers and adapters share the documented cache registration key."""
    assert CACHE_DEPENDENCY_KEY == "orbit.cache"


def test_errors_share_stable_base_type() -> None:
    """Callers can catch all capability errors or classify config/backend failures."""
    assert issubclass(CacheConfigurationError, CacheError)
    assert issubclass(CacheOperationError, CacheError)
