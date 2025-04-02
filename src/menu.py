### THIS IS WHERE THE USER END INTERACTION STUFF WILL BE ###
# Note(TeYo) I'm thinking we implement a basic version of this before we get the more complex rendering in place, for testing of the backend and stuff

from src.external_imports import *

class MenuStateType(Enum):
    IDLE = 0

@dataclass
class MenuState:
    ...

@dataclass
class MenuState:
    state_type: MenuStateType
    valid_state_transitions: list[MenuStateType]
    state_transition_array: list[Callable[[MenuState], bool]]
    

# state machine
class MenuStateMachine:
    def __init__(self):
        self.all_states = []
        self.current_state_type = MenuStateType.IDLE
        self.current_state_info = MenuState
        self.valid_state_change_array = []

    def add_state(self, state: MenuState) -> bool:
        ...

    def change_state(self, state: MenuStateType) -> bool:
        ...

# initializes the menu state machine
def menu_init() -> MenuStateMachine:
    ...

def menu_start():
    ...

def menu_input_money():
    ...

def menu_withdraw_money():
    ...

def menu_transfer_money():
    ...

def menu_login():
    ...

def menu_logout():
    ...

def menu_create_account():
    ...

# where the account is visualized and where you can choose what to do once logged in
def menu_view_account():
    ...
