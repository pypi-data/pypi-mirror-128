from functools import partial

from .func import FuncCond
from .task import *
from .scheduler import *
from .time import *
from .git import *
from .parameter import ParamExists, IsEnv
from .meta import TaskCond

from redengine.core.condition import PARSERS, CLS_CONDITIONS
from redengine.core.condition import AlwaysFalse, AlwaysTrue, All, Any, Not

true = AlwaysTrue()
false = AlwaysFalse()

def _from_period_task_has(cls, span_type=None, inverse=False, **kwargs):
    from redengine.time.construct import get_full_cycle, get_between, get_after, get_before
    from redengine.time import TimeDelta

    period_func = {
        "between": get_between,
        "after": get_after,
        "before": get_before,
        "starting": get_full_cycle,
        None: get_full_cycle,
        "every": TimeDelta,
        "on": get_on,

        "past": TimeDelta,
    }[span_type]

    task = kwargs.pop("task", None)
    period = period_func(**kwargs)

    cls_kwargs = {"task": task} if task is not None else {}
    if inverse:
        return Not(cls(period=period, **cls_kwargs))
    else:
        return cls(period=period, **cls_kwargs)


def _set_is_period_parsing():
    from redengine.core.time import PARSERS as _TIME_PARSERS
    
    from functools import partial

    def _get_is_period(period_constructor, *args, **kwargs):
        period = period_constructor(*args, **kwargs)
        return IsPeriod(period=period)

    PARSERS.update(
        {
            parsing: partial(_get_is_period, period_constructor=parser)
            for parsing, parser in _TIME_PARSERS.items()
        }
    )

def _set_task_has_parsing():
    clss = [
        ("failed", TaskFailed),
        ("succeeded", TaskSucceeded),
        ("finished", TaskFinished),
        ("terminated", TaskTerminated),
        ("inacted", TaskInacted),
        ("started", TaskStarted)
    ]
    for (action, cls) in clss:
        func = partial(_from_period_task_has, cls=cls)
        for prefix in ("", r"task '(?P<task>.+)' "):
            PARSERS.update(
                {
                    re.compile(fr"{prefix}has {action}"): cls,
                    re.compile(fr"{prefix}has {action} (?P<type_>this month|this week|today|this hour|this minute) (?P<span_type>starting) (?P<start>.+)"): func,
                    re.compile(fr"{prefix}has {action} (?P<type_>this month|this week|today|this hour|this minute) (?P<span_type>between) (?P<start>.+) and (?P<end>.+)"): func,
                    re.compile(fr"{prefix}has {action} (?P<type_>this month|this week|today|this hour|this minute) (?P<span_type>after) (?P<start>.+)"): func,
                    re.compile(fr"{prefix}has {action} (?P<type_>this month|this week|today|this hour|this minute) (?P<span_type>before) (?P<end>.+)"): func,
                    re.compile(fr"{prefix}has {action} (?P<type_>this month|this week|today|this hour|this minute)"): func,
                    re.compile(fr"{prefix}has {action} (?P<type_>this month|this week|today|this hour|this minute) (?P<span_type>on) (?P<start>.+)"): func,
                    re.compile(fr"{prefix}has {action} (in )?past (?P<past>.+)"): partial(func, span_type='past'),
                }
            )

def _set_scheduler_parsing():
    cls = SchedulerStarted
    func = partial(_from_period_task_has, cls=cls)
    PARSERS.update(
        {
            re.compile(fr"scheduler has run over (?P<past>.+)"): partial(func, span_type='past', inverse=True),
            re.compile(fr"scheduler started (?P<past>.+) ago"): partial(func, span_type='past'),
        }
    )

_set_is_period_parsing()
_set_task_has_parsing()
_set_scheduler_parsing()