### THIS IS WHERE THE USER END INTERACTION STUFF WILL BE ###
# Note(TeYo) I'm thinking we implement a basic version of this before we get the more complex rendering in place, for testing of the backend and stuff

from src.external_imports import *
from src.backend import *
from src.render import *
from src.io import *

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
    window: cs.window = None

def menu_wrapped_run(menu: MenuStateMachine, window: cs.window):
    menu.window = window
    init_window_settings()   
    while True:
        next = menu.current_state.menu_function(menu)
        # TODO(TeYo): Handle the error
        if type(next) is MenuError:
            save_bank()
            return
        menu.current_state = menu.all_states[next]   

def menu_run(menu: MenuStateMachine):
    load_bank()
    cs.wrapper(lambda window: menu_wrapped_run(menu, window))

# TODO(TeYo): add error handling
def menu_update_on_type(menu: MenuStateMachine, select_frame: SelectFrame, char: str):
    current_option = None
    for option in select_frame.options:
        if option.select == SelectState.HOVER and type(option) == SelectField:
            current_option = option
    if current_option is None:
        return
    if char == "backspace":
        if len(current_option.field) == 0:
            return
        current_option.field = current_option.field[:-1]
    else:
        current_option.field += char
    draw_select_frame(menu.window, select_frame)
    menu.window.refresh()

# TODO(TeYo): add error handling
def menu_handle_inputs(menu: MenuStateMachine,
                       select_frame: SelectFrame, 
                       on_press_state_list: list[MenuState | MenuError | None], # None if pressing that button should be ignored
                       on_press_func_list: list[Callable[[], MenuError | None] | None],
                       on_escape_state: MenuState | MenuError) -> MenuState | MenuError:
    current_option_idx = None
    current_option = None
    for idx, option in enumerate(select_frame.options):
        if option.select != SelectState.HOVER:
            continue
        current_option_idx = idx
        current_option = option
    while True:
        io = await_input(lambda char: menu_update_on_type(menu, select_frame, char))
        match io.input_type:
            case InputType.MOVE_UP:
                current_option.select = SelectState.NONE
                current_option_idx -= 1
                if current_option_idx < 0:
                    current_option_idx = len(select_frame.options) - 1
                current_option = select_frame.options[current_option_idx]
                current_option.select = SelectState.HOVER
                draw_select_frame(menu.window, select_frame)
                menu.window.refresh()
            case InputType.MOVE_DOWN:
                current_option.select = SelectState.NONE
                current_option_idx += 1
                if current_option_idx >= len(select_frame.options):
                    current_option_idx = 0
                current_option = select_frame.options[current_option_idx]
                current_option.select = SelectState.HOVER
                draw_select_frame(menu.window, select_frame)
                menu.window.refresh()
            case InputType.PRESS:
                if not on_press_state_list[current_option_idx] is None:
                    current_option.select = SelectState.SELECT
                    current_option.color = Color.GREEN
                    draw_select_frame(menu.window, select_frame)
                    menu.window.refresh()
                    time.sleep(0.5)
                if type(current_option) is SelectToggle:
                    current_option.toggle = not current_option.toggle
                func = on_press_func_list[current_option_idx]
                if not func is None:
                    error = func()
                    if not error is None:
                        return error
                if not on_press_state_list[current_option_idx] is None:
                    return on_press_state_list[current_option_idx]
            case InputType.ESCAPE:
                return on_escape_state

def menu_render_default_frame(menu: MenuStateMachine, option_count: int):
    rows, cols = menu.window.getmaxyx()
    frame = Frame(cols-1,rows-option_count-1)
    draw_bank_logo(frame)
    draw_frame(menu.window, frame)
    menu.window.refresh()

def menu_start(menu: MenuStateMachine) -> MenuStateType | MenuError:
    OPTION_COUNT = 4
    menu_render_default_frame(menu, OPTION_COUNT)
    select_frame = build_select_frame(menu.window, [
        SelectButton(name="Login", select=SelectState.HOVER),
        SelectButton(name="Create Account"),
        SelectField(name="Help", field=""),
        SelectButton(name="Exit"),
    ])
    draw_select_frame(menu.window, select_frame)
    menu.window.refresh()
    return menu_handle_inputs(menu, select_frame, 
                              [MenuStateType.LOGIN, MenuStateType.CREATE_ACCOUNT, None, MenuError.EXIT],
                              [None, None, None, None],
                              MenuError.EXIT)

