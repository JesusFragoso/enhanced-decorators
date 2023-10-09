from typing import Tuple
from entities import User
from entities import AccountUser
from decorators import exception_handler
from decorators import decorator_with_arguments
from decorators import normal_decorator
from decimal import Decimal
from typing import Union
from decorators import DataHandler
from decorators import OperationHandler
from decorators import CustomDict
from uuid import uuid4
from decorators import EntityHandler


"""
TODO:

1. Make a decorator with arguments. ✅
2. Make a decorator using a class instead of a normal function. ✅
3. Make a decorator for a class, that applies the additional behaviour into
   each one of the methods of the decorated class.
"""

@normal_decorator
def numbers_division_mapping(*numbers: Tuple, **kwargs: Union[dict[str, int], None]):
    result =  dict(map(lambda number: (str(number), float(Decimal((number / (number + 1))).quantize(Decimal("1.00")))), numbers))
    result.update(kwargs)
    return result

@exception_handler
@decorator_with_arguments(10, 20)
def square_number_mapping(*numbers: Tuple) -> Tuple[int, int]:
    return list(map(lambda number: (number, number ** 2), numbers))

@DataHandler.generate_random_age
def create_user(**user_data: dict) -> User:
    user_instance = User(**user_data)
    return user_instance


if __name__ == "__main__":
    #* Using a normal decorator.
    print(numbers_division_mapping(1, 2, 3, 4, 5))

    #* Using two decorators.
    print(square_number_mapping(1, 2, 3))
    
    #* Using a decorator that is defined inside a class.
    user_created: User = create_user(name="Bucky")
    print(f"The user created is: {user_created.model_dump()}")

    #* Using a decorator defined outside a class, in the methods
    #* of another class.
    
    random_number, result = OperationHandler.multiply_numbers(1, 2, 3)
    assert result == (1 * 2 * 3) * random_number
    
    #* In this case, an instance of the `OperationHandler` class is needed
    #* in order to pass the `self` attribute to the `add_numbers` instance method.
    random_number, result = OperationHandler().add_numbers(1, 2, 3)
    assert result == (1 + 2 + 3) + random_number
    
    random_number, result = OperationHandler.substract_numbers(1, 2, 3)
    assert result == (1 - 2 - 3) - random_number

    #* Using a decorator defined inside a class.
    first_custom_dictionary = CustomDict(name="Bucky", age=24)
    second_custom_dictionary = CustomDict(country="Mexico", is_alive=True)

    #* All the different scenarios listed below are executed to verify if the tag for each
    #* `CustomDict` is created as expected inside the `tag_dictionary` decorator.
    new_custom_dictionary = first_custom_dictionary + second_custom_dictionary
    print(new_custom_dictionary)

    another_custom_dictionary = new_custom_dictionary + CustomDict(tag="New tag - 🏷️")
    print(another_custom_dictionary)
    
    user_with_extra_data = new_custom_dictionary + CustomDict(account_bank=uuid4())
    print(user_with_extra_data)

    #* Validating user data using a class as a decorator.
    
    #* Correct validation.
    user_data: dict = {'name': 'John','age': 23,'bank_account_mount': 23456.789,'is_alive': True}
    entity_or_error = EntityHandler().create_entity(AccountUser, **user_data)
    assert isinstance(entity_or_error, AccountUser) == True
    
    #* Wrong validation. 
    user_data: dict = {'name': 'John','age': 23,'bank_account_mount': 23456.789,'is_alive': 23.45}
    entity_or_error = EntityHandler().create_entity(AccountUser, **user_data)
    assert entity_or_error == 'There was an error validating the data'
     
    