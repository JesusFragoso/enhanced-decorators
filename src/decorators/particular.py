import inspect
from typing import Callable
from typing import Tuple
from typing import TypeVar
from typing import Type
from entities import User
from entities import AccountUser
from pydantic import BaseModel
from pydantic import ValidationError

T = TypeVar('T')

def validator(main_class: Type[T]) -> Callable:
    def method_decorator(main_function: Callable) -> Callable:
        def wrapper(*args: Tuple, **kwargs: dict):
            try:
                return main_function(*args, **kwargs)
            except ValidationError:
                return "There was an error with the data entered - 😞 ❌"
        return wrapper
    
    for attribute_name, attribute_value in main_class.__dict__.items():
        if attribute_name != "__init__" and inspect.isfunction(attribute_value):
            setattr(main_class, attribute_name, method_decorator(attribute_value))
    return main_class

@validator
class DataController:
    def create_entity(cls, entity: BaseModel, **data: dict) -> BaseModel:
        return entity(**data)