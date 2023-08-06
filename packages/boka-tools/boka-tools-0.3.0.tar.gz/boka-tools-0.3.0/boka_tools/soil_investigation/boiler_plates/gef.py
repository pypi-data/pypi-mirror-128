import math
from datetime import datetime

import numpy as np
from pygef import ParseGEF


def standard_gef_plot(gef: ParseGEF) -> dict:
    """

    Parameters
    ----------
    gef : pygef.ParseGef
        parsed gef file by pygef

    Returns
    -------
    plot_props : dict
        Returns a dictionary containing all data and properties for plotting a GEF File
    """

    df = gef.df
    # get max and min depths and round up/down respectively
    ymin = math.floor(df.elevation_with_respect_to_NAP.min())
    ymax = math.ceil(df.elevation_with_respect_to_NAP.max())

    # set the meter tick interval
    y_int = 2

    # make the json object
    plot_props = dict(
        plots=dict(
            y_data=df.elevation_with_respect_to_NAP.values,
            plot_1=dict(
                ax="ax1",
                name="qc",
                type="plot",
                x_data=df.qc.values,
                kwargs=dict(color="black", ls="-", lw=1.5, label="qc"),
            ),
            plot_2=dict(
                ax="ax1_2",
                name="Rf",
                type="plot",
                x_data=df.friction_number.values,
                kwargs=dict(color="red", lw=1, label="Rf"),
            ),
            plot_3=dict(
                ax="ax2",
                name="fs",
                type="plot",
                x_data=df.fs.values,
                kwargs=dict(color="orange", ls="-", lw=1, label="fs"),
            ),
            plot_4=dict(
                ax="ax3",
                name="u2",
                type="plot",
                x_data=df.u2.values,
                kwargs=dict(color="blue", ls="-", lw=1.0, label="u2"),
            ),
        ),
        axes=dict(
            num=3,
            widths=[0.5, 0.25, 0.25],
            kwargs=dict(
                ax1=dict(xlim=[0, 10], xlabel="qt [MPa]", ylabel="Elevation [m+CD]"),
                ax2=dict(xlim=[0, 0.50], xlabel="fs [MPa]"),
                ax3=dict(xlim=[0, 1], xlabel="u2 [MPa]"),
                all=dict(
                    ylim=[ymin, ymax],
                    yticks=[x for x in range(ymin, ymax + y_int, y_int)],
                ),
            ),
            twiny=dict(
                ax1_2=dict(
                    twin="ax1",
                    kwargs=dict(
                        xticks=[x for x in range(0, 6, 1)],
                        xticklabels=["" if x == 0 else str(x) for x in range(0, 6, 1)],
                        xlim=[25, 0],
                        xlabel="Rf [%]",
                    ),
                )
            ),
        ),
        layout=dict(
            papersize="A4",
            margins=[1, 1, 1, 1],
            # logo='./hydronamic.tif'
        ),
        info=dict(
            pointid=[gef.test_id],
            row_spacing=np.linspace(0.6, 0.1, 5),
            general_titles=["CLIENT", "ENGINEER", "AC", "CONTRACTOR", "PROJECT"],
            general_values=[
                "Client A",
                "Consultant A",
                "Consultant B",
                "Boskalis",
                gef.project_id,
            ],
            location_titles=["AREA", "SUBAREA", "EASTING", "NORTHING", "ELEVATION"],
            location_values=["NA", "NA", gef.x, gef.y, gef.zid],
            location_units=["", "", "", "", " m+CD"],
            version_titles=[
                "CPT DATE",
                "PRINT DATE",
                "PREPARED BY",
                "CHECKED BY",
                "APPROVED BY",
            ],
            version_values=[
                gef.file_date.strftime("%d-%b-%Y"),
                datetime.now().strftime("%d-%b-%Y"),
                "MBET",
                "MBET",
                "MBET",
            ],
        ),
    )

    return plot_props
