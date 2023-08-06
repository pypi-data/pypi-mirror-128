
from typing import Tuple, Dict
import inspect

# Copied from redengine.pybox\meta\func\func.py

def filter_keyword_args(_func, _params:dict=None, **kwargs):
    """Filter only keyword arguments that the 
    function requires."""
    if _params:
        kwargs.update(_params)
    sig = inspect.signature(_func)

    kw_args = [
        val.name
        for name, val in sig.parameters.items()
        if val.kind in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD, # Normal argument
            inspect.Parameter.KEYWORD_ONLY # Keyword argument
        )
    ]
    return {
        key: val for key, val in kwargs.items()
        if key in kw_args
    }

def parse_return(obj, args:Tuple=None, kwargs:Dict=None) -> Tuple[Tuple, Dict]:
    """Turn a function return to Pythonic args and kwargs of a function
    
    Examples:
    ---------
        def myfunc():
            ....
            return (1,2,3)

        return_value_to_args_kwargs(myfunc())
        >>> (1,2,3), {}

        def myfunc():
            ....
            return {"x": 1, "y": 5}

        return_value_to_args_kwargs(myfunc())
        >>> (), {"x": 1, "y": 5}

        def myfunc():
            ....
            return (1,2,3), {"x": 1, "y": 5}

        return_value_to_args_kwargs(myfunc())
        >>> (1,2,3), {"x": 1, "y": 5}

        def myfunc():
            ....
            return [1,2,3]

        return_value_to_args_kwargs(myfunc())
        >>> ([1,2,3],), {}
    """
    args = () if args is None else args
    kwargs = {} if kwargs is None else kwargs

    is_kwargs = isinstance(obj, dict)
    is_args = isinstance(obj, tuple)
    is_args_and_kwargs = (
        isinstance(obj, tuple) 
        and len(obj) == 2 
        and isinstance(obj[0], tuple) and isinstance(obj[1], dict)
    )
    
    if obj is None:
        # return
        pass
    elif is_args_and_kwargs:
        # return (1,2,3), {"x": 5, "y": 10}
        args = args + obj[0]
        kwargs.update(obj[1])
    elif is_kwargs:
        # return {"x": 5, "y": 10}
        kwargs.update(obj)
    elif is_args:
        # return 1, 2, 3
        args = args + obj
    else:
        # return not_a_tuple_or_dict
        args = args + (obj,)
    return args, kwargs