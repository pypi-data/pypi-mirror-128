
from typing import Pattern

from ..utils import ParserError
from redengine.core.time.base import PARSERS, TimePeriod

def add_time_parser(d):
    """Add a parsing instruction to be used for parsing a 
    string to condition.

    Parameters
    ----------
    s : str
        Exact string (if regex=False) or regex (if regex=True)
        to be matched. If regex and has groups, the groups are
        passed to func.
    func : Callable
        Function that should return a condition. 
    regex : bool, optional
        Whether the 's' is a regex or exact string, 
        by default True
    """
    PARSERS.update(d)

def parse_time_item(s:str):
    "Parse one condition"
    for statement, parser in PARSERS.items():
        if isinstance(statement, Pattern):
            res = statement.fullmatch(s)
            if res:
                args = ()
                kwargs = res.groupdict()
                break
        else:
            if s == statement:
                args = (s,)
                kwargs = {}
                break
    else:
        raise ParserError(f"Could not find parser for string {repr(s)}.")

    if isinstance(parser, TimePeriod):
        return parser
    else:
        return parser(**kwargs)
