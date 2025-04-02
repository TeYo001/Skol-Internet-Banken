### NAMING CONVENTION ###

# for variables, functions and members:
# 1. use descriptive names
# 2. don't use short-form unless it is clear what it means
# ex: do change_directory_to_main(), not cdtm()

snake_case = 0

def snake_case_func():
    ...

@dataclass
class ThisIsAClass:
    member_one
    member_two

# for constants and enum elements:

THIS_IS_A_CONSTANT = 0

class EnumType(Enum):
    ONE = 0
    TWO = 1
    THREE = 2

# for class / type names:

class TypeOne:
    ...


### GOOD PRACTICE ###

# 1. always use typehints
# 2. don't write comments that describe what some piece of code is doing unless REALLY necessary. The code should describe itself
# 3. don't use globabl variables unless it is really needed
# 4. generally try to keep related code in their own files or sections.
# 5. you don't have to give a shit about performance, we are coding in python here [:
# 6. OOP and DRY is the devil, try to avoid it
