### THIS IS WHERE THE USER END INTERACTION STUFF WILL BE ###
# Note(TeYo) I'm thinking we implement a basic version of this before we get the more complex rendering in place, for testing of the backend and stuff

from src.external_imports import *
from src.backend import *

class MenuStateType(Enum):
    START = 0
    LOGIN = 1
    LOGOUT = 2
    CREATE_ACCOUNT = 3
    ACCOUNT_VIEW = 4
    INPUT_MONEY = 5
    WITHDRAW_MONEY = 6
    TRANSFER_MONEY = 7

class MenuError(Enum):
    EXIT = 0
    PANIC = 1

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
    load_bank()
    while True:
        next = menu.current_state.menu_function(menu)
        # TODO(TeYo): Handle the error
        if type(next) is MenuError:
            save_bank()
            return
        menu.current_state = menu.all_states[next]

def menu_start(menu: MenuStateMachine) -> MenuStateType | MenuError:
    print("This is the bank start menu")
    print("1: login")
    print("2: create account")
    print("3: exit")
    option = int(input("select: "))
    match option:
        case 1: return MenuStateType.LOGIN
        case 2: return MenuStateType.CREATE_ACCOUNT
        case 3: return MenuError.EXIT

def menu_input_money(menu: MenuStateMachine) -> MenuStateType | MenuError:
    amount = int(input("enter input amount (kr): "))
    account = get_current_account()
    if type(account) is AccountError:
        return MenuError.PANIC
    error = input_money(account, Money(amount))
    if not error is None:
        return MenuError.PANIC
    print(f"{amount}kr deposited into account")
    time.sleep(1.5)
    return MenuStateType.ACCOUNT_VIEW

def menu_withdraw_money(menu: MenuStateMachine) -> MenuStateType | MenuError:
    amount = int(input("enter withdraw amount (kr): "))
    account = get_current_account()
    if type(account) is AccountError:
        return MenuError.PANIC
    error = withdraw_money(account, Money(amount))
    if not error is None:
        return MenuError.PANIC
    print(f"{amount}kr withdrawn from account")
    time.sleep(1.5)
    return MenuStateType.ACCOUNT_VIEW

def menu_transfer_money(menu: MenuStateMachine) -> MenuStateType | MenuError:
    dest_account_name = input("enter destination account name: ")
    dest_account = get_account_from_name(dest_account_name)
    if type(dest_account) is AccountError:
        return MenuError.PANIC # TODO(TeYo): actually handle this error properly
    amount = int(input("enter transfer amount (kr): "))
    account = get_current_account()
    if type(account) is AccountError:
        return MenuError.PANIC
    error = transfer_money(account, dest_account, Money(amount))
    if not error is None:
        return MenuError.PANIC # TODO(TeYo): actually handle this error properly
    print(f"{amount}kr transfered to {dest_account_name}")
    time.sleep(1.5)
    return MenuStateType.ACCOUNT_VIEW

def menu_login(menu: MenuStateMachine) -> MenuStateType | MenuError:
    account_name = input("enter account name: ")
    account_password = input("enter account password: ")
    account = login(account_name, account_password)
    if type(account) is AccountError:
        match account:
            case AccountError.WRONG_NAME: 
                print("wrong name")
                return MenuStateType.LOGIN
            case AccountError.WRONG_PASSWORD:
                print("wrong password")
                return MenuStateType.LOGIN
            case _:
                print("panic")
                return MenuError.PANIC
    return MenuStateType.ACCOUNT_VIEW

def menu_logout(menu: MenuStateMachine) -> MenuStateType | MenuError:
    logout()
    return MenuStateType.START

def menu_create_account(menu: MenuStateMachine) -> MenuStateType | MenuError:
    account_name = input("enter account name: ")
    account_password = input("enter account password: ")
    print("Choose account type")
    print("1: debit")
    print("2: savings")
    print("3: stock fond")
    type_num = int(input("select: "))
    acc_type = None
    match type_num:
        case 1: acc_type = AccountType.DEBIT
        case 2: acc_type = AccountType.SAVINGS
        case 3: acc_type = AccountType.STOCK_FOND
    account = create_account(account_name, account_password, acc_type)
    if type(account) is AccountError:
        match account:
            case _: 
                return MenuError.PANIC
    return MenuStateType.START
    

# where the account is visualized and where you can choose what to do once logged in
def menu_view_account(menu: MenuStateMachine) -> MenuStateType | MenuError:
    account = get_current_account()
    if type(account) is AccountError:
        return MenuError.PANIC   

    print(f"Your account balance: {account.money.amount_kr}kr")
    print("1: input money")
    print("2: withdraw money")
    print("3: tranfer money")
    print("4: logout")
    print("5: exit")
    option = int(input("select: "))
    match option:
        case 1: return MenuStateType.INPUT_MONEY
        case 2: return MenuStateType.WITHDRAW_MONEY
        case 3: return MenuStateType.TRANSFER_MONEY
        case 4: return MenuStateType.LOGOUT
        case 5: return MenuError.EXIT

# initializes the menu state machine
def menu_init() -> MenuStateMachine:
    all_states = {
        MenuStateType.START : MenuState(menu_start, MenuStateType.START),
        MenuStateType.LOGIN : MenuState(menu_login, MenuStateType.LOGIN),
        MenuStateType.LOGOUT : MenuState(menu_logout, MenuStateType.LOGOUT),
        MenuStateType.CREATE_ACCOUNT : MenuState(menu_create_account, MenuStateType.CREATE_ACCOUNT),
        MenuStateType.ACCOUNT_VIEW : MenuState(menu_view_account, MenuStateType.ACCOUNT_VIEW),
        MenuStateType.INPUT_MONEY : MenuState(menu_input_money, MenuStateType.INPUT_MONEY),
        MenuStateType.WITHDRAW_MONEY : MenuState(menu_withdraw_money, MenuStateType.WITHDRAW_MONEY),
        MenuStateType.TRANSFER_MONEY : MenuState(menu_transfer_money, MenuStateType.TRANSFER_MONEY),
    }
    return MenuStateMachine(all_states, all_states[MenuStateType.START])


