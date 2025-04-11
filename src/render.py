### THIS IS WHERE WE CAN PUT SOME MORE COOL LOOKING GRAPHICS HANDLING ###
# Note(TeYo): This is basically what will set this project apart from the others and shit, I'm quite used to doing these kind of things so it should
# hopefully be kinda cool

from src.external_imports import *
from src.data import *

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

def draw_graph(frame: Frame, graph: GraphData, min_delta_x=0.5, min_delta_y=0.5, color=Color.WHITE):
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
        frame.set_pixel(adjusted_x_points[i], adjusted_y_points[i], Pixel(cs.ACS_BLOCK, ch_color=color))

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
