from __future__ import annotations

import functools
import logging
import struct
import textwrap
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, FrozenSet, Hashable, Tuple, cast

import xxhash  # type: ignore

if TYPE_CHECKING:
    from typing import Protocol

else:
    Protocol = object


logger = logging.getLogger("charmonium.cache.determ_hash")


class Hasher(Protocol):
    def update(self, value: bytes) -> None:
        pass

    def digest(self) -> bytes:
        pass


def intdigest(hasher: Hasher) -> int:
    return int.from_bytes(hasher.digest(), byteorder="big")


@dataclass
class Config:
    # xxhash is one of the fastest hashes at the time of writing.
    # https://github.com/Cyan4973/xxHash
    hasher: Callable[[], Hasher] = xxhash.xxh128


config = Config()


# pylint: disable=invalid-name
def determ_hash(obj: Hashable) -> int:
    """A deterministic hash protocol.

        Python's |hash|_ will return different values across different
        processes. This hash is deterministic across:

        - different processes
        - different machines
        - different Python versions
        - different OSes

        ``determ_hash`` is based on the contents:

        - Primitive types (bytes, str, int, float, complex, None) are
          hashed by their value or a checksum of their value.

        - Immutable container types (tuple, frozenset) are hashed by the
          XOR of their elements.

    .. |hash| replace:: ``hash``
    .. _`hash`: https://docs.python.org/3/library/functions.html?highlight=hash#hash

    """
    hasher = config.hasher()
    logger.debug("determ_hash begin")
    _determ_hash(obj, hasher, 0)
    logger.debug("determ_hash end")
    return intdigest(hasher)


def _determ_hash(obj: Any, hasher: Hasher, level: int) -> None:
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(
            " ".join(
                [
                    level * " ",
                    type(obj).__name__,
                    textwrap.shorten(repr(obj), width=100),
                ]
            )
        )
    __determ_hash(obj, hasher, level)


@functools.singledispatch
def __determ_hash(obj: Any, hasher: Hasher, level: int) -> None:
    raise TypeError(f"{obj} ({type(obj)}) is not determ_hashable")


# pylint: disable=unused-argument
@__determ_hash.register(type(None))
def _(obj: None, hasher: Hasher, level: int) -> None:
    hasher.update(b"n")


# pylint: disable=unused-argument
@__determ_hash.register(bytes)
def _(obj: bytes, hasher: Hasher, level: int) -> None:
    # Naively, hash of empty containers output might map to 0.
    # But empty is a popular input.
    # If any two branches have 0 as a popular output, collisions ensue.
    # Therefore, I try to make each branch section have a different ouptut for empty/zero/nil inputs.
    # I do this by seeding each with the name of their type, `b"b(" + obj + b")"` and `b"t(" + hash(obj) + ")"`.
    # This way, the empty tuple and empty frozenset map to different outputs.
    # The end-parenthesis ensures that `((1, 2), 3)` and `((1, 2, 3))` map to different bytes.
    hasher.update(b"b(")
    hasher.update(obj)
    hasher.update(b")")


# pylint: disable=unused-argument
@__determ_hash.register
def _(obj: str, hasher: Hasher, level: int) -> None:
    hasher.update(b"s(")
    hasher.update(obj.encode())
    hasher.update(b")")


# pylint: disable=unused-argument
@__determ_hash.register
def _(obj: int, hasher: Hasher, level: int) -> None:
    hasher.update(b"i(")
    hasher.update(
        obj.to_bytes(
            length=(8 + (obj + (obj < 0)).bit_length()) // 8,
            byteorder="big",
            signed=True,
        )
    )
    hasher.update(")")


# pylint: disable=unused-argument
@__determ_hash.register
def _(obj: float, hasher: Hasher, level: int) -> None:
    # These types are fixed-size, so no need for `b"( + ... + b")"`.
    hasher.update(b"f")
    hasher.update(struct.pack("!d", obj))


@__determ_hash.register
def _(obj: complex, hasher: Hasher, level: int) -> None:
    hasher.update(b"c")
    _determ_hash(obj.imag, hasher, level + 1)
    _determ_hash(obj.real, hasher, level + 1)


@__determ_hash.register(tuple)
def _(obj: Tuple[Any], hasher: Hasher, level: int) -> None:
    hasher.update(b"t(")
    for elem in cast(Tuple[Hashable], obj):
        _determ_hash(elem, hasher, level + 1)
    hasher.update(b")")


@__determ_hash.register(frozenset)
def _(obj: FrozenSet[Any], hasher: Hasher, level: int) -> None:
    # The order of objects in a frozenset does not matter.
    # I would like to `hash(sorted(obj))`, but the elements of obj might not be comparable.
    # And `id(a) < id(b)` is not a stable comparison.
    # So I will `_determ_hash` each element to an integer, sort the integers, and hash that list.
    elem_hashes = []
    for elem in cast(FrozenSet[Any], obj):
        elem_hasher = config.hasher()
        _determ_hash(elem, elem_hasher, level + 1)
        elem_hashes.append(intdigest(elem_hasher))
    _determ_hash(tuple(sorted(elem_hashes)), hasher, level + 1)


@__determ_hash.register(type(...))
def _(obj: Any, hasher: Hasher, level: int) -> None:
    hasher.update(b".")
