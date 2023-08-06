import datetime
import time
from abc import abstractmethod
from typing import Callable, Dict, List, Pattern, Union
import itertools

import pandas as pd

from redengine.core.meta import _add_parser


PARSERS: Dict[Union[str, Pattern], Union[Callable, 'TimePeriod']] = {}

class _TimeMeta(type):
    def __new__(mcs, name, bases, class_dict):
        cls = type.__new__(mcs, name, bases, class_dict)
        # Add the parsers
        _add_parser(cls, container=PARSERS)
        return cls


class TimePeriod(metaclass=_TimeMeta):
    """Base for all classes that represent a time period.

    Time period is a period in time with a start and an end.
    These are useful to determine whether an event took 
    place in a specific time span or whether current time 
    is in a given time span.
    """

    resolution = pd.Timestamp.resolution
    min = pd.Timestamp.min
    max = pd.Timestamp.max

    def __init__(self, *args, **kwargs):
        pass

    def __contains__(self, other):
        """Whether a given point of time is in
        the TimePeriod"""
        interval = self.rollforward(other)
        return other in interval

    def __and__(self, other):
        # self & other
        # bitwise and
        # using & operator

        return All(self, other)

    def __or__(self, other):
        # self | other
        # bitwise or

        return Any(self, other)

    def rollforward(self, dt):
        "Get previous time interval of the period."
        raise NotImplementedError

    def rollback(self, dt):
        "Get previous time interval of the period."
        raise NotImplementedError

    def next(self, dt):
        "Get next interval (excluding currently ongoing if any)."
        interv = self.rollforward(dt)
        if dt in interv:
            # Offsetting the end point with minimum amount to get new full interval
            interv = self.rollforward(dt.right + self.resolution)
        return interv

    def prev(self, dt):
        "Get previous interval (excluding currently ongoing if any)."
        interv = self.rollback(dt)
        if dt in interv:
            # Offsetting the end point with minimum amount to get new full interval
            interv = self.rollback(dt.left - self.resolution)
        return interv


class TimeInterval(TimePeriod):
    """Base for all time intervals

    Time interval is a period between two fixed but repeating 
    times. Fixed repeated times are defined as time elements
    that repeats constantly but are fixed in a sense that
    if the datetime of an event is known, the question
    whether the event belongs to the period can be answered
    unambigiously.

    Answers to "between 11:00 and 12:00" and "from monday to tuesday"
    """
    _type_name = "interval"
    @abstractmethod
    def __contains__(self, dt):
        "Check whether the datetime is on the period"
        raise NotImplementedError("Contains not implemented.")

    @abstractmethod
    def rollstart(self, dt):
        "Roll forward to next point in time that on the period"
        raise NotImplementedError("Contains not implemented.")

    @abstractmethod
    def rollend(self, dt):
        "Roll back to previous point in time that is on the period"
        raise NotImplementedError("Contains not implemented.")

    @abstractmethod
    def next_start(self, dt):
        "Get next start point of the period"
        raise NotImplementedError("Contains not implemented.")

    @abstractmethod
    def next_end(self, dt):
        "Get next end point of the period"
        raise NotImplementedError("Contains not implemented.")

    @abstractmethod
    def prev_start(self, dt):
        "Get previous start point of the period"
        raise NotImplementedError("Contains not implemented.")

    @abstractmethod
    def prev_end(self, dt):
        "Get pervious end point of the period"
        raise NotImplementedError("Contains not implemented.")

    @abstractmethod
    def from_between(start, end) -> pd.Interval:
        raise NotImplementedError("__between__ not implemented.")

    def rollforward(self, dt):
        "Get next time interval of the period"

        start = self.rollstart(dt)
        end = self.next_end(dt)

        start = pd.Timestamp(start)
        end = pd.Timestamp(end)
        
        return pd.Interval(start, end, closed="both")
    
    def rollback(self, dt) -> pd.Interval:
        "Get previous time interval of the period"

        end = self.rollend(dt)
        start = self.prev_start(dt)

        start = pd.Timestamp(start)
        end = pd.Timestamp(end)
        
        return pd.Interval(start, end, closed="both")

    def __eq__(self, other):
        "Test whether self and other are essentially the same periods"
        is_same_class = type(self) == type(other)
        if is_same_class:
            return (self._start == other._start) and (self._end == other._end)
        else:
            return False


