"""value_error.py

Collection of functions useful in parsing ValueError messages and
providing a more detailed explanation.
"""

import inspect
import re
from types import FrameType
from typing import Any, Optional, Tuple

from .. import info_variables, token_utils, utils
from ..core import TracebackData
from ..ft_gettext import current_lang
from ..typing import CauseInfo

convert_type = info_variables.convert_type
parser = utils.RuntimeMessageParser()
_ = current_lang.translate


def _unpacking() -> str:
    return _(
        "Unpacking is a convenient way to assign a name,\n"
        "to each item of an iterable.\n"
    )


def get_iterable(code: str, frame: FrameType) -> Tuple[Any, Optional[str]]:
    """gets an iterable object and its type as a string."""
    try:
        # As a ValueError exception has been raised, Python has already evaluated
        # all the relevant code parts. Thus, using eval should be completely safe.
        obj = utils.eval_expr(code, frame)
    except Exception:  # noqa
        return None, None

    if isinstance(obj, dict):
        iterable = "dict"
    elif isinstance(obj, list):
        iterable = "list"
    elif isinstance(obj, set):
        iterable = "set"
    elif isinstance(obj, str):
        iterable = "str"
    elif isinstance(obj, tuple):
        iterable = "tuple"
    else:
        iterable = None
    return obj, iterable


@parser.add
def not_enough_values_to_unpack(
    message: str, frame: FrameType, tb_data: TracebackData
) -> CauseInfo:
    pattern1 = re.compile(r"not enough values to unpack \(expected (\d+), got (\d+)\)")
    match1 = re.search(pattern1, message)
    pattern2 = re.compile(
        r"not enough values to unpack \(expected at least (\d+), got (\d+)\)"
    )
    match2 = re.search(pattern2, message)
    if match1 is None and match2 is None:
        return {}

    match = match1 if match2 is None else match2

    nb_names = match.group(1)
    length = match.group(2)

    if tb_data.bad_line.count("=") != 1:
        cause = _unpacking() + _(
            "In this instance, there are more names ({nb_names})\n"
            "than {length}, the length of the iterable.\n"
        ).format(nb_names=nb_names, length=length)
        return {"cause": cause}

    _lhs, rhs = tb_data.bad_line.split("=")
    obj, iterable = get_iterable(rhs, frame)
    if obj is None or iterable is None:
        cause = _unpacking() + _(
            "In this instance, there are more names ({nb_names})\n"
            "than {length}, the length of the iterable.\n"
        ).format(nb_names=nb_names, length=length)
        return {"cause": cause}

    cause = _unpacking() + _(
        "In this instance, there are more names ({nb_names})\n"
        "than the length of the iterable, {iter_type} of length {length}.\n"
    ).format(nb_names=nb_names, iter_type=convert_type(iterable), length=length)
    return {"cause": cause}


@parser.add
def too_many_values_to_unpack(
    message: str, frame: FrameType, tb_data: TracebackData
) -> CauseInfo:
    pattern = re.compile(r"too many values to unpack \(expected (\d+)\)")
    match = re.search(pattern, message)
    if match is None:
        return {}

    nb_names = match.group(1)

    if tb_data.bad_line.count("=") != 1:
        cause = _unpacking() + _(
            "In this instance, there are fewer names ({nb_names})\n"
            "than the length of the iterable.\n"
        ).format(nb_names=nb_names)
        return {"cause": cause}

    _lhs, rhs = tb_data.bad_line.split("=")

    obj, iterable = get_iterable(rhs, frame)
    if obj is None or iterable is None or not hasattr(obj, "__len__"):
        cause = _unpacking() + _(
            "In this instance, there are fewer names ({nb_names})\n"
            "than the length of the iterable.\n"
        ).format(nb_names=nb_names)
        return {"cause": cause}

    cause = _unpacking() + _(
        "In this instance, there are fewer names ({nb_names})\n"
        "than the length of the iterable, {iter_type} of length {length}.\n"
    ).format(nb_names=nb_names, iter_type=convert_type(iterable), length=len(obj))
    return {"cause": cause}


# TODO: complete the work below; note noqa to be removed


