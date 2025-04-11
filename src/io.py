from src.external_imports import *

class InputType(Enum):
    MOVE_UP = 0
    MOVE_DOWN = 1
    PRESS = 2
    ESCAPE = 3

@dataclass
class IOState:
    input_type: InputType
    update_on_type: Callable[[], None]

def on_press(io: IOState, key):
    match key:
        case keyboard.Key.up: 
            io.input_type = InputType.MOVE_UP
            return False
        case keyboard.Key.down:
            io.input_type = InputType.MOVE_DOWN
            return False
        case keyboard.Key.enter:
            io.input_type = InputType.PRESS
            return False
        case keyboard.Key.esc:
            io.input_type = InputType.ESCAPE
            return False
        case keyboard.Key.backspace:
            io.update_on_type("backspace")
            return None
    try:
        io.update_on_type(key.char)
    except AttributeError:
        return

def await_input(update_on_type: Callable[[str], None]) -> IOState:
    io = IOState(InputType.ESCAPE, update_on_type)
    with keyboard.Listener(on_press=lambda key: on_press(io, key)) as listener:
        listener.join()
    return io
