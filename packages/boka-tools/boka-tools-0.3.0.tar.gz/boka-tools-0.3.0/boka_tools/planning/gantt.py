"""function to print gantt charts

Code by: Maarten Betman
DTED Hydronamic, Boskalis
maarten.betman@boskalis.com
date 05-Jun-2020

"""
# Standard libs
import datetime
from collections import OrderedDict
import math
from calendar import monthrange
import warnings

# Other libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import matplotlib.image as image
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# paper sizes in inches, landscape
PAPER_SIZES = dict(
    A0=[46.8, 33.1], A1=[33.1, 23.4], A2=[23.4, 16.5], A3=[16.5, 11.7], A4=[11.7, 8.3],
)


def gantt(
    df,
    datemin,
    datemax,
    date_cols_prefix=None,
    date_cols_sep="_",
    date_cols_suffix=None,
    date_bars_widths=None,
    date_bars_color_categories="",
    date_bars_color_type="planning",
    date_bars_colors=None,
    col_widths=None,
    footer_info=None,
    plt_title="Planning",
    papersize="A1",
    object_lines=16,
    max_objects=5,
    cols_table=None,
):
    """
    function to plot a gantt chart of a planning DataFrame

    Parameters
    ----------
    df : Pandas DataFrame
        Dataframe with activities to plot. Most comply with XER format in terms of columns names and defined pre- and
        suffixes for dates
    datemin : Datetime date
        Start date of plot
    datemax : Datetime date
        End date of plot
    date_cols_prefix : list
        list with prefix for column names, default ['Start', 'End']
    date_cols_sep : str
        separator between prefix and suffix defining the date columns, default "_"
    date_cols_suffix : list
        list with suffic for column names, default ['Start', 'End']
    date_bars_widths : list
        specify the height of the gantt bars. default [3, 1.5]
    date_bars_color_categories : str
        Define how gantt function should distinct between categories. Either column name or empty string to be
        passed. If empty string is passed distinction is made between the date categories (eg. planned / actual).
        default ''
    date_bars_color_type : str
        default 'planning'
    date_bars_colors : list
        Colors to use for gantt bars. Length should correspond with categories. default ['#65f794','blue']
    col_widths : list
    footer_info : dict
    plt_title : str
        title on top of gantt chart, default Planning
    papersize : str
        iso paper size format, default 'A1'
    object_lines : int
        number of lines be obs object, default 16
    max_objects : int
        number of obs object to plot, default 5
    cols_table : list
        df columns names for table, default ['Box', 'Task', 'Planned_Start', 'Planned_End', 'Actual_Start', 'Actual_End']

    Returns
    -------
    figure
        returns a figure containing a gantt chart

    Raises
    ------
    ValueError
        if lists are not corresponding in length

    """
    # cm to inches
    if date_cols_prefix is None:
        date_cols_prefix = ["Planned", "Actual"]
    if date_cols_suffix is None:
        date_cols_suffix = ["Start", "End"]
    if date_bars_widths is None:
        date_bars_widths = [3, 1.5]
    if date_bars_colors is None:
        date_bars_colors = [
            "#65f794",
            "blue",
        ]
    if cols_table is None:
        cols_table = [
            "Box",
            "Planned_Start",
            "Task",
            "Planned_End",
            "Actual_Start",
            "Actual_End",
        ]

    cm_to_inch = 0.393700787

    # font sizes
    font_size_table = 9
    font_size_title = 24
    font_size_footer = 12

    # footer info
    if footer_info is None:
        footer_info = dict(
            legend_title="Legend",
            page=1,
            total_pages=1,
            prepared_by="Mr. X",
            checked_by="Mr. Y",
            aproved_by="Mrs. Z",
            date=datetime.datetime.now().strftime("%d-%b-%Y"),
        )

    # Margins around planning in inch
    MARGINS = dict(
        top=(cm_to_inch * 4) / PAPER_SIZES[papersize][1],
        left=(cm_to_inch * 1) / PAPER_SIZES[papersize][0],
        right=(cm_to_inch * 1) / PAPER_SIZES[papersize][0],
        bottom=(cm_to_inch * 5) / PAPER_SIZES[papersize][1],
    )

    # Get bbox dimensions for planning axis
    width_table = 0.3
    rect = [
        width_table + MARGINS["right"],
        MARGINS["bottom"],
        (1 - MARGINS["left"] - MARGINS["right"] - width_table),
        (1 - MARGINS["top"] - MARGINS["bottom"]),
    ]  # xll, yll, width, height

    rect_table = [
        MARGINS["right"],
        MARGINS["bottom"],
        width_table,
        (1 - MARGINS["top"] - MARGINS["bottom"]),
    ]

    rect_header = [
        MARGINS["right"],
        (1 - MARGINS["top"] + (cm_to_inch * 1.5) / PAPER_SIZES[papersize][1]),
        (1 - MARGINS["right"] - MARGINS["left"]),
        (cm_to_inch * 2.0) / PAPER_SIZES[papersize][1],
    ]

    rect_footer = [
        MARGINS["right"],
        (cm_to_inch * 1) / PAPER_SIZES[papersize][1],
        (1 - MARGINS["right"] - MARGINS["left"]),
        (cm_to_inch * 3.75) / PAPER_SIZES[papersize][1],
    ]

    rect_img = [
        MARGINS["right"],
        (1 - MARGINS["top"] + (cm_to_inch * 1.7) / PAPER_SIZES[papersize][1]),
        (cm_to_inch * 4.0) / PAPER_SIZES[papersize][0],
        (cm_to_inch * 1.75) / PAPER_SIZES[papersize][1],
    ]

    # place logo in header
    # im = image.imread("./resources/JV.png") TODO Add logo support for top of gantt

    # make ax and figure
    fig = plt.figure(figsize=PAPER_SIZES[papersize], edgecolor="black", linewidth=3.0)
    ax = plt.axes(rect)
    ax_legend = plt.axes(rect_footer)
    ax_header = plt.axes(rect_header)
    # im_ax = fig.add_axes(rect_img, anchor="NE", zorder=10)
    ax_table = plt.axes(rect_table)

    x = 0
    for w in [1 / 3] * 3:
        ax_legend.add_patch(
            patches.Rectangle(
                (x, 0), w, 1, edgecolor="black", facecolor="none", linewidth=1.5
            )
        )
        x = x + w

    ax_table.axis("off")
    # im_ax.axis("off")
    ax_legend.set_xticks([])
    ax_legend.set_yticks([])
    ax_header.set_xticks([])
    ax_header.set_yticks([])

    # im_ax.imshow(im)

    # set styling dimension of chart
    barwidth_planned = 3
    barwidth_actual = barwidth_planned / 2
    activitywidth = 5
    whitespace_around_bars = 1

    # calc max number of lines
    max_lines = object_lines * max_objects

    # Date ranges for month and week headers
    date_range = np.arange(datemin, datemax, np.timedelta64(1, "M")).astype(
        datetime.date
    )
    date_range_total_days = sum([monthrange(x.year, x.month)[1] for x in date_range])
    week_nums = _find_weeks(
        datemin.astype(datetime.datetime), datemax.astype(datetime.date)
    )
    wk = _week_width(datemin.astype(datetime.date), datemax.astype(datetime.date))

    # add lines to df if maxlines is not satified
    missing_rows = max_lines - df.shape[0]
    for i in range(missing_rows):
        df = df.append(pd.Series(), ignore_index=True)

    # y-axis formatting
    ax.set_yticks(np.arange(0, 3.5 + (max_lines + 1) * activitywidth, activitywidth))
    ax.set_yticklabels([])
    ax.set_ylim(max_lines * activitywidth, 0)

    # x-axis tick locators
    months = mdates.MonthLocator()  # every month
    weeks = mdates.WeekdayLocator()
    date_fmt = mdates.DateFormatter("%Y-%b")

    # x-axis ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(date_fmt)
    ax.xaxis.set_minor_locator(weeks)

    ax.set_xlim(datemin, datemax)
    ax.xaxis.tick_top()
    ax.set_xticklabels([])

    # error checking
    if not len(date_cols_suffix) == 2:
        raise ValueError("Only a start and end suffix are allowed")

    if len(df) > max_lines:
        df = df.iloc[:80, :]
        warnings.warn("DataFrame truncated because it was more than 80 lines")

    # draw bars
    pos = 0
    row_colors = ["#e8e8e8", "white"] * 10
    rowColours = []

    if date_bars_color_type == "pandas_col":
        date_bars_color_category_list = list(df[date_bars_color_categories].unique())
    elif date_bars_color_type == "list":
        date_bars_color_category_list = date_bars_color_categories
    elif date_bars_color_type is None:
        pass
    else:
        pass

    # Plot bars
    for index, row in df.iterrows():
        for i, prefix in enumerate(date_cols_prefix):
            if date_bars_color_type == "pandas_col":
                cat = row[date_bars_color_categories]
                i_c = date_bars_color_category_list.index(cat)
                label = cat
            else:
                label = prefix
                i_c = i

            start = row[date_cols_sep.join([prefix, date_cols_suffix[0]])]
            end = row[date_cols_sep.join([prefix, date_cols_suffix[1]])]
            middle = activitywidth / 2 + pos * activitywidth

            if not isinstance(start, type(pd.NaT)):
                ax.broken_barh(
                    [(start, end - start)],
                    (middle - date_bars_widths[i] / 2, date_bars_widths[i]),
                    facecolor=date_bars_colors[i_c],
                    edgecolor="black",
                    label=label,
                )

        rowColours.append(row_colors[math.floor(pos / object_lines)])

        pos += 1

    header_height = 0.0125 / 0.75

    the_table = plt.table(
        cellText=df[cols_table]
        .astype(str)
        .replace("NaT", "")
        .replace("nan", "")
        .values,
        colWidths=col_widths,  # TODO Make something to look at string length in cell
        cellLoc="center",
        cellColours=[[x] * len(cols_table) for x in rowColours],
        bbox=(0.0, 0.0, 1, 1),
    )

    if col_widths is None:
        w = the_table.get_celld()[0, 0].get_width()

        for i in range(len(cols_table)):
            the_table.add_cell(
                -1, i, height=header_height, width=w, text=cols_table[i], loc="center"
            )

    else:
        for i, w in enumerate(col_widths):
            the_table.add_cell(
                -1, i, height=header_height, width=w, text=cols_table[i], loc="center"
            )

    # Grey bands
    for i in range(max_objects):
        if (i % 2) == 0:
            ax.axhspan(
                i * max_lines,
                (i + 1) * max_lines,
                facecolor="lightgrey",
                alpha=0.5,
                zorder=-100,
            )

    # Date line
    ax.axvline(datetime.datetime.now(), color="red", label="Today")

    ax.margins(y=(1 - barwidth_planned) / 2 / pos)
    ax.grid(linestyle="--", linewidth=1)

    # set title
    fig.suptitle(plt_title, fontsize=font_size_title)

    # Create legend and remove repeated label due to broken bar loop
    handles, labels = ax.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    ax_legend.legend(
        by_label.values(),
        by_label.keys(),
        loc="upper left",
        bbox_to_anchor=(0.005, 0.8),
        frameon=False,
        fontsize=font_size_table,
        ncol=4,
    )

    # add months at top of gantt chart
    table_dates = ax.table(
        cellText=[[x.strftime("%Y-%b") for x in date_range]],
        colWidths=[
            monthrange(x.year, x.month)[1] / date_range_total_days for x in date_range
        ],
        cellLoc="center",
        bbox=(0.0, 1.0125, 1.0, 0.0125),
    )

    # add weeks at top of gantt chart
    table_weeks = ax.table(
        cellText=[week_nums],
        colWidths=[
            (j - i).days / date_range_total_days for i, j in zip(wk[:-1], wk[1:])
        ],
        cellLoc="center",
        bbox=(0.0, 1.0, 1.0, 0.0125),
    )

    # redraw to change table fonts
    for t in [
        table_dates,
        table_weeks,
        the_table,
    ]:
        t.auto_set_font_size(False)
        t.set_fontsize(font_size_table)

    # insert text in footer
    ax_legend.text(
        0.005,
        0.9,
        footer_info["legend_title"],
        fontsize=font_size_footer,
        fontweight="bold",
        verticalalignment="top",
        horizontalalignment="left",
    )

    ax_legend.text(
        0.5,
        0.1,
        f"[page {footer_info['page']} of {footer_info['total_pages']}]",
        fontsize=font_size_footer,
        verticalalignment="center",
        horizontalalignment="center",
    )

    for i, key in enumerate(list(footer_info.keys())[-4:]):
        y_start = 0.65
        x_start = 0.9
        spacing_lines = 0.15
        ax_legend.text(
            x_start,
            y_start - (i * spacing_lines),
            key,
            fontsize=font_size_footer,
            verticalalignment="top",
            horizontalalignment="left",
        )
        ax_legend.text(
            x_start + 0.05,
            y_start - (i * spacing_lines),
            f":",
            fontsize=font_size_footer,
            verticalalignment="top",
            horizontalalignment="left",
        )
        ax_legend.text(
            x_start + 0.06,
            y_start - (i * spacing_lines),
            footer_info[key],
            fontsize=font_size_footer,
            verticalalignment="top",
            horizontalalignment="left",
        )

    fig.canvas.draw()
    plt.close()

    return fig


def _week_width(start, end):
    l = [start]
    for i in range((end - start).days + 1):
        d = start + datetime.timedelta(days=i)
        if d.weekday() == 1:
            l.append(d)
    l.append(end)
    return l


def _find_weeks(start, end):
    l = []
    for i in range((end - start).days + 1):
        d = (start + datetime.timedelta(days=i + 1)).isocalendar()  # e.g. (2011, 52)
        yearweek = "{}{:02}".format(*d)  # e.g. "201152"
        l.append(yearweek)
    return [x[-2:] for x in sorted(set(l))]
