from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch


def ic_colormap():
    """

    Returns
    -------

    """
    ic_colors = ["#d6a000", "#d2d600", "#02e595", "#005f9b", "#005f9b", "#7f5901"]
    ic_values = [0, 1.31, 2.05, 2.60, 2.95, 3.60]
    # ic_labels = ["Gravel", "Sands", "Sand mixtures", "Silt mixtures", "Clays", "Peats"]

    cmap = ListedColormap(ic_colors)
    norm = BoundaryNorm(ic_values, cmap.N, clip=True)

    return cmap, norm


def ic_legend():
    """
    Function to make a legend for Ic plots.
    Ic = Soil Behaviour type index

    Returns
    -------
    legend : list
        Returns a list with legend patches

    """
    ic_colors = ["#d6a000", "#d2d600", "#02e595", "#005f9b", "#005f9b", "#7f5901"]
    ic_values = [0, 1.31, 2.05, 2.60, 2.95, 3.60]
    ic_labels = ["Gravel", "Sands", "Sand mixtures", "Silt mixtures", "Clays", "Peats"]

    legend = []

    for c, s, l in zip(ic_colors, ic_values, ic_labels):
        entry = Patch(facecolor=c, edgecolor="black", label=l)
        legend.append(entry)

    return legend


def bh_colormap(su_in_log: str):
    """
    Function that returns the color code for the corresponding geological formation

    Parameters
    ----------
    su_in_log : str
        GEOL_LEG entry in the borehole log

    Returns
    -------
    color : str
        Returns string with correct color code
    """
    su_in_log_stripped = su_in_log.strip()

    colors = [
        "#E6E67D",
        "#99CCFF",
        "#CCFF99",
        "#FFFF99",
        "#9999FF",
        "#C0C0C0",
        "#C0C0C0",
        "#C0C0C0",
        "#C0C0C0",
        "#C0C0C0",
        "#C0C0C0",
        "#C0C0C0",
        "#878686",
        "#878686",
        "#878686",
        "#878686",
        "#878686",
        "#878686",
    ]


    su = [
        "FILL",
        "M",
        "E",
        "F1",
        "F2",
        "S",
        "S(I)",
        "S(II)",
        "S(III)",
        "S(IV)",
        "S(V)",
        "S(VI)",
        "G(V)",
        "G(IV)",
        "G(VI)",
        "G(III)",
        "G(II)",
        "G(I)",
    ]
    labels = [
        "Sand (fill)",
        "Marine Clay",
        "Estuarine Clay",
        "Fluvial Sand",
        "Fluvial Clay",
        "Residual Soil",
        "Granite"
    ]

    if su_in_log_stripped not in su:
        raise ValueError(f"Soil Unit not known - {su_in_log_stripped}")

    return colors[su.index(su_in_log_stripped)]


def bh_legend():
    """
    Function to make the borehole legend

    Returns
    -------
    legend : list
        returns a list with legend patches
    """
    colors = [
        "#E6E67D",
        "#99CCFF",
        "#CCFF99",
        "#FFFF99",
        "#9999FF",
        "#C0C0C0",
        "#878686",
    ]

    su = ["FILL", "M", "E", "F1", "F2", "S"]

    labels = [
        "Sand (fill)",
        "Marine Clay",
        "Estuarine Clay",
        "Fluvial Sand",
        "Fluvial Clay",
        "Residual Soil",
        "Granite"
    ]

    legend = []

    for c, s, l in zip(colors, su, labels):
        entry = Patch(facecolor=c, edgecolor="black", label=f"{s} - {l}")
        legend.append(entry)

    return legend