class TimeDelta(TimePeriod):
    """Base for all time deltas

    Time delta is a period of time from a reference
    point. It is floating in nature as it could
    contain arbitrary datetimes depending on where
    the reference point is set. This reference
    point is typically current datetime.
    """
    _type_name = "delta"

    reference: datetime.datetime

    def __init__(self, past=None, future=None, kws_past=None, kws_future=None):

        past = 0 if past is None else past
        future = 0 if future is None else future

        kws_past = {} if kws_past is None else kws_past
        kws_future = {} if kws_future is None else kws_future
        
        self.past = abs(pd.Timedelta(past, **kws_past))
        self.future = abs(pd.Timedelta(future, **kws_future))
        if pd.isna(self.past):
            raise future("TimeDelta past duration cannot be 'not a time'")
        if pd.isna(self.past):
            raise ValueError("TimeDelta future duration cannot be 'not a time'")

    @abstractmethod
    def __contains__(self, dt):
        "Check whether the datetime is in "
        reference = getattr(self, "reference", datetime.datetime.fromtimestamp(time.time()))
        start = reference - abs(self.past)
        end = reference + abs(self.future)
        return start <= dt <= end

    def rollback(self, dt):
        "Get previous interval (including currently ongoing)"
        start = dt - abs(self.past)
        start = pd.Timestamp(start)
        end = pd.Timestamp(dt)
        return pd.Interval(start, end) 

    def rollforward(self, dt):
        "Get next interval (including currently ongoing)"
        end = dt + abs(self.future)
        start = pd.Timestamp(dt)
        end = pd.Timestamp(end)
        return pd.Interval(start, end)

    def __eq__(self, other):
        "Test whether self and other are essentially the same periods"
        is_same_class = type(self) == type(other)
        if is_same_class:
            return (self.past == other.past) and (self.future == other.future)
        else:
            return False

class TimeCycle(TimePeriod):
    """Base for all time cycles

    Time cycle is a period of time that is constantly
    repeating. It has start time but inherently all
    datetimes belong to the cycle. Useful tool to 
    check whether an event has already 

    Useful for checking times an event has happened
    during the cycle

    Examples:

    - hourly
    - daily
    - weekly
    - monthly
    """
    # TODO: Delete
    _type_name = "cycle"

    offset = None
    def __init__(self, *args, n=1, **kwargs):
        self.start = self.transform_start(*args, **kwargs)
        self.n = n

    def __mul__(self, value):
        return type(self)(self.start, n=value)

    def rollback(self, dt):
        dt_start = dt - (self.n - 1) * self.offset
        if self.get_time_element(dt_start) >= self.start:
            #       dt
            #  -->--------------------->-----------
            #  time   |              time     |    
            pass
        else:
            #               dt
            #  -->--------------------->-----------
            #  time   |              time     |    
            dt_start = dt_start - self.offset
        dt_start = self.replace(dt_start)

        start = pd.Timestamp(dt_start)
        end = pd.Timestamp(dt)

        return pd.Interval(start, end)

    def rollforward(self, dt):
        dt_end = dt + (self.n - 1) * self.offset
        if self.get_time_element(dt_end) >= self.start:
            #       dt           (dt_end)
            #  -->--------------------->-----------
            #  time   |              time     |    
            dt_end = dt_end + self.offset
        else:
            #               dt
            #  -->--------------------->-----------
            #  time   |              time     |    
            pass
        dt_end = self.replace(dt_end)

        start = pd.Timestamp(dt)
        end = pd.Timestamp(dt_end) - self.resolution
        
        return pd.Interval(start, end)

    def rollend(self, dt):
        """All datetimes are in the cycle thus rolls
        returns the same datetime. This method is for
        convenience"""
        return dt

    def rollstart(self, dt):
        """All datetimes are in the cycle thus rolls
        returns the same datetime. This method is for
        convenience"""
        return dt

    @abstractmethod
    def transform_start(self, dt):
        pass

    @abstractmethod
    def get_time_element(self, dt):
        """Extract the time element from a
        datetime.
        Examples:
        ---------
            week cycle: day of week
            day cycle: time of day
            month cycle: day of month"""

    @abstractmethod
    def replace(self, dt):
        """Replace the datetime in a way that it is
        on current cycle's start day. This is to make
        the implementation of cycles less tiresome"""
        #              dt---------->
        #  -->--------------------->-----------
        #  time      |           time     |    
        # OR
        #    <----dt  
        #  -->--------------------->-----------
        #  time      |           time     |    


def all_overlap(times:List[pd.Interval]):
    return all(a.overlaps(b) for a, b in itertools.combinations(times, 2))

def get_overlapping(times):
    # Example:
    # A:    <-------------->
    # B:     <------>
    # C:         <------>
    # Out:       <-->
    starts = [interval.left for interval in times]
    ends = [interval.right for interval in times]

    start = max(starts)
    end = min(ends)
    return pd.Interval(start, end)

