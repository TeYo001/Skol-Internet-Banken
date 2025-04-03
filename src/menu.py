### THIS IS WHERE THE USER END INTERACTION STUFF WILL BE ###
# Note(TeYo) I'm thinking we implement a basic version of this before we get the more complex rendering in place, for testing of the backend and stuff

from src.external_imports import *
from src.backend import *

class MenuStateType(Enum):
    START = 0
    LOGIN = 1
    LOGOUT = 2
    ACCOUNT_VIEW = 3
    INPUT_MONEY = 4
    WITHDRAW_MONEY = 5
    TRANSFER_MONEY = 6

class MenuError(Enum):
    EXIT = 0

@dataclass
class MenuState:
    ...
@dataclass
class MenuStateMachine:
    ...

@dataclass
class MenuState:
    menu_function: Callable[[MenuStateMachine], MenuStateType | MenuError]
    state_type: MenuStateType

# state machine
@dataclass
class MenuStateMachine:
    all_states: Dict[MenuStateType, MenuState]
    current_state: MenuState
        
def menu_run(menu: MenuStateMachine):
    while True:
        next = menu.current_state.menu_function(menu)
        # TODO(TeYo): Handle the error
        if type(next) is MenuError:
            return
        menu.current_state = menu.all_states[next]

def menu_start(menu: MenuStateMachine) -> MenuStateType | MenuError:
    print("This is the bank start menu")
    print("1: login")
    print("2: exit")
    option = int(input("select: "))
    match option:
        case 1: return MenuStateType.LOGIN
        case 2: return MenuError.EXIT

def menu_input_money(menu: MenuStateMachine) -> MenuStateType | MenuError:
    amount = int(input("enter input amount (kr): "))
    print(f"{amount}kr deposited into account")
    time.sleep(1.5)
    return MenuStateType.ACCOUNT_VIEW

def menu_withdraw_money(menu: MenuStateMachine) -> MenuStateType | MenuError:
    amount = int(input("enter withdraw amount (kr): "))
    print(f"{amount}kr withdrawn from account")
    time.sleep(1.5)
    return MenuStateType.ACCOUNT_VIEW

def menu_transfer_money(menu: MenuStateMachine) -> MenuStateType | MenuError:
    dest_account_name = input("enter destination account name: ")
    amount = int(input("enter transfer amount (kr): "))
    print(f"{amount}kr transfered to {dest_account_name}")
    time.sleep(1.5)
    return MenuStateType.ACCOUNT_VIEW

def menu_login(menu: MenuStateMachine) -> MenuStateType | MenuError:
    account_name = input("enter account name: ")
    account_password = input("enter account password: ")
    # TODO(TeYo): actually interact with the backend
    return MenuStateType.ACCOUNT_VIEW

def menu_logout():
    ...

def menu_create_account():
    ...

# where the account is visualized and where you can choose what to do once logged in
def menu_view_account(menu: MenuStateMachine) -> MenuStateType | MenuError:
    print("Your account balance: you're broke")
    print("1: input money")
    print("2: withdraw money")
    print("3: tranfer money")
    print("4: exit")
    option = int(input("select: "))
    match option:
        case 1: return MenuStateType.INPUT_MONEY
        case 2: return MenuStateType.WITHDRAW_MONEY
        case 3: return MenuStateType.TRANSFER_MONEY
        case 4: return MenuError.EXIT

# initializes the menu state machine
def menu_init() -> MenuStateMachine:
    all_states = {
        MenuStateType.START : MenuState(menu_start, MenuStateType.START),
        MenuStateType.LOGIN : MenuState(menu_login, MenuStateType.LOGIN),
        MenuStateType.LOGOUT : MenuState(menu_logout, MenuStateType.LOGOUT),
        MenuStateType.ACCOUNT_VIEW : MenuState(menu_view_account, MenuStateType.ACCOUNT_VIEW),
        MenuStateType.INPUT_MONEY : MenuState(menu_input_money, MenuStateType.INPUT_MONEY),
        MenuStateType.WITHDRAW_MONEY : MenuState(menu_withdraw_money, MenuStateType.WITHDRAW_MONEY),
        MenuStateType.TRANSFER_MONEY : MenuState(menu_transfer_money, MenuStateType.TRANSFER_MONEY),
    }
    return MenuStateMachine(all_states, all_states[MenuStateType.START])


