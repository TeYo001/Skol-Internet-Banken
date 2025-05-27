### THIS IS WHERE WE CAN PUT SOME MORE COOL LOOKING GRAPHICS HANDLING ###
# Note(TeYo): This is basically what will set this project apart from the others and shit, I'm quite used to doing these kind of things so it should
# hopefully be kinda cool

from src.external_imports import *
from src.data import *
from src.art import *

class Color(IntEnum):
    BLACK = 0
    WHITE = 1
    GREEN = 2
    RED = 3
    YELLOW = 4

@dataclass
class Pixel:
    ch: str | int
    ch_color: Color = Color.WHITE

class Frame:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = [Pixel(' ')] * (width * height)

    def set_pixel(self, x: int, y: int, pixel: Pixel):
        self.pixels[y * self.width + x] = pixel

class SelectState(Enum):
    NONE = 0
    HOVER = 1
    SELECT = 2

@dataclass
class SelectButton:
    name: str
    select: SelectState = SelectState.NONE
    color: Color = Color.WHITE

@dataclass
class SelectTitle:
    name: str
    select: SelectState = SelectState.NONE
    color: Color = Color.WHITE

@dataclass
class SelectToggle:
    name: str
    toggle: bool
    select: SelectState = SelectState.NONE
    color: Color = Color.WHITE

@dataclass
class SelectField:
    name: str
    field: str
    select: SelectState = SelectState.NONE
    color: Color = Color.WHITE

@dataclass
class SelectFrame:
    width: int
    height: int
    start_row: int # at which row the select frame starts
    options: list[SelectButton | SelectField | SelectTitle | SelectToggle]

def build_select_frame(window: cs.window, options: list[SelectButton | SelectField | SelectTitle | SelectToggle]):
    rows, cols = window.getmaxyx()
    return SelectFrame(width=cols, 
                       height=len(options),
                       start_row=rows-len(options),
                       options=options)

def draw_frame(window: cs.window, frame: Frame):
    for y in range(frame.height):
        for x in range(frame.width):
            pixel = frame.pixels[x + y * frame.width]
            window.addch(frame.height - y, x, pixel.ch, cs.color_pair(int(pixel.ch_color)))

def draw_select_frame(window: cs.window, frame: SelectFrame):
    for idx, option in enumerate(frame.options):
        hover_str = "> " if (option.select == SelectState.HOVER or option.select == SelectState.SELECT) else ""
        select_str = "x" if option.select == SelectState.SELECT else ""
        button_str = None
        if type(option) is SelectButton: button_str = f"{hover_str}[{select_str}] {option.name}"
        elif type(option) is SelectField: button_str = f"{hover_str}[{select_str}] {option.name}: {option.field}"
        elif type(option) is SelectTitle: button_str = f"{hover_str}{option.name}"
        elif type(option) is SelectToggle:
            toggle_str = "x" if option.toggle else ""
            button_str = f"{hover_str}[{toggle_str}] {option.name}"
        else:
            print("ERROR")
            exit(1)
        window.move(frame.start_row+idx, 0)
        window.clrtoeol()
        window.addstr(frame.start_row+idx, 0, button_str, cs.color_pair(int(option.color)))

def draw_func(window: cs.window):
    func = lambda x: np.sqrt(x)
    for x in range(10):
        x = float(x)
        y = np.clip(0, 10, func(10-x))
        window.addch(int(y+10), int(x+10), cs.ACS_BLOCK, cs.color_pair(1))

def number_to_pretty_string(number: int | float) -> str:
    size_specifiers = ['', 'k', 'M', 'B', 'T']
    size_exponent = 0
    small_num = number
    while small_num > 10**3:
        small_num = small_num / 10**3
        size_exponent += 1
    if size_exponent >= len(size_specifiers):
        return '' # TODO(TeYo): perhaps do some type of error handling here (or just ensure it's nearly impossible)
    return f"{small_num:.2f}{size_specifiers[size_exponent]}"


