import pandas as pd
import numpy as np
from munch import Munch
import datetime


class P6:
    """
    Class that parses Primavera P6 xer files

    Parameters
    ----------
    path : str
        path to .xer file

    Attributes
    ----------
    path : str
        string of file path
    xer_dict : dict
        Dictionary containing all xer tables and data
    xer_df : dict
        Dictionary of Pandas DataFrames. Keys are as per xer table names.

    Returns
    -------
    object
        P6 object
    """
    def __init__(self, path: str):
        self.path = path
        self.xer_dict = Munch()
        self.xer_df = Munch()

        self._parse_xer()

    def _parse_xer(self):

        with open(self.path, "r") as f:
            xer = f.readlines()

        for line in xer:

            split_line = line.replace("\n", "").split("\t")

            if "%T" in split_line:
                table_name = split_line[-1]
                self.xer_dict[table_name] = Munch()

            elif "%F" in split_line:
                headers = split_line

                for header in headers[1:]:
                    self.xer_dict[table_name][header] = []

            elif "%R" in split_line:
                row = split_line[1:]

                for header, col in zip(headers[1:], row):
                    # inset regex https://stackoverflow.com/questions/12595051/check-if-string-matches-pattern
                    if len(col) > 0:
                        if "date" in header and len(col) > 10:
                            value = datetime.datetime.strptime(col, "%Y-%m-%d %H:%M")
                        else:
                            value = col
                    else:
                        value = np.nan

                    self.xer_dict[table_name][header].append(value)

        for key in self.xer_dict.keys():
            self.xer_df[key.lower()] = pd.DataFrame(self.xer_dict[key])

    def filter_df(self, regex: str = r"([A-E]{1,2}\d[A-D]?)"):
        """
        Filter Task Table by running regex search on the task_name column

        Parameters
        ----------
        regex : str
            a string in regex format. Default value looks for area names at Pulau Tekong Project

        Returns
        -------
        filtered Task DataFrame
        """
        df = self.xer_df.task

        df_filtered = df[
            [
                "task_code",
                "task_name",
                "target_start_date",
                "target_end_date",
                "act_start_date",
                "act_end_date",
            ]
        ]

        df_filtered["start"] = df_filtered["target_start_date"].dt.date
        df_filtered["end"] = df_filtered["target_end_date"].dt.date
        df_filtered["duration"] = np.nan

        if isinstance(regex, str):
            df_filtered["areas"] = df_filtered.task_name.str.findall(regex)

        for index, row in df_filtered.iterrows():
            if isinstance(row["start"], type(pd.NaT)):
                df_filtered.loc[index, "start"] = row["act_start_date"].date()

            if isinstance(row["end"], type(pd.NaT)):
                df_filtered.loc[index, "end"] = row["act_end_date"].date()

        df_filtered["duration"] = (df_filtered["end"] - df_filtered["start"]).dt.days

        return df_filtered

    def to_excel(self, path: str, how: str or list = "all"):
        """
        Method to export xer file to an Excel file

        Parameters
        ----------
        path : str
            String containing file name and/or location.
        how : list of str
            String for list of strings containing the table names to export to Excel. Defaults to 'all'.
            If you want a single sheet to be exported this has to be captured in a list.

        Returns
        -------
        An Excel file with the XER tables per separated per sheet
        """
        if not path.lower().endswith((".xlsx", ".xls")):
            path = path + ".xlsx"

        if how == "all":
            with pd.ExcelWriter(path) as writer:
                for key in self.xer_df:
                    self.xer_df[key].to_excel(writer, sheet_name=key, index=False)

        else:
            with pd.ExcelWriter(path) as writer:
                for key in how:
                    self.xer_df[key].to_excel(writer, sheet_name=key, index=False)

    def __repr__(self):
        return str([key for key in self.xer_dict])
