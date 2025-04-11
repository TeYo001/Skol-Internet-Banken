from src.external_imports import *

class GraphError(Enum):
    EMPTY = 0
    UNEQUAL_POINT_COUNT = 1
    FUNCTION_ERROR = 2

@dataclass
class GraphData:
    x_points: list[float]
    y_points: list[float]
    x_min: float
    x_max: float
    y_min: float
    y_max: float

def build_data_from_points(x_points: list[float], y_points: list[float]) -> GraphData | GraphError:
    if len(x_points) != len(y_points):
        return GraphError.UNEQUAL_POINT_COUNT
    if len(x_points) == 0:
        return GraphError.EMPTY
    return GraphData(x_points=x_points,
                     y_points=y_points,
                     x_min=min(x_points),
                     x_max=max(x_points),
                     y_min=min(y_points),
                     y_max=max(y_points))

def build_data_from_func(func, x_points = list[float]) -> GraphData | GraphError:
    y_points = []
    for x in x_points:
        y_points.append(func(x))
    return GraphData(x_points=x_points,
                     y_points=y_points,
                     x_min=min(x_points),
                     x_max=max(x_points),
                     y_min=min(y_points),
                     y_max=max(y_points))
