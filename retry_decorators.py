import random
import time
from functools import wraps

def retry(ExceptionToCheck, tries=3, delay=1, backoff=2):
    """Retry calling the decorated function using an exponential backoff."""

    def deco_retry(f):

        @wraps(f)
        def wrapped_func(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    print(f"{str(e)}, Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return wrapped_func

    return deco_retry

class retry:
    """
    Class Decorator that adds retry logic using an exponential backoff.
    """

    def __init__(self, ExceptionToCheck, tries=3, delay=1, backoff=2):
        self._ExceptionToCheck = ExceptionToCheck 
        self._max_tries = tries
        self._delay = delay
        self._backoff = backoff

    def __call__(self, f):

        @wraps(f)
        def wrapped_func(*args, **kwargs):
            mtries, mdelay = self._max_tries, self._delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except self._ExceptionToCheck as e:
                    logger.exception(f"{str(e)}, Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= self._backoff
            return f(*args, **kwargs)

        return wrapped_func


# Tests .....................
# Test1
@retry(Exception, tries=5)
def test_fail(text):
    raise Exception("Fail")

    
try:
    test_fail("It works!")
except:
    pass

# Test2
@retry(Exception, tries=5)
def test_success(text):
    print(f"Success: {text}")

try:
    test_success("it works!")
except:
    pass

# Test3
@retry(Exception, tries=4)
def test_random(text):
    x = random.random()
    if x < 0.5:
        raise Exception("Fail")
    else:
        print(f"Success: {text}")
try:
    test_random("it works!")
except:
    pass

# Test4
@retry((NameError, IOError), tries=20, delay=1, backoff=1)
def test_multiple_exceptions():
    x = random.random()
    if x < 0.40:
        raise NameError("NameError")
    elif x < 0.80:
        raise IOError("IOError")
    else:
        raise KeyError("KeyError")

try:
    test_multiple_exceptions()
except:
    pass