def draw_y_axis_labels(frame: Frame, y_max: int, label_count=10, y_offset=0, color=Color.WHITE):
    for i in range(label_count):
        row_idx = np.clip(i * frame.height // label_count, 0, frame.height-1)
        number_str = number_to_pretty_string(y_max / label_count * i)
        for x, ch in enumerate(number_str):
            frame.set_pixel(x, row_idx+y_offset, Pixel(ch, color))

def draw_x_axis_labels(frame: Frame, base_x_offset: int, end_margin_size: int, step_size: int=4, label_count: int=5, color=Color.WHITE):
    adjusted_width = frame.width - base_x_offset - end_margin_size
    for i in range(label_count):
        year_str = f"{i*step_size}years"
        x_offset = np.clip(adjusted_width // (label_count-1) * i, 0, adjusted_width-1) + base_x_offset
        for x, ch in enumerate(year_str):
            frame.set_pixel(x_offset + x, 0, Pixel(ch, color))

def draw_graph(frame: Frame, graph: GraphData, min_delta_x=0.5, min_delta_y=0.5, x_size_modifier=1, y_size_modifier=1, x_offset=0, y_offset=0, color=Color.WHITE):
    adjusted_x_points = []
    adjusted_y_points = []
    if graph.x_max - graph.x_min <= min_delta_x:
        adjusted_x_points = copy(graph.x_points)
    else:
        x_adjust_factor = frame.width / graph.x_max
        for x in graph.x_points:
            adjusted_x_points.append(np.clip(int(x / graph.x_max * frame.width), 0, frame.width-1))
    if graph.y_max - graph.y_min >= min_delta_y:
        y_adjust_factor = frame.height / graph.y_max
        for y in graph.y_points:
            adjusted_y_points.append(np.clip(int(y / graph.y_max * frame.height), 0, frame.height-1))
    for i in range(len(adjusted_x_points)):
        frame.set_pixel(int(adjusted_x_points[i] * x_size_modifier + x_offset), 
                        int(adjusted_y_points[i] * y_size_modifier + y_offset), Pixel(cs.ACS_BLOCK, ch_color=color))

def calculate_interest(start_cash: float, interest: float, time_years: float) -> float:
    return start_cash * interest**time_years

def draw_cash_history_with_interest_projection(frame: Frame, cash_history: list[int], interest_rate: float=1.07, x_margin_size=10, bottom_margin_size=1):
    if len(cash_history) == 0:
        return
    if cash_history[-1] == 0:
        return
    projection_length_years=8
    width = frame.width - x_margin_size*2
    height = frame.height - bottom_margin_size
    cash_x_adjust_factor = width/2/len(cash_history)
    interest_x_adjust_factor = projection_length_years/(width/2)
    max_cash_after_interest = calculate_interest(cash_history[-1], interest_rate, projection_length_years)
    cash_y_adjust_factor = height/2/cash_history[-1]
    #interest_y_adjust_factor = frame.height/max_cash_after_interest
    last_y = 0
    
    # draws cash history
    for x in range(width//2):
        cash_idx = int(np.clip(x // len(cash_history), 0, len(cash_history)-1))
        cash = cash_history[cash_idx]
        y = int(np.clip(cash * cash_y_adjust_factor, 0, height/2))
        frame.set_pixel(x+x_margin_size, y+bottom_margin_size, Pixel(cs.ACS_BLOCK, Color.GREEN))
        if last_y != y:
            min_y = min([last_y, y])
            for vertical_y in range(np.abs(y - last_y)):
                frame.set_pixel(x+x_margin_size, min_y + vertical_y + bottom_margin_size, Pixel(cs.ACS_BLOCK, Color.GREEN))
        last_y = y
    
    # draws interest projection
    for x in range(width//2):
        cash = calculate_interest(cash_history[-1], interest_rate, x * interest_x_adjust_factor)
        y = int(np.clip(cash * cash_y_adjust_factor, 0, height-1))
        min_y = min([last_y, y])
        frame.set_pixel(x+width//2+x_margin_size, y + bottom_margin_size, Pixel(cs.ACS_BLOCK, Color.YELLOW))

    draw_y_axis_labels(frame, cash_history[-1]*2, y_offset=1)
    draw_x_axis_labels(frame, frame.width//2, x_margin_size, step_size=2, label_count=5)

def draw_ascii_str(frame: Frame, ascii_str: str, x_offset: int, y_offset: int, color=Color.WHITE):
    x = x_offset
    y = y_offset
    for ch in ascii_str:
        if ch == '\n':
            x = x_offset
            y -= 1
            continue
        frame.set_pixel(x, y, Pixel(ch, color))
        x += 1

def draw_bank_logo(frame: Frame):
    TEST = 53
    draw_ascii_str(frame, BANK_LOGO_B_STR, frame.width//2 - 26, frame.height//2 + 7, color=Color.GREEN)
    draw_ascii_str(frame, BANK_LOGO_ANK_STR, frame.width//2 - 26 + 13, frame.height//2 + 7, color=Color.YELLOW)
    draw_ascii_str(frame, BANK_LOGO_SQUIGGLE_STR, frame.width//2 - 26, frame.height//2 + 7 - 13, color=Color.WHITE)
    

def init_window_settings():
    cs.curs_set(False)
    cs.init_pair(int(Color.WHITE), cs.COLOR_WHITE, cs.COLOR_BLACK)
    cs.init_pair(int(Color.GREEN), cs.COLOR_GREEN, cs.COLOR_BLACK)
    cs.init_pair(int(Color.RED), cs.COLOR_RED, cs.COLOR_BLACK)
    cs.init_pair(int(Color.YELLOW), cs.COLOR_YELLOW, cs.COLOR_BLACK)

### JUST FOR TESTING HERE
def render_test(window: cs.window):
    init_window_settings()
    rows, cols = window.getmaxyx()
    frame = Frame(cols-1,rows-3-1)
    graph = build_data_from_func(lambda x: x**2, list(range(0, 1000)))
    draw_graph(frame, graph, color=Color.GREEN)
    draw_frame(window, frame)
    select_frame = build_select_frame(window, [
        SelectButton(name="Test Button", select=SelectState.SELECT, color=Color.GREEN),
        SelectButton(name="Test Button 2"),
        SelectField(name="Input amount", field="0kr")
    ])
    draw_select_frame(window, select_frame)
    window.refresh()
    time.sleep(20)
