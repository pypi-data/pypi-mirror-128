import math
from datetime import datetime
import textwrap

import numpy as np
import pandas as pd

from .legends_styles import *
from ..sql.gint_sql import *


def gint_plot_cpt_lab_bh(engine, pointid_cpt, pointid_bh):

    # make tuple of the pointids
    pointids = (pointid_cpt, pointid_bh)

    # get data from gINT database. make sure CTP_COMB and BH_COMB views are made
    point = pd.read_sql_query(point_data.format(**{"pointids": str(pointids)}), engine)
    cpt = pd.read_sql_query(cpt_data.format(**{"pointid": str(pointid_cpt)}), engine)
    bh = pd.read_sql_query(bh_data.format(**{"pointid": str(pointid_bh)}), engine)
    lab = (
        pd.read_sql_query(lab_data.format(**{"pointid": str(pointid_bh)}), engine)
        .sort_values("Depth")
        .drop_duplicates()
    )

    # separate the columns for readability of the code
    qt = cpt.Total_Cone_Resistance
    rf = cpt.Friction_Ratio
    fs = cpt.Sleeve_Friction_Resistance
    u0 = cpt.In_Situ_Pore_Pressure
    sigma = cpt.Total_Stress
    sigma_eff = cpt.Effective_Stress
    u2 = cpt.Porewater_Pressure_2
    su = cpt.Undrained_Shear_Strength_1
    pc = cpt.Preconsolidation_Stress_1
    elevation = cpt.Elevation

    lab_y = lab.Elevation
    lab_su_uu = lab.UU_Su
    lab_su_ciu = lab.CIU_Su
    lab_pc = lab.Preconsolidation_Pressure

    bh_x = [0.5] * len(bh)
    bh_height = bh.Thickness
    bh_bottom = bh.Elevation_Top

    # set bh colors
    bh_color = []
    for gu in bh.Geology_Unit_1.values:
        bh_color.append(bh_colormap(gu))

    # get max and min depths and round up/down respectively
    ymin, ymax = math.floor(elevation.min()), math.ceil(elevation.max())

    # set the meter tick interval
    y_int = 2

    # make the json object
    plot_props = dict(
        plots=dict(
            y_data=elevation,
            plot_1=dict(
                ax="ax1",
                name="qc",
                type="plot",
                x_data=qt,
                kwargs=dict(color="black", ls="-", lw=1.5, label="qc"),
            ),
            plot_2=dict(
                ax="ax1_2",
                name="Rf",
                type="plot",
                x_data=rf,
                kwargs=dict(color="red", lw=1, label="Rf"),
            ),
            plot_3=dict(
                ax="ax2",
                name="fs",
                type="plot",
                x_data=fs,
                kwargs=dict(color="orange", ls="-", lw=1, label="fs"),
            ),
            plot_4=dict(
                ax="ax3",
                name="u0",
                type="plot",
                x_data=u0,
                kwargs=dict(color="darkblue", ls="-", lw=1.0, label="u0"),
            ),
            plot_5=dict(
                ax="ax3",
                name="u2",
                type="plot",
                x_data=u2,
                kwargs=dict(color="blue", ls="-", lw=1.0, label="u2"),
            ),
            plot_6=dict(
                ax="ax4",
                name="borehole",
                type="bar",
                x_data=[],
                args=[bh_x, bh_height],
                kwargs=dict(
                    width=0.5,
                    bottom=bh_bottom,
                    color=bh_color,
                    label="BH Log",
                    hatch="...",
                    edgecolor="black",
                ),
            ),
            plot_7=dict(
                ax="ax6",
                name="su",
                type="plot",
                x_data=su,
                kwargs=dict(color="black", label="Su - Nkt"),
            ),
            plot_8=dict(
                ax="ax6",
                name="su_req",
                type="axvline",
                x_data=[],
                args=[23],
                kwargs=dict(color="red", label="Su - Req."),
            ),
            plot_9=dict(
                ax="ax6",
                name="su_lab_uu",
                type="scatter",
                x_data=[],
                args=[lab_su_uu, lab_y],
                kwargs=dict(
                    c="white", s=100, marker="^", edgecolor="black", label="Su - UU"
                ),
            ),
            plot_10=dict(
                ax="ax6",
                name="su_lab_ciu",
                type="scatter",
                x_data=[],
                args=[lab_su_ciu, lab_y],
                kwargs=dict(
                    c="white", s=100, marker="v", edgecolor="black", label="Su - CIU"
                ),
            ),
            plot_11=dict(
                ax="ax5",
                name="u0",
                type="plot",
                x_data=u0,
                kwargs=dict(color="blue", label="u0"),
            ),
            plot_12=dict(
                ax="ax5",
                name="sigma",
                type="plot",
                x_data=sigma,
                kwargs=dict(color="black", label="sigma"),
            ),
            plot_13=dict(
                ax="ax5",
                name="sigma_eff",
                type="plot",
                x_data=sigma_eff,
                kwargs=dict(color="orange", label="sigma_eff"),
            ),
            plot_14=dict(
                ax="ax7",
                name="pc",
                type="plot",
                x_data=pc,
                kwargs=dict(color="orange", label="pc - alpha"),
            ),
            plot_15=dict(
                ax="ax7",
                name="pc_oed",
                type="scatter",
                x_data=[],
                args=[lab_pc, lab_y],
                kwargs=dict(
                    c="white", s=100, marker="^", edgecolor="black", label="Pc - OED"
                ),
            ),
            plot_16=dict(
                ax="ax7",
                name="sigma_eff",
                type="plot",
                x_data=sigma_eff,
                kwargs=dict(color="green", label="sigma_eff"),
            ),
        ),
        axes=dict(
            num=7,
            widths=[0.25, 0.125, 0.125, 0.08, 0.14, 0.14, 0.14],
            kwargs=dict(
                ax1=dict(
                    xlim=[0, 10],
                    xlabel="Cone Resistance [MPa]",
                    ylabel="Elevation [m+CD]",
                ),
                ax2=dict(xlim=[0, 100], xlabel="Friction [kPa]"),
                ax3=dict(xlim=[0, 150], xlabel="Pressure [kPa]"),
                ax4=dict(xlim=[0, 1], xticks=[0, 1], xticklabels=[], xlabel="BH Log"),
                ax5=dict(xlim=[0, 800], xlabel="Stress [kPa]"),
                ax6=dict(xlim=[0, 100], xlabel="SU [kPa]"),
                ax7=dict(xlim=[0, 800], xlabel="Pre-consolidation Stress [kPa]"),
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
            custom_legend=dict(
                ax4=bh_legend()
                )
        ),
        layout=dict(
            papersize="A3",
            margins=[1, 1, 1, 1],
            # logo=r'D:\Users\mbet\OneDrive - boskalis.com\9. PEng\a. Pulau Tekong\02. GIS\a. QGIS files\Logo\JV.png'
        ),
        info=dict(
            pointid=[p for p in pointids],
            row_spacing=np.linspace(0.6, 0.1, 5),
            general_titles=["CLIENT", "SO Rep", "PE-GEO", "CONTRACTOR", "PROJECT"],
            general_values=[
                "Housing & Development Board",
                "Surbana Jurong",
                "AECOM",
                "BPJV",
                "Pulau Tekong Polder Development",
            ],
            location_titles=["AREA", "PANEL", "EASTING", "NORTHING", "ELEVATION"],
            location_values=[
                point[x].iloc[0]
                for x in ["Area", "Box", "Easting", "Northing", "Elevation"]
            ],
            location_units=["", "", "", "", " m+CD"],
            version_titles=[
                "CPT DATE",
                "PRINT DATE",
                "PREPARED BY",
                "CHECKED BY",
                "APPROVED BY",
            ],
            version_values=[
                point["DateTime"].iloc[0].strftime("%d-%b-%Y"),
                datetime.now().strftime("%d-%b-%Y"),
                "MBET",
                "ANAM",
                "LBOL",
            ],
        ),
    )

    return plot_props


def standard_gint_cpt_plot(engine, pointid):

    # make tuple of the pointids
    pointids = (pointid, )

    # get data from gINT database. make sure CTP_COMB and BH_COMB views are made
    point = pd.read_sql_query(point_data_single.format(**{"pointid": str(pointid)}), engine)
    cpt = pd.read_sql_query(cpt_data.format(**{"pointid": str(pointid)}), engine)

    # separate the columns for readability of the code
    qt = cpt.Total_Cone_Resistance
    rf = cpt.Friction_Ratio
    fs = cpt.Sleeve_Friction_Resistance
    u0 = cpt.In_Situ_Pore_Pressure
    sigma = cpt.Total_Stress
    sigma_eff = cpt.Effective_Stress
    u2 = cpt.Porewater_Pressure_2
    su = cpt.Undrained_Shear_Strength_1
    pc = cpt.Preconsolidation_Stress_1
    elevation = cpt.Elevation

    # get max and min depths and round up/down respectively
    ymin, ymax = math.floor(elevation.min()), math.ceil(elevation.max())

    # set the meter tick interval
    y_int = 2

    # make the json object
    plot_props = dict(
        plots=dict(
            y_data=elevation,
            plot_1=dict(
                ax="ax1",
                name="qc",
                type="plot",
                x_data=qt,
                kwargs=dict(color="black", ls="-", lw=1.5, label="qc"),
                ),
            plot_2=dict(
                ax="ax1_2",
                name="Rf",
                type="plot",
                x_data=rf,
                kwargs=dict(color="red", lw=1, label="Rf"),
                ),
            plot_3=dict(
                ax="ax2",
                name="fs",
                type="plot",
                x_data=fs,
                kwargs=dict(color="orange", ls="-", lw=1, label="fs"),
                ),
            plot_4=dict(
                ax="ax3",
                name="u0",
                type="plot",
                x_data=u0,
                kwargs=dict(color="darkblue", ls="-", lw=1.0, label="u0"),
                ),
            plot_5=dict(
                ax="ax3",
                name="u2",
                type="plot",
                x_data=u2,
                kwargs=dict(color="blue", ls="-", lw=1.0, label="u2"),
                ),
            ),
        axes=dict(
            num=3,
            widths=[0.50, 0.25, 0.25],
            kwargs=dict(
                ax1=dict(
                    xlim=[0, 10],
                    xlabel="Cone Resistance [MPa]",
                    ylabel="Elevation [m+CD]",
                    ),
                ax2=dict(xlim=[0, 100], xlabel="Friction [kPa]"),
                ax3=dict(xlim=[0, 150], xlabel="Pressure [kPa]"),
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
            custom_legend=dict(
                ax4=bh_legend()
                )
            ),
        layout=dict(
            papersize="A4",
            margins=[1, 1, 1, 1],
            # logo=r'D:\Users\mbet\OneDrive - boskalis.com\9. PEng\a. Pulau Tekong\02. GIS\a. QGIS files\Logo\JV.png'
            ),
        info=dict(
            pointid=[p for p in pointids],
            row_spacing=np.linspace(0.6, 0.1, 5),
            general_titles=["CLIENT", "SO Rep", "PE-GEO", "CONTRACTOR", "PROJECT"],
            general_values=[
                "Housing & Development Board",
                "Surbana Jurong",
                "AECOM",
                "BPJV",
                "Pulau Tekong Polder Development",
                ],
            location_titles=["AREA", "PANEL", "EASTING", "NORTHING", "ELEVATION"],
            location_values=[
                point[x].iloc[0]
                for x in ["Area", "Box", "Easting", "Northing", "Elevation"]
                ],
            location_units=["", "", "", "", " m+CD"],
            version_titles=[
                "CPT DATE",
                "PRINT DATE",
                "PREPARED BY",
                "CHECKED BY",
                "APPROVED BY",
                ],
            version_values=[
                point["DateTime"].iloc[0].strftime("%d-%b-%Y"),
                datetime.now().strftime("%d-%b-%Y"),
                "MBET",
                "ANAM",
                "LBOL",
                ],
            ),
        )

    return plot_props


def su_gint_cpt_plot(engine, pointid):

    # make tuple of the pointids
    pointids = (pointid, )

    # get data from gINT database. make sure CTP_COMB and BH_COMB views are made
    point = pd.read_sql_query(point_data_single.format(**{"pointid": str(pointid)}), engine)
    cpt = pd.read_sql_query(cpt_data.format(**{"pointid": str(pointid)}), engine)

    # separate the columns for readability of the code
    qt = cpt.Total_Cone_Resistance
    rf = cpt.Friction_Ratio
    fs = cpt.Sleeve_Friction_Resistance
    u0 = cpt.In_Situ_Pore_Pressure
    qnet = cpt.Net_Cone_Resistance
    sigma = cpt.Total_Stress
    sigma_eff = cpt.Effective_Stress
    u2 = cpt.Porewater_Pressure_2
    su = cpt.Undrained_Shear_Strength_1
    pc = cpt.Preconsolidation_Stress_1
    elevation = cpt.Elevation

    # get max and min depths and round up/down respectively
    ymin, ymax = math.floor(elevation.min()), math.ceil(elevation.max())

    # set the meter tick interval
    y_int = 2

    # make the json object
    plot_props = dict(
        plots=dict(
            y_data=elevation,
            plot_1=dict(
                ax="ax1",
                name="qc",
                type="plot",
                x_data=qt,
                kwargs=dict(color="black", ls="-", lw=1.5, label="$q_{t}$"),
                ),
            plot_2=dict(
                ax="ax1_2",
                name="Rf",
                type="plot",
                x_data=rf,
                kwargs=dict(color="red", lw=1, label="$Rf$ [%]"),
                ),
            plot_3=dict(
                ax="ax2",
                name="qnet",
                type="plot",
                x_data=qnet*1000,
                kwargs=dict(color="black", ls="-", lw=1, label="$q_{net}$"),
                ),
            plot_4=dict(
                ax="ax3",
                name="u0",
                type="plot",
                x_data=u0,
                kwargs=dict(color="darkblue", ls="-", lw=1.0, label="$u_{0}$"),
                ),
            plot_5=dict(
                ax="ax3",
                name="u2",
                type="plot",
                x_data=u2,
                kwargs=dict(color="blue", ls="-", lw=1.0, label="$u_{2}$"),
                ),
            plot_6=dict(
                ax="ax3",
                name="sigma",
                type="plot",
                x_data=sigma,
                kwargs=dict(color="black", ls="--", lw=1.0, label="$\sigma_{v}$"),
                ),
            plot_7=dict(
                ax="ax3",
                name="sigma",
                type="plot",
                x_data=sigma_eff,
                kwargs=dict(color="black", ls="-", lw=1.0, label="$\sigma'_{v}$"),
                ),
            plot_10=dict(
                ax="ax4",
                name="su",
                type="plot",
                x_data=su,
                kwargs=dict(color="orange", ls="-", lw=1.0, label="$su$"),
                ),
            plot_11=dict(
                ax="ax4",
                name="su_req",
                type="axvline",
                x_data=[],
                args = [23],
                kwargs=dict(color="red", ls="-", lw=1.0, label="Req."),
                ),
            plot_8=dict(
                ax="ax4",
                name="sigma_eff",
                type="plot",
                x_data=sigma_eff * 0.23,
                kwargs=dict(color="black", ls="--", lw=1.0, label="$.23 * \sigma'_{v}$"),
                ),
            plot_9=dict(
                ax="ax4",
                name="sigma_eff",
                type="plot",
                x_data=sigma_eff * 0.28,
                kwargs=dict(color="black", ls="-.", lw=1.0, label="$.28 * \sigma'_{v}$"),
                ),
            ),
        axes=dict(
            num=4,
            widths=[0.25, 0.25, 0.25, 0.25],
            kwargs=dict(
                ax1=dict(
                    xlim=[0, 10],
                    xlabel="Cone Resistance [MPa]",
                    ylabel="Elevation [m+CD]",
                    ),
                ax2=dict(xlim=[0, 1000], xlabel="Nett. Cone Resistance [kPa]"),
                ax3=dict(xlim=[0, 500], xlabel="In-situ Stress [kPa]"),
                ax4=dict(xlim=[0, 50], xlabel="SU [kPa]"),
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
                        xlabel="",
                        ),
                    )
                ),
            ),
        layout=dict(
            papersize="A4",
            margins=[1, 1, 1, 1],
            # logo=r'D:\Users\mbet\OneDrive - boskalis.com\9. PEng\a. Pulau Tekong\02. GIS\a. QGIS files\Logo\JV.png'
            ),
        info=dict(
            pointid=[p for p in pointids],
            row_spacing=np.linspace(0.6, 0.1, 5),
            general_titles=["CLIENT", "SO Rep", "PE-GEO", "CONTRACTOR", "PROJECT"],
            general_values=[
                "Housing & Development Board",
                "Surbana Jurong",
                "AECOM",
                "BPJV",
                "Pulau Tekong Polder Development",
                ],
            location_titles=["AREA", "PANEL", "EASTING", "NORTHING", "ELEVATION"],
            location_values=[
                point[x].iloc[0]
                for x in ["Area", "Box", "Easting", "Northing", "Elevation"]
                ],
            location_units=["", "", "", "", " m+CD"],
            version_titles=[
                "CPT DATE",
                "PRINT DATE",
                "PREPARED BY",
                "CHECKED BY",
                "APPROVED BY",
                ],
            version_values=[
                point["DateTime"].iloc[0].strftime("%d-%b-%Y"),
                datetime.now().strftime("%d-%b-%Y"),
                "MBET",
                "ANAM",
                "LBOL",
                ],
            ),
        )

    return plot_props


