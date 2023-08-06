import argparse
import enum
import dataclasses
import functools
import logging
from typing import Type, TypeVar, Optional

import okome
import serde.compat
import serde.de

T = TypeVar("T")

log = logging.getLogger("oppapi")


def _generate_parser(cls) -> argparse.ArgumentParser:
    """
    Generate `argparse.ArgumentParser` from a class declaration.
    """
    log.debug("Generating command line parser.")

    class_comment = okome.parse(cls).comment
    if class_comment:
        parser_description = "\n".join(class_comment)
    else:
        parser_description = ""

    parser = argparse.ArgumentParser(description=parser_description)

    # Inspect fields of dataclass.
    # `f`  conveys pyserde field attributes as well as dataclass's
    # `of` conveys docstring comments declared in dataclass fields
    for f, of in zip(serde.de.defields(cls), okome.fields(cls)):
        log.debug(f"Inspecting field: {f}, {of}")

        if serde.compat.is_opt(f.type):
            typ = serde.compat.get_args(f.type)[0]
        else:
            typ = f.type

        opts = {}
        if not isinstance(f.default, dataclasses._MISSING_TYPE):
            opts["default"] = f.default
        if of.comment:
            opts["help"] = " ".join(of.comment)
        if serde.compat.is_list(typ):
            opts["nargs"] = "+"
        elif serde.compat.is_tuple(typ):
            opts["nargs"] = len(serde.compat.get_args(typ))
        elif serde.compat.is_enum(typ):
            opts["choices"] = [e.value for e in typ]

        if _determine_option(f):
            _add_option(parser, f, **opts)
        else:
            _add_argument(parser, f, **opts)

    return parser


def _add_argument(parser: argparse.ArgumentParser, f: serde.de.DeField, **opts):
    """
    Add positional argument to parser.
    """
    command = _command(f)
    typ = _get_type_for_argparse(f.type)
    if typ:
        opts["type"] = typ

    log.debug(f"Add argument to parser: command={command}, type={typ}, opts={opts}")
    parser.add_argument(command, **opts)


def _add_option(parser: argparse.ArgumentParser, f: serde.de.DeField, **opts):
    """
    Add optional argument to parser.
    """
    short = _short(f)
    long = _long(f)
    typ = _get_type_for_argparse(f.type)
    if typ is bool:
        opts["action"] = "store_true"
    elif typ:
        # NOTE: Specifying both "type" and "action" raises an error
        opts["type"] = typ

    opts["required"] = f.metadata.get("oppapi_required", False)

    opts["dest"] = f.name

    log.debug(f"Add option to parser: short={short}, long={long}, type={typ}, opts={opts}")
    parser.add_argument(short, long, **opts)


def _get_type_for_argparse(typ: Type):
    """
    Get type supported by `argparse.Parser`.

    * Get inner type T from Optional[T]
    * Use `str` for Date, Time and DateTime
    * Use `str` for other string serializable types e.g. `pathlib.Path`
    * Use inner type T from List[T]
    """
    if serde.compat.is_opt(typ):
        return _get_type_for_argparse(serde.compat.get_args(typ)[0])
    if serde.compat.is_list(typ):
        return serde.compat.get_args(typ)[0]
    if serde.compat.is_tuple(typ):
        return None
    elif typ in serde.de.StrSerializableTypes or typ in serde.de.DateTimeTypes:
        return str
    elif issubclass(typ, enum.IntEnum):
        return int
    elif issubclass(typ, enum.Enum):
        return str
    else:
        return typ


def _determine_option(f: serde.de.DeField):
    return (
        f.metadata.get(
            "oppapi_option",
        )
        or serde.compat.is_opt(f.type)
    )


def _snake_to_kebab(s: str) -> str:
    return s.replace("_", "-")


def _command(f: serde.de.DeField) -> str:
    return _snake_to_kebab(f.conv_name("snakecase"))


def _short(f: serde.de.DeField) -> str:
    return f.metadata.get("oppapi_short") or "-" + f.conv_name("snakecase")[0]


def _long(f: serde.de.DeField) -> str:
    return f.metadata.get("oppapi_long") or "--" + _snake_to_kebab(f.conv_name("snakecase"))


def from_args(cls: Type[T]) -> T:
    parser = _generate_parser(cls)
    args = parser.parse_args()
    args = vars(args)  # type: ignore
    log.debug(f"Parsed: {args}")
    return serde.from_dict(cls, args)


def oppapi(_cls):
    @functools.wraps(_cls)
    def wrap(cls):
        if not dataclasses.is_dataclass(cls):
            cls = dataclasses.dataclass(cls)
        serde.deserialize(cls, reuse_instances_default=False)
        return cls

    if _cls is None:
        return wrap  # type: ignore
    else:
        return wrap(_cls)


@dataclasses.dataclass
class Field(serde.de.DeField):
    """
    Represents a field in oppapi class.

    It inherits `dataclasses` and `pyserde` attributes.
    """
    option: bool = False


def field(*args, short: Optional[str] = None, long: Optional[str] = None,
          required: bool = False, option=False,
          metadata=None, **kwargs):
    """
    Declare a field with parameters.
    """
    if not metadata:
        metadata = {}
    metadata["oppapi_option"] = option

    if short:
        metadata["oppapi_short"] = short
    if long:
        metadata["oppapi_long"] = long

    metadata["oppapi_required"] = required

    return dataclasses.field(*args, metadata=metadata, **kwargs)


def argument(*args, short=None, long=None, **kwargs):
    return field(*args, option=False, short=short, long=long, **kwargs)


def option(*args, short=None, long=None, **kwargs):
    return field(*args, option=True, short=short, long=long, **kwargs)
