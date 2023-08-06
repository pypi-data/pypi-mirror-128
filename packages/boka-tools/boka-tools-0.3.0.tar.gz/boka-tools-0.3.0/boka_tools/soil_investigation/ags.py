import re

from munch import Munch
import pandas as pd


class AGS:
    """Class to parse AGS files.

    Parameters
    ----------
    path : str
        path to AGS file
    ags_version : int
        specify AGS version. Either 3 or 4. Defaults to 3, as 4 still needs to be implemented.

    Attributes
    ----------
    ags_version : int
        version number of the AGS file
    ags_raw : list
        list of strings containing the raw AGS ASCII data
    ags : dict
        dictionary containing all tables and data
    df : Munch dict
        dictionary of dataframe. Each AGS table is represented in a dataframe containing all the data
    """

    def __init__(self, path, ags_version=3):

        self.ags_version = ags_version

        with open(path, 'r') as f:
            self.ags_raw = f.readlines()

        self.ags = dict()
        self.df = Munch()

        if self.ags_version == 3:
            self._parse_ags_3()
            self._make_df()
        elif self.ags_version == 4:
            self._parse_ags_4()
            self._make_df()
        else:
            raise AttributeError('This AGS version is unknown. Please only use AGS 3 or AGS 4.')

    def _parse_ags_3(self):
        """
        private method to parse AGS3 data

        """
        for i, line in enumerate(self.ags_raw):
            if '**' in line:
                group = re.search(r'[A-Z]{4}', line).group(0)
                group_line = i
                if '?' in line:
                    user_def = True
                else:
                    user_def = False

                self.ags[group] = dict()

            elif '*' in line:
                headers = re.findall(r'[A-Z]{4}_[A-Z,0-9]{2,4}\d?', line)
                for header in headers:
                    self.ags[group][header] = []

                start_block = i + 1

            elif '<UNITS>' in line:
                pass

            else:
                split_line = line.split('","')
                len_block = len(split_line)
                len_header = len(self.ags[group].keys())
                headers = list(self.ags[group].keys())

                if len_block == len_header:
                    if '"<CONT>' == split_line[0]:
                        for header, col in zip(headers[1:], split_line[1:]):
                            self.ags[group][header][-1] = self.ags[group][header][-1] + (
                                col.replace('\n', '').replace('"', ''))
                    else:
                        for header, col in zip(headers, split_line):
                            self.ags[group][header].append(col.replace('\n', '').replace('"', ''))

    def _parse_ags_4(self):
        """
        private method to parse AGS4 data
        """
        for i, line in enumerate(self.ags_raw):
            if 'GROUP' in line:
                group = re.search(r'"[A-Z]{4}"', line).group(0).replace('"','')
                group_line = i

                self.ags[group] = dict()

            elif 'HEADING' in line:
                headers = re.findall(r'[A-Z]{4}_[A-Z,0-9]{2,4}\d?', line)
                for header in headers:
                    self.ags[group][header] = []

                start_block = i + 1

            elif 'UNIT' in line:
                # TODO add parser for unit and convert columns to other unit if required
                pass

            elif 'DATA' in line:
                split_line = line.split('","')[1:]
                len_block = len(split_line)
                len_header = len(self.ags[group].keys())
                headers = list(self.ags[group].keys())

                for header, col in zip(headers, split_line):
                    self.ags[group][header].append(col.replace('\n', '').replace('"', ''))

            else:
                pass

    def _make_df(self, to_numeric=True):
        """Private method to make DataFrames from the AGS dict data

        Parameters
        ----------
        to_numeric : bool
            True if values should be converted to numeric values. Default is true
        """
        for key in self.ags.keys():
            self.df[key] = pd.DataFrame(self.ags[key])

            if to_numeric:
                self.df[key] = self.df[key].apply(pd.to_numeric, errors='ignore')

    def _gint_mapper(self, mapper):
        """function to rename ags columns in the DataFrames

        Parameters
        ----------
        mapper : dict
            mapper on how the rename the extracted DataFrames. Used for uploading to databases.

        Returns
        -------
        renamed dataframe
        """
        renamed_df = Munch()

        for group in mapper.group.unique():
            try:
                temp = mapper[mapper.group == group][['ags_name', 'gint_name']]
                headers = temp.ags_name.to_list()
                d = {x[0]: x[1] for x in temp.values}

                temp_df = self.df[group][headers].rename(columns=d)

                for col in temp_df.columns:
                    if 'date' in col.lower():
                        temp_df[col] = pd.to_datetime(temp_df[col], format=r'%d/%m/%Y', errors='coerce')

                renamed_df[group] = temp_df
            except KeyError:
                renamed_df[group] = pd.DataFrame()

        return renamed_df

    @staticmethod
    def upload_to_gint(engine, df_dict, sequence, gint_proj_id=3):
        # TODO Make uploader to gint using merge statement and a reflected gINT database
        pass