def menu_input_confirm(menu: MenuStateMachine, select_frame: SelectFrame) -> MenuError | None:
    # TODO(TeYo): error handling
    account = get_current_account()
    if type(account) is AccountError:
        return MenuError.PANIC
    amount = int(select_frame.options[0].field)
    error = input_money(account, Money(amount))
    if not error is None:
        return MenuError.PANIC

def menu_input_money(menu: MenuStateMachine) -> MenuStateType | MenuError:
    OPTION_COUNT = 2
    menu_render_default_frame(menu, OPTION_COUNT)
    select_frame = build_select_frame(menu.window, [
        SelectField(name="Input Amount (kr)", field="", select=SelectState.HOVER),
        SelectButton(name="Confirm")
    ])
    draw_select_frame(menu.window, select_frame)
    menu.window.refresh()
    return menu_handle_inputs(menu, select_frame, 
                              [None, MenuStateType.ACCOUNT_VIEW],
                              [None, lambda: menu_input_confirm(menu, select_frame)],
                              MenuError.EXIT)

def menu_withdraw_confirm(menu: MenuStateMachine, select_frame: SelectFrame) -> MenuError | None:
    # TODO(TeYo): error handling
    account = get_current_account()
    if type(account) is AccountError:
        return MenuError.PANIC
    amount = int(select_frame.options[0].field)
    error = withdraw_money(account, Money(amount))
    if not error is None:
        return MenuError.PANIC

def menu_withdraw_money(menu: MenuStateMachine) -> MenuStateType | MenuError:
    OPTION_COUNT = 2
    menu_render_default_frame(menu, OPTION_COUNT)
    select_frame = build_select_frame(menu.window, [
        SelectField(name="Withdraw Amount (kr)", field="", select=SelectState.HOVER),
        SelectButton(name="Confirm")
    ])
    draw_select_frame(menu.window, select_frame)
    menu.window.refresh()
    return menu_handle_inputs(menu, select_frame, 
                              [None, MenuStateType.ACCOUNT_VIEW],
                              [None, lambda: menu_withdraw_confirm(menu, select_frame)],
                              MenuError.EXIT)

def menu_transfer_confirm(menu: MenuStateMachine, select_frame: SelectFrame) -> MenuError | None:
    # TODO(TeYo): error handling
    account = get_current_account()
    if type(account) is AccountError:
        return MenuError.PANIC
    amount = int(select_frame.options[1].field)
    dest_account = get_account_from_name(select_frame.options[0].field)
    if type(dest_account) is AccountError:
        return MenuError.PANIC
    error = transfer_money(account, dest_amount, Money(amount))
    if not error is None:
        return MenuError.PANIC

def menu_transfer_money(menu: MenuStateMachine) -> MenuStateType | MenuError:
    OPTION_COUNT = 3
    menu_render_default_frame(menu, OPTION_COUNT)
    select_frame = build_select_frame(menu.window, [
        SelectField(name="Destination Account Name", field="", select=SelectState.HOVER),
        SelectField(name="Transfer Amount (kr)", field=""),
        SelectButton(name="Confirm")
    ])
    draw_select_frame(menu.window, select_frame)
    menu.window.refresh()
    return menu_handle_inputs(menu, select_frame, 
                              [None, None, MenuStateType.ACCOUNT_VIEW],
                              [None, None, lambda: menu_transfer_confirm(menu, select_frame)],
                              MenuError.EXIT)

def menu_login_confirm(menu: MenuStateMachine, select_frame: SelectFrame) -> MenuError | None:
    account_name = select_frame.options[0].field
    account_password = select_frame.options[1].field
    account = login(account_name, account_password)
    if type(account) is AccountError:
        # TODO(TeYo): handle the errors (can't use print with the new rendering system)
        return MenuError.PANIC

