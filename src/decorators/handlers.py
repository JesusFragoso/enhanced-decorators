from functools import reduce
from random import randint 
from typing import Callable
from typing import Union
from typing import Tuple
from utils import Ranges
from copy import copy
from pydantic import BaseModel
from typing import Type
from typing import TypeVar
from pydantic import ValidationError

T = TypeVar('T')


class DataHandler:
    """
    Class that uses a normal method inside a class and uses it as a decorator
    for a class that creates an user.

    It can also be decorated with the `staticmethod` decorator.
    """
    
    # @staticmethod -> This statement can be used wihout any other modification.
    def generate_random_age(main_function: Callable) -> Callable:
        def wrapper(*args: Tuple, **kwargs: dict):
            kwargs.update(age=randint(*Ranges.RANDOM_NUMBERS_RANGE.value))
            return main_function(*args, **kwargs)
        return wrapper


def generate_additional_number(main_function: Callable) -> Callable:
    def operation_selector(function_name: str) -> Callable:
        """
        Function to select the operation to be performed,
        based in the name of the decorated function.

        Parameters
        ----------
        `function_name` : `str`
            Function that will perform some operation
            based in addition, substraction or multiplication.

        Returns
        -------
        `Callable`
            A callable object in this case, a lambda function
            previously mapped to the specific name of the function
            to be executed.
        """
        operations: dict = {
            "add_numbers": lambda x, y: x + y,
            "substract_numbers": lambda x, y: x - y,
            "multiply_numbers": lambda x, y: x * y
        }

        return operations.get(function_name)

    def inner_function(*args: Tuple, **kwargs: dict) -> Tuple[int, Union[int, float]]:
        print("Generating a random number between 1 and 10 ... ")
        
        random_number = randint(*Ranges.RANDOM_NUMBERS_RANGE.value)
        print(f"The random number generated is: {random_number}")

        result = main_function(*args,**kwargs)
        return random_number, operation_selector(main_function.__name__)(result, random_number)
    
    return inner_function


class OperationHandler:
    """
    This class defines three different methods, and each
    one of them is decorated with a method outside this class,
    that generates an additional number that is applied based on 
    the operation that is executed for each particular method.
    """

    @generate_additional_number
    def add_numbers(self, *numbers: Tuple) ->Union[int, float]:
        return reduce(lambda first_number, second_number: first_number + second_number, numbers)
    
    @staticmethod
    @generate_additional_number
    def multiply_numbers(*numbers: Tuple):
        return reduce(lambda first_number, second_number: first_number * second_number, numbers)

    @classmethod
    @generate_additional_number
    def substract_numbers(cls, *numbers: Tuple):
        return reduce(lambda first_number, second_number: first_number - second_number, numbers)


class CustomDict(dict):
    """
    Custom dictionary that inherits from the built-in `dict` class,
    and overwrites the dunder method `__add__`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def tag_dictionary(main_function: Callable) -> Callable:
        def wrapper(*args: Tuple, **kwargs: dict):
            if "tag" not in (*args[0].keys(), *args[1].keys()):
                return main_function(*args, tag="Custom Dictionary - 🏷️", **kwargs)

            first_dictionary: dict = copy(args[0])
            second_dictionary: dict = copy(args[1])

            if "tag" in first_dictionary.keys() and "tag" in second_dictionary.keys():
                first_dictionary.pop("tag")

            return main_function(first_dictionary, second_dictionary)
        return wrapper
    
    @tag_dictionary
    def __add__(self, dictionary: dict, tag=None) -> dict:
        if tag:
            return CustomDict(**self, tag=tag, **dictionary)
        return CustomDict(**self, **dictionary)

#* ---- Use a class as a decorator. ---= #

class DataValidator:
    """
    Class that is used as a decorator to validate
    data that is used to create a `pydantic` entity/model.
    """
    def __init__(self, function: Callable):
        self.function = function

    def __get__(self, instance: T, class_type: Type[T]) -> Callable:
        """
        This method returns a `lambda` function that takes the instance of the class
        that holds a `DataValidator` object as attribute, along with any other arguments
        that could be passed into the `__call__` dunder method. 

        Parameters
        ----------
        instance : `T`
            Instance of the class that calls this descriptor.
        class_type : `Type[T]`
            Type of the class that the `T` instance belongs to.

        Returns
        -------
        `Callable`
            A `lambda` function that will accept as argument the instance that holds
            this `DataValidator` class as an attribute/descriptor.
        """
        return lambda *args, **kwargs: self(instance, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        try:
            return self.function(*args, **kwargs)
        except ValidationError:
            return "There was an error validating the data"
 

class EntityHandler:

    @DataValidator
    def create_entity(self, model_class: BaseModel, **data: dict)-> BaseModel:
        return model_class(**data)