@parser.add
def invalid_literal_for_int(
    message: str, _frame: FrameType, _tb_data: TracebackData
) -> CauseInfo:
    pattern = re.compile(r"invalid literal for int\(\) with base (\d+): '(.*)'")
    match = re.search(pattern, message)
    if match is None:
        return {}
    base, value = int(match.group(1)), match.group(2)
    if not value:
        cause = _(
            "`int()` expects an argument that looks like a number in base `{base}`\n"
            "but you gave it an empty string.\n"
        ).format(base=base)
        return {"cause": cause}

    begin_cause = _(
        "`{value}` is an invalid argument for `int()` in base `{base}`.\n"
    ).format(value=repr(value), base=base)

    try:
        _value = float(value)  # noqa
        cause = _convert_to_float(value)
        cause["cause"] = begin_cause + cause["cause"]
        return cause
    except ValueError:
        pass

    valid = "0123456789abcdefghijiklmnopqrstuvwxyz"

    if 2 <= base <= 10:
        cause = _(
            "In base `{base}`, `int()` is most often use to convert a string\n"
            "containing the digits `0` to `{max_n}` into an integer.\n"
        ).format(base=base, max_n=valid[base - 1])
    elif base == 11:
        cause = _(
            "In base `11`, `int()` is most often use to convert a string\n"
            "containing the digits `0` to `9` and the letter `'a'` into an integer.\n"
        )
    elif base <= 36:
        cause = _(
            "In base `base`, `int()` is most often use to convert a string\n"
            "containing the digits `0` to `9` and the letters\n"
            "from `'a'` to `'{max_n}'` into an integer.\n"
        ).format(base=base, max_n=valid[base - 1])
    elif base == 0:
        cause = _(
            "When base `0` is specified, `int()` expects the string argument to\n"
            "represent an integer literal.\n"
        )
    else:
        return {}

    return {"cause": begin_cause + cause}


def _convert_to_float(value: Any) -> CauseInfo:
    hint = _("You need to convert `'{value}'` to a float first.\n").format(value=value)
    cause = _(
        "The string `'{value}'` needs to be first converted using `float()`\n"
        "before the result can be converted into an integer using `int()`.\n"
    ).format(value=value)
    return {"cause": cause, "suggest": hint}


@parser.add
def date_month_must_be_between_1_and_12(
    message: str, _frame: FrameType, _tb_data: TracebackData
) -> CauseInfo:
    if message != "month must be in 1..12":
        return {}

    hint = _("Did you specify an invalid month?\n")
    cause = _(
        "I am guessing that you specify an invalid value for a month\n"
        "in a `date` object. Valid values are integers, from 1 to 12.\n"
    )
    return {"cause": cause, "suggest": hint}


@parser.add
def slots_conflicts_with_class_variable(
    value: str, frame: FrameType, tb_data: TracebackData
) -> CauseInfo:
    pattern = r"'(.*)' in __slots__ conflicts with class variable"
    match = re.search(pattern, str(value))
    if not match:
        return {}
    var = match.group(1)
    cause = _(
        "The name `{var}` is used both as the name of a class variable\n"
        "and as a string item in the class `__slots__`;\n"
        "this is not allowed.\n"
    ).format(var=var)
    return {"cause": cause}


@parser.add
def unrecognized_message(
    _value: str, frame: FrameType, tb_data: TracebackData
) -> CauseInfo:
    """This attempts to provide some help when a message is not recognized."""
    bad_line = tb_data.bad_line.strip()
    if bad_line.startswith("raise ") or bad_line.startswith("raise\t"):
        try:
            name = inspect.getframeinfo(frame).function
            fn_obj = frame.f_globals[name]
        except Exception:
            return {}
    else:
        all_objects = info_variables.get_all_objects(bad_line, frame)["name, obj"]
        callables = []
        for name, obj in all_objects:
            if callable(obj):
                callables.append((name, obj))
        if not callables:
            return {}

        tokens = token_utils.get_significant_tokens(tb_data.bad_line)
        name, fn_obj = callables[0]
        if name != tokens[0]:
            return {}

    cause = _(
        "I do not recognize this error message.\n"
        "I am guessing that the problem is with the function `{name}`.\n"
    ).format(name=name)

    if hasattr(fn_obj, "__doc__") and fn_obj.__doc__ is not None:
        cause += _("Its docstring is:\n\n`'''{docstring}'''`\n").format(
            docstring=fn_obj.__doc__
        )
    else:
        cause += _("I have no more information.\n")
    return {"cause": cause}


@parser.add
def time_strptime_incorrect_format(
    value: str, _frame: FrameType, _tb_data: TracebackData
) -> CauseInfo:
    pattern = r"time data '(.*)' does not match format '(.*)'"
    match = re.search(pattern, str(value))
    if not match:
        return {}
    cause = _(
        "The value you gave for the time is not in the format you specified.\n"
        "Make sure to use the same separator between items\n"
        "(for example, between day and month) and keep the order the same\n"
        "in both the data provided and the format you specified.\n"
        "The following table might be useful:\n"
        "https://docs.python.org/3/library/time.html#time.strftime\n"
        "The following site might also be useful: https://www.strfti.me/\n"
    )
    return {"cause": cause}
