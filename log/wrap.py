from typing import Callable

def wrap(func:Callable) -> Callable:
    """Copies a function's name, docstring, and annotations into the decorated function
        
    A quick rewrite of the functools.wraps() for the micropython system that does not have functools

    Makes debugging easier by keeping the function name instead of "wrapper"

    Parameters
    ----------
    func : `Callable`
        The function whose attributes are copied in

    Returns
    -------
    wrapper : `Callable`
    """

    def wrapper(dec: Callable) -> Callable:
        # copy attributes
        dec.__name__ = func.__name__
        dec.__qualname__ = func.__qualname__
        dec.__doc__ = func.__doc__
        dec.__annotations__ = func.__annotations__
        dec.__module__ = func.__module__
        dec.__wrapped__ = func
        return dec
    return wrapper