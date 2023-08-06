from typing import List, Optional, Union, Dict, Any
from typing_extensions import Literal

from pydantic import BaseModel, FilePath, Field, validator
from pydantic.color import Color
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm


def _convert_color(color: Color) -> str:
    if isinstance(color, Color):
        return color.as_hex()
    else:
        return color


class LineKwargs(BaseModel):
    label: str = Field(..., description="Label to appear in legend")
    color: Color = Field("black", description="Line color")
    ls: Literal[
        "-", "--", "-.", ":", " ", "", "solid", "dashed", "dashdot", "dotted"
    ] = Field("-", description="Line style of plot")
    lw: float = Field(1.5, lt=5.0, gt=0.1, description="Line width of plot")

    _normalize_color = validator("color", allow_reuse=True)(_convert_color)


class ScatterKwargs(BaseModel):
    label: str = Field(..., description="Label to appear in legend")
    c: Union[
        Color, List[Union[float, None]]
    ] = None  # Field("white", description="Face color of marker")
    cmap: Any = None
    norm: Any = None
    edgecolor: Color = None  # Field("black", description="Edge color of marker")
    s: int = Field(100, gt=1, lt=150, description="Marker size")
    marker: Literal["^", "v", "<", ">", "o", "x"] = None  # Field(
    #     "^", description="Marker style"
    # )

    _normalize_c = validator("c", allow_reuse=True)(_convert_color)
    _normalize_edgecolor = validator("edgecolor", allow_reuse=True)(_convert_color)


class BarKwargs(BaseModel):
    label: str = Field(..., description="Label to appear in legend")
    width: Optional[float] = Field(0.5, gt=0.1, lt=2, description="Width of bar")
    bottom: List[float] = Field(
        ..., description="List to indicate y position of bottom bar"
    )
    color: List[str] = Field(..., description="List of bar colors")
    hatch: Optional[Literal["...", "..", "\\", "/"]] = Field(
        None, description="Hatch style"
    )

    # _normalize_color = validator("color", allow_reuse=True)(_convert_color)


class AxKwargs(BaseModel):
    xlim: List[float] = None
    xlabel: str = None
    ylim: List[float] = None
    ylabel: str = None
    xticks: Optional[List[float]]
    yticks: Optional[List[float]]
    xticklabels: Optional[List[str]]
    yticklabels: Optional[List[str]]


class Plot(BaseModel):
    ax: str
    name: str
    type: Literal["plot", "scatter", "axvline", "axhline", "bar"] = "plot"
    x_data: List[float] = None
    args: List[List[Union[float, None]]] = None
    kwargs: Optional[Any]


class PlotContainer(BaseModel):
    y_data: List[float]
    plots: List[Plot]


class Twiny(BaseModel):
    twin: str
    kwargs: AxKwargs


class Axes(BaseModel):
    num: int
    widths: List[float]
    kwargs: Dict[str, AxKwargs]
    twiny: Optional[Dict[str, Twiny]]

    @validator("widths")
    def validate_widths(cls, v):
        assert sum(v) == 1.0, "sum of all widths must be 1"
        return v


class Layout(BaseModel):
    papersize: Literal["A4", "A3"] = "A4"
    margins: List[float] = [1, 1, 1, 1]
    logo: Optional[FilePath]


class Info(BaseModel):
    pointid: List[str]
    row_spacing: List[float] = np.linspace(0.6, 0.1, 5)
    general_titles: List[str] = ["CLIENT", "ENGINEER", "AC", "CONTRACTOR", "PROJECT"]
    general_values: List[str]
    location_titles: List[str] = ["AREA", "SUBAREA", "EASTING", "NORTHING", "ELEVATION"]
    location_values: List[str]
    location_units: List[str]
    version_titles: List[str] = [
        "CPT DATE",
        "PRINT DATE",
        "PREPARED BY",
        "CHECKED BY",
        "APPROVED BY",
    ]
    version_values: List[str]


class PlotProps(BaseModel):
    plots: PlotContainer
    axes: Axes
    layout: Layout
    info: Info


if __name__ == "__main__":
    print(PlotProps.schema_json(indent=2))