def standard_gint_bh_plot(engine, pointid):
    # make tuple of the pointids
    pointids = (pointid, )

    # get data from gINT database. make sure CTP_COMB and BH_COMB views are made
    point = pd.read_sql_query(point_data_single.format(**{"pointid": str(pointid)}), engine)
    bh = pd.read_sql_query(bh_data.format(**{"pointid": str(pointid)}), engine)
    spt = pd.read_sql_query(spt_data.format(**{"pointid": str(pointid)}), engine)
    vst = pd.read_sql_query(fvst_data.format(**{"pointid": str(pointid)}), engine)
    lab = (
        pd.read_sql_query(lab_data.format(**{"pointid": str(pointid)}), engine)
            .sort_values("Depth")
            .drop_duplicates()
    )

    # separate the columns for readability of the code
    elevation = bh.Elevation_Top

    lab_y = lab.Elevation
    lab_su_uu = lab.UU_Su
    lab_su_ciu = lab.CIU_Su

    bh_x = [0.5] * len(bh)
    bh_height = bh.Thickness
    bh_bottom = bh.Elevation_Top

    # set bh colors
    bh_color = []
    for gu in bh.Geology_Unit_1.values:
        bh_color.append(bh_colormap(gu))

    # get max and min depths and round up/down respectively
    ymin, ymax = math.floor(elevation.min())-1, math.ceil(elevation.max())

    # set the meter tick interval
    y_int = 2

    # makersize lab and vst
    s=50

    # make the json object
    plot_props = dict(
        plots=dict(
            y_data=elevation,
            plot_1=dict(
                ax="ax1",
                name="borehole",
                type="bar",
                x_data=[],
                args=[bh_x, bh_height],
                kwargs=dict(
                    width=0.5,
                    bottom=bh_bottom,
                    color=bh_color,
                    label="BH Log",
                    hatch="...",
                    edgecolor="black",
                    ),
                ),
            plot_2=dict(
                ax="ax2",
                name="Description",
                type="hlines",
                x_data=[],
                args=[elevation, 0, 1],
                kwargs=dict(color='black', lw=0.8),
                ),
            plot_3=dict(
                ax="ax3",
                name="borehole",
                type="plot",
                x_data=[],
                args=[spt.N_Value, spt.Elevation],
                kwargs=dict(color='black', marker='o', ms=10, mec='black', mfc='red', label='SPT-N Value'),
                ),
            plot_4=dict(
                ax="ax4",
                name="uu",
                type="scatter",
                x_data=[],
                args=[lab_su_uu, lab_y],
                kwargs=dict(marker='^', s=s, edgecolors='black', c='white', label='UU'),
                ),
            plot_5=dict(
                ax="ax4",
                name="ciu",
                type="scatter",
                x_data=[],
                args=[lab_su_ciu, lab_y],
                kwargs=dict(marker='v', s=s, edgecolors='black', c='white', label='CIU'),
                ),
            plot_6=dict(
                ax="ax4",
                name="vst",
                type="scatter",
                x_data=[],
                args=[vst.Vane_Peak_Uncorrected_Su, vst.Elevation],
                kwargs=dict(marker='<', s=s, edgecolors='black', c='white', label='F-VST'),
                )
            ),
        axes=dict(
            num=4,
            widths=[0.15, 0.30, 0.30, 0.25],
            kwargs=dict(
                ax1=dict(xlim=[0, 1], xticks=[0, 1], xticklabels=[], xlabel="BH Log", ylabel='Elevation [m+CD]'),
                ax2=dict(xlim=[0, 1], xticks=[0, 1], yticklabels=[], xticklabels=[], xlabel="Description"),
                ax3=dict(xlim=[0, 100], xlabel="SPT [-]"),
                ax4=dict(xlim=[0, 100], xlabel="Undrained Shear Stength [kPa]"),
                all=dict(
                    ylim=[ymin, ymax],
                    yticks=[x for x in range(ymin, ymax + y_int, y_int)],
                    ),
                ),
            custom_legend=dict(
                ax1=bh_legend()
                ),
            no_grid=['ax2']
            ),
        layout=dict(
            papersize="A4",
            margins=[1, 1, 1, 1],
            # logo=r'D:\Users\mbet\OneDrive - boskalis.com\9. PEng\a. Pulau Tekong\02. GIS\a. QGIS files\Logo\JV.png'
            ),
        info=dict(
            pointid=[p for p in pointids],
            row_spacing=np.linspace(0.6, 0.1, 5),
            general_titles=["CLIENT", "SO Rep", "PE-GEO", "CONTRACTOR", "PROJECT"],
            general_values=[
                "Housing & Development Board",
                "Surbana Jurong",
                "AECOM",
                "BPJV",
                "Pulau Tekong Polder Development",
                ],
            location_titles=["AREA", "PANEL", "EASTING", "NORTHING", "ELEVATION"],
            location_values=[
                point[x].iloc[0]
                for x in ["Area", "Box", "Easting", "Northing", "Elevation"]
                ],
            location_units=["", "", "", "", " m+CD"],
            version_titles=[
                "CPT DATE",
                "PRINT DATE",
                "PREPARED BY",
                "CHECKED BY",
                "APPROVED BY",
                ],
            version_values=[
                point["DateTime"].iloc[0].strftime("%d-%b-%Y"),
                datetime.now().strftime("%d-%b-%Y"),
                "MBET",
                "ANAM",
                "LBOL",
                ],
            ),
        )

    for index, row in bh.iterrows():
        plot_name = f'plot_text_{index}'
        text = '\n'.join(textwrap.wrap(row.Description, width=40))
        props = dict(
            ax='ax2',
            type='annotate',
            x_data=[],
            args=[text, (0.05, row.Elevation_Top)],
            kwargs=dict(va='top', ha='left', fontsize=7, wrap=True)
        )

        plot_props['plots'][plot_name] = props



    return plot_props