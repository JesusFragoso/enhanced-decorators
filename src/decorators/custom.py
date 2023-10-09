from typing import Any
from typing import Callable
from typing import Tuple
from random import randint
from utils import Ranges

def normal_decorator(main_function: Callable) -> Callable:
    def wrapper(*args: Tuple, **kwargs: dict):
        print("Generating the random number ... 💭")
        
        random_number: int = randint(*Ranges.RANDOM_NUMBERS_RANGE.value)
        
        print(f"The number generated was: {random_number}")
        return main_function(*args, random_number=random_number, **kwargs)
    return wrapper

def decorator_with_arguments(first_argument: Any, second_argument: Any):
    def first_wrapper(main_function: Callable):
        def second_wrapper(*args: Tuple, **kwargs: dict):
            if first_argument >= second_argument:
                raise Exception("The first interval number must be minor than the second interval number")
            
            random_number: int = randint(first_argument, second_argument)
            return main_function(random_number, *args, **kwargs)
        return second_wrapper
    return first_wrapper

def exception_handler(main_function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return main_function(*args, **kwargs)
        except Exception as e:
            return e.args[0]
    return wrapper