class All(TimePeriod):

    def __init__(self, *args):
        if any(not isinstance(arg, TimePeriod) for arg in args):
            raise TypeError("All is only supported with TimePeriods")
        self.periods = args

    def rollback(self, dt):
        intervals = [
            period.rollback(dt)
            for period in self.periods
        ]

        if all_overlap(intervals):
            # Example:
            # A:    <-------------->
            # B:     <------>
            # C:         <------>
            # Out:       <-->
            return get_overlapping(intervals)
        else:
            # A:         <---------------->
            # B:            <--->     <--->
            # C:         <------->
            # Try from:             <-|

            starts = [interval.left for interval in intervals]
            return self.rollback(max(starts) - datetime.datetime.resolution)

    def rollforward(self, dt):
        intervals = [
            period.rollforward(dt)
            for period in self.periods
        ]
        if all_overlap(intervals):
            # Example:
            # A:    <-------------->
            # B:     <------>
            # C:         <------>
            # Out:       <-->
            return get_overlapping(intervals)
        else:
            # A:          <---------------->
            # B:            <--->     <--->
            # C:                  <------->
            # Try from:         |->
            ends = [interval.right for interval in intervals]
            return self.rollforward(min(ends) + datetime.datetime.resolution)


class Any(TimePeriod):

    def __init__(self, *args):
        if any(not isinstance(arg, TimePeriod) for arg in args):
            raise TypeError("Any is only supported with TimePeriods")
        self.periods = args

    def rollback(self, dt):
        intervals = [
            period.rollback(dt)
            for period in self.periods
        ]

        # Example:
        # A:    <-------------->
        # B:     <------>
        # C:         <------------->
        # Out:  <------------------>

        # Example:
        # A:    <-->   
        # B:     <--->     <--->
        # C:     <------>
        # Out:  <------->

        # Example:
        # A:    <-->   
        # B:    <--->     <--->
        # C:        <----->
        # Out:  <------------->
        starts = [interval.left for interval in intervals]
        ends = [interval.right for interval in intervals]

        start = min(starts)
        end = max(ends)

        next_intervals = [
            period.rollback(start - datetime.datetime.resolution)
            for period in self.periods
        ]
        if any(pd.Interval(start, end).overlaps(interval) for interval in next_intervals):
            # Example:
            # A:    <-->   
            # B:    <--->     <--->
            # C:        <----->
            # Out:  <---------|--->
            extended = self.rollback(start - datetime.datetime.resolution)
            start = extended.left

        return pd.Interval(start, end)

    def rollforward(self, dt):
        intervals = [
            period.rollforward(dt)
            for period in self.periods
        ]

        starts = [interval.left for interval in intervals]
        ends = [interval.right for interval in intervals]

        start = min(starts)
        end = max(ends)

        next_intervals = [
            period.rollforward(end + datetime.datetime.resolution)
            for period in self.periods
        ]

        if any(pd.Interval(start, end).overlaps(interval) for interval in next_intervals):
            # Example:
            # A:    <-->   
            # B:    <--->     <--->
            # C:        <----->
            # Out:  <---------|--->
            extended = self.rollforward(end + datetime.datetime.resolution)
            end = extended.right

        return pd.Interval(start, end)

class Offsetted(TimePeriod):
    # TODO: This is not used. Delete?
    def __init__(self, period, n):
        if isinstance(period, TimeCycle):
            # adjust prev & next
            raise NotImplementedError
        self.period = period
        self.n = n

    def rollback(self, dt):
        interval = self.period.rollback(dt)
        new_dt = interval.left - pd.Timestamp.resolution
        interval = self.period.rollback(new_dt)
        return interval

    def rollforward(self, dt):
        interval = self.period.rollforward(dt)
        new_dt = interval.right + pd.Timestamp.resolution
        interval = self.period.rollforward(new_dt)
        return interval

class StaticInterval(TimePeriod):
    """Inverval that is fixed in specific datetimes."""

    def __init__(self, start=None, end=None):
        self.start = start if start is not None else self.min
        self.end = end if end is not None else self.max

    def rollback(self, dt):
        dt = pd.Timestamp(dt)
        start = pd.Timestamp(self.start)
        if start > dt:
            # The actual interval is in the future
            return pd.Interval(self.min, self.min)
        return pd.Interval(start, dt)

    def rollforward(self, dt):
        dt = pd.Timestamp(dt)
        end = pd.Timestamp(self.end)
        if end < dt:
            # The actual interval is already gone
            return pd.Interval(self.max, self.max, closed="both")
        return pd.Interval(dt, end, closed="both")

    @property
    def is_max_interval(self):
        return (self.start == self.min) and (self.end == self.max)