def menu_login(menu: MenuStateMachine) -> MenuStateType | MenuError:
    OPTION_COUNT = 3
    menu_render_default_frame(menu, OPTION_COUNT)
    select_frame = build_select_frame(menu.window, [
        SelectField(name="Name", field="", select=SelectState.HOVER),
        SelectField(name="Password", field=""),
        SelectButton(name="Confirm")
    ])
    draw_select_frame(menu.window, select_frame)
    menu.window.refresh()
    return menu_handle_inputs(menu, select_frame, 
                              [None, None, MenuStateType.ACCOUNT_VIEW],
                              [None, None, lambda: menu_login_confirm(menu, select_frame)],
                              MenuError.EXIT)

def menu_logout(menu: MenuStateMachine) -> MenuStateType | MenuError:
    logout()
    return MenuStateType.START

def menu_choose_account_type(menu: MenuStateMachine, previous_toggle_idx: list[int], select_frame: SelectFrame) -> MenuError | None:
    if previous_toggle_idx[0] != -1:
        select_frame.options[previous_toggle_idx[0]].toggle = False
    for i in range(3, 6): # NOTE(TeYo): not great to have magic numbers like this, but I'm tired
        if select_frame.options[i].toggle:
            previous_toggle_idx[0] = i
            break
    draw_select_frame(menu.window, select_frame)
    menu.window.refresh()

def menu_create_account_confirm(menu: MenuStateMachine, select_frame: SelectFrame) -> MenuError | None:
    account_name = select_frame.options[0].field
    account_password = select_frame.options[1].field
    account_type = None
    account_type_idx = -1
    for i in range(3, 6):
        if not select_frame.options[i].toggle:
            continue
        account_type_idx = i
        break
    match account_type_idx:
        case 3: account_type = AccountType.DEBIT
        case 4: account_type = AccountType.SAVINGS
        case 5: account_type = AccountType.STOCK_FOND
        case _:
            # TODO(TeYo): handle error
            return MenuError.PANIC
    account = create_account(account_name, account_password, account_type)
    if type(account) is AccountError:
        # TODO(TeYo): handle error
        return MenuError.PANIC

def menu_create_account(menu: MenuStateMachine) -> MenuStateType | MenuError:
    OPTION_COUNT = 8
    previous_toggle_idx = [-1] 
    menu_render_default_frame(menu, OPTION_COUNT)
    select_frame = build_select_frame(menu.window, [
        SelectField(name="Account Name", field="", select=SelectState.HOVER),
        SelectField(name="Account Password", field=""),
        SelectTitle(name="Choose Account Type:"),
        SelectToggle(name="Debit", toggle=False),
        SelectToggle(name="Savings", toggle=False),
        SelectToggle(name="Stock Fond", toggle=False),
        SelectButton(name="Confirm"),
        SelectButton(name="Exit")
    ])
    draw_select_frame(menu.window, select_frame)
    menu.window.refresh()
    acc_switch_func = lambda: menu_choose_account_type(menu, previous_toggle_idx, select_frame)
    confirm_func = lambda: menu_create_account_confirm(menu, select_frame)
    return menu_handle_inputs(menu, select_frame, 
                              [None, None, None, None, None, None, MenuStateType.ACCOUNT_VIEW, MenuError.EXIT],
                              [None, None, None, acc_switch_func, acc_switch_func, acc_switch_func, confirm_func, None],
                              MenuError.EXIT)

# where the account is visualized and where you can choose what to do once logged in
def menu_view_account(menu: MenuStateMachine) -> MenuStateType | MenuError:
    # TODO(TeYo): Add the actual account visualization
    OPTION_COUNT = 5
    menu_render_default_frame(menu, OPTION_COUNT)
    select_frame = build_select_frame(menu.window, [
        SelectButton(name="Input Money", select=SelectState.HOVER),
        SelectButton(name="Withdraw Money"),
        SelectButton(name="Transfer Money"),
        SelectButton(name="Logout"),
        SelectButton(name="Exit")
    ])
    draw_select_frame(menu.window, select_frame)
    menu.window.refresh()
    return menu_handle_inputs(menu, select_frame, 
                              [MenuStateType.INPUT_MONEY, MenuStateType.WITHDRAW_MONEY, MenuStateType.TRANSFER_MONEY, MenuStateType.LOGOUT, MenuError.EXIT],
                              [None, None, None, None, None],
                              MenuError.EXIT)

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


