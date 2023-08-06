from collections import OrderedDict

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib.image as image
from munch import *

__dev__ = True


def _fig_to_ax(fig, ax, coords):
    display_coords = fig.transFigure.transform(coords)
    inv = ax.transAxes.inverted()
    return inv.transform(display_coords)


def _ax_to_fig(fig, ax, coords):
    display_coords = ax.transAxes.transform(coords)
    inv = fig.transFigure.inverted()
    return inv.transform(display_coords)


def plot_si_results(plot_props):
    """

    Parameters
    ----------
    plot_props : dict
        Dictionary containing all data and kwargs for the plots
    """
    # if plot props is not a munch, turn it into one.
    if not isinstance(plot_props, Munch):
        plot_props = munchify(plot_props)

    # cm to inches
    cm_to_inch = 0.393700787

    # Default papersizes in inches and choose one according to dict
    PAPER_SIZES = dict(A3=[16.5, 11.7], A4=[8.30, 11.7],)  # A3 Landscape  # A4 Portrait

    papersize = PAPER_SIZES[plot_props.layout.papersize]

    # Change some rcParams
    plt.rcParams["font.family"] = "arial"
    plt.rcParams["font.size"] = 8.5
    plt.rcParams["figure.dpi"] = 80
    plt.rcParams["savefig.dpi"] = 400
    plt.rcParams['hatch.linewidth'] = 0.1

    # initialize figure, size in inches
    fig = plt.figure(figsize=papersize)

    # set margin around figure
    margins = Munch(
        left=(cm_to_inch * plot_props.layout.margins[0]),
        right=(cm_to_inch * plot_props.layout.margins[1]),
        top=(cm_to_inch * plot_props.layout.margins[2]),
        bottom=(cm_to_inch * plot_props.layout.margins[3]),
    )

    fig_layout = Munch()
    fig_layout.dimensions = Munch()

    # main dimensions axis in cm, w x h. List comprehension to convert to inches
    fig_layout.dimensions.h_header = 3.5 * cm_to_inch
    fig_layout.dimensions.h_spacing_header_title = 0.1 * cm_to_inch
    fig_layout.dimensions.h_title = 1.0 * cm_to_inch
    fig_layout.dimensions.h_spacing_axis_footer = 0.1 * cm_to_inch
    fig_layout.dimensions.h_footer = 2.0 * cm_to_inch
    fig_layout.dimensions.level_box_indent = 1.25 * cm_to_inch
    fig_layout.dimensions.logo = 1.5 * cm_to_inch

    fig_layout.dimensions.h_axis = (
        papersize[1]
        - margins.top
        - margins.bottom
        - sum(fig_layout.dimensions[h] for h in fig_layout.dimensions if 'h_' in h)
    )

    fig_layout.dimensions.w_axis = (
        papersize[0]
        - margins.left
        - margins.right
        - fig_layout.dimensions.level_box_indent
    )
    fig_layout.dimensions.h_level = fig_layout.dimensions.h_axis

    fig_layout.axes = Munch()
    fig_layout.axes.dimensions = Munch()

    for i in range(plot_props.axes.num):
        fig_layout.axes.dimensions["ax" + str(i + 1)] = [
            plot_props.axes.widths[i] * fig_layout.dimensions.w_axis,
            fig_layout.dimensions.h_axis,
        ]

    fig_layout.axes.dimensions.header = [
        fig_layout.dimensions.w_axis + fig_layout.dimensions.level_box_indent,
        fig_layout.dimensions.h_header,
    ]
    fig_layout.axes.dimensions.title = [
        fig_layout.dimensions.w_axis + fig_layout.dimensions.level_box_indent,
        fig_layout.dimensions.h_title,
    ]
    fig_layout.axes.dimensions.level = [
        fig_layout.dimensions.level_box_indent,
        fig_layout.dimensions.h_axis,
    ]
    fig_layout.axes.dimensions.footer = [
        fig_layout.dimensions.w_axis + fig_layout.dimensions.level_box_indent,
        fig_layout.dimensions.h_footer,
    ]

    fig_layout.axes.rect = Munch()

    # make header boxes
    yll_offset = 0
    for box in [
        "footer",
        "h_spacing_axis_footer",
        "level",
        "title",
        "h_spacing_header_title",
        "header",
    ]:
        if "spacing" not in box:
            fig_layout.axes.rect[box] = [
                margins.left / papersize[0],  # xll
                (margins.bottom + yll_offset) / papersize[1],  # yll
                fig_layout.axes.dimensions[box][0] / papersize[0],  # dx
                fig_layout.axes.dimensions[box][1] / papersize[1],  # dy
            ]

            yll_offset = yll_offset + fig_layout.dimensions["h_" + box]
        else:
            yll_offset = yll_offset + fig_layout.dimensions[box]

    # make axis for plotting
    xll_offset = fig_layout.dimensions.level_box_indent
    for i in range(plot_props.axes.num):
        fig_layout.axes.rect["ax" + str(i + 1)] = [
            (margins.left + xll_offset) / papersize[0],  # xll
            fig_layout.axes.rect.level[1],
            fig_layout.axes.dimensions["ax" + str(i + 1)][0] / papersize[0],
            fig_layout.axes.dimensions["ax" + str(i + 1)][1] / papersize[1],
        ]

        xll_offset = xll_offset + fig_layout.axes.dimensions["ax" + str(i + 1)][0]

        # plot the info headers
    fig_layout.axes.axs_info = Munch()
    for ax in ["footer", "level", "title", "header"]:
        fig_layout.axes.axs_info[ax] = plt.axes(
            fig_layout.axes.rect[ax], facecolor="none"
        )

    # Place logo..
    im_xy0 = _ax_to_fig(fig, fig_layout.axes.axs_info.header, [0.00, 0.65])
    ax_logo = plt.axes(
        [
            im_xy0[0] + (0.25 * cm_to_inch / papersize[1]),
            im_xy0[1] + (0.10 * cm_to_inch / papersize[1]),
            (3 * cm_to_inch / papersize[0]),
            (1 * cm_to_inch / papersize[1]),
        ]
    )
    ax_logo.axis("off")

    if 'logo' in plot_props.layout.keys():
        ax_logo.imshow(
            image.imread(plot_props.layout.logo),
            zorder=-1,
            origin="upper",
            interpolation="nearest",
        )

    # plot the graphs axes..
    fig_layout.axes.axs_plots = Munch()
    for i in range(plot_props.axes.num):
        fig_layout.axes.axs_plots["ax" + str(i + 1)] = plt.axes(
            fig_layout.axes.rect["ax" + str(i + 1)],
            **plot_props.axes.kwargs["ax" + str(i + 1)],
            **plot_props.axes.kwargs.all
        )

    # make twiny axes if any..
    if "twiny" in [x for x in plot_props.axes]:
        for twiny in plot_props.axes.twiny:
            ref_ax = plot_props.axes.twiny[twiny].twin
            fig_layout.axes.axs_plots[twiny] = fig_layout.axes.axs_plots[ref_ax].twiny()

            ax = fig_layout.axes.axs_plots[twiny]
            kwargs = plot_props.axes.twiny[twiny].kwargs
            for key in kwargs:
                getattr(ax, "set_%s" % key)(kwargs.get(key))

    # ax formatting
    try:
        no_grid = plot_props.axes.no_grid
    except AttributeError:
        no_grid = []

    for key in fig_layout.axes.axs_plots:
        ax = fig_layout.axes.axs_plots[key]

        if key in no_grid:
            pass
        else:
            ax.grid(linestyle="--")

        ax.xaxis.set_label_position("top")
        ax.xaxis.tick_top()
        ax.yaxis.set_minor_locator(MultipleLocator(0.25))

        # set the alignment for outer ticklabels
        ticklabels = ax.get_xticklabels()
        ticklabels[0].set_ha("left")
        ticklabels[-1].set_ha("right")

        # set the alignment for outer ticklabels
        ticklabels = ax.get_yticklabels()
        ticklabels[-1].set_va("top")
        ticklabels[0].set_va("bottom")

        # move secondary x-axis to the inside
        if "_" in key:
            ax.tick_params(axis="x", direction="in", pad=-15)
        else:
            ax.tick_params(axis="both", pad=1)

    # turn of labels and/or ticks for some of the axis
    for key in fig_layout.axes.axs_plots:
        ax = fig_layout.axes.axs_plots[key]
        if "ax1" not in key:
            ax.set_yticklabels([])

    for key in fig_layout.axes.axs_info:
        ax = fig_layout.axes.axs_info[key]
        ax.set_xticks([])
        ax.set_yticks([])

    # place divider lines in footer and title block
    for i in range(plot_props.axes.num):
        y = fig_layout.axes.rect.title[1]
        x = fig_layout.axes.rect["ax" + str(i + 1)][0]
        x_t = _fig_to_ax(fig, fig_layout.axes.axs_info.title, [x, y])[0]
        for ax in ["footer", "title"]:
            fig_layout.axes.axs_info[ax].axvline(x_t, color="black", lw=0.75)

    # make the plots!!
    for plot in plot_props.plots:
        y_data = plot_props.plots.y_data
        if "plot" in plot.lower():
            ax = fig_layout.axes.axs_plots[plot_props.plots[plot].ax]
            x_data = plot_props.plots[plot].x_data
            kwargs = plot_props.plots[plot].kwargs
            plot_type = plot_props.plots[plot].type

            if 'args' in plot_props.plots[plot].keys():
                args = tuple(plot_props.plots[plot].args)
            else:
                args = (x_data, y_data)

            getattr(ax, plot_type)(*args, **kwargs)

    # legends
    for key in fig_layout.axes.axs_plots:

        # filter out the twin y axis to avoid legend mistakes.
        if "_" not in key:
            ax = fig_layout.axes.axs_plots[key]
            handles, labels = ax.get_legend_handles_labels()

            # get handles from twin y axis if available.
            try:
                ax_2 = fig_layout.axes.axs_plots[key + "_2"]
                handles_2, labels_2 = ax_2.get_legend_handles_labels()
                handles = handles + handles_2
                labels = labels + labels_2
            except KeyError:
                pass

            # Filter out double entries
            by_label = OrderedDict(zip(labels, handles))
            # Set position, place top left point of legend at bottom left point of ax.
            bbox = ax.get_position()
            xy = (bbox.xmin, bbox.ymin)
            legend_kwargs = dict(
                loc="upper left",
                bbox_to_anchor=xy,
                bbox_transform=fig.transFigure,
                frameon=False,)
            # Check if custom legend is available
            try:
                ax.legend(
                    handles=plot_props.axes.custom_legend[key],
                    fontsize='x-small',
                    ncol=1,
                    **legend_kwargs
                    )
            except (KeyError, AttributeError):
                ax.legend(
                    by_label.values(),
                    by_label.keys(),
                    ncol=2,
                    **legend_kwargs
                )

    # Header info and styling
    hline_y = 0.65
    fig_layout.axes.axs_info.header.axhline(hline_y, lw=0.80, color="black")

    header = fig_layout.axes.axs_info.header
    sep = ":"
    sep_cols = [1, 4, 7]
    cols = [key for key in plot_props.info if "titles" in key or "values" in key]
    cols_spacing = [
        0.0125,
        0.1300,
        0.1500,
        0.5000,
        0.6175,
        0.6375,
        0.7500,
        0.8675,
        0.8875,
    ]

    if plot_props.layout.papersize == "A3":
        cols_spacing = [s * 0.5 for s in cols_spacing]

    for s in sep_cols:
        cols.insert(s, sep)

    for i, x in enumerate(cols_spacing):
        for j, y in enumerate(plot_props.info.row_spacing):
            if cols[i] == sep:
                header.text(
                    x, y, sep, verticalalignment="top", horizontalalignment="left"
                )
            else:
                header.text(
                    x,
                    y,
                    plot_props.info[cols[i]][j],
                    verticalalignment="top",
                    horizontalalignment="left",
                )

    header.text(
        0.99,
        1.0 - ((1 - hline_y) / 2),
        " - ".join(plot_props.info.pointid),
        verticalalignment="center",
        horizontalalignment="right",
        fontsize=16,
        fontweight="bold",
    )

    plt.close()
    return fig
