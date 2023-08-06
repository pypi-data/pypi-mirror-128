"""
Methods to make sql engines and query spatial data from MS SQL Server and return it into a pandas DataFrame.
"""
import platform

import pandas as pd
import urllib.parse
import sqlalchemy as sa

try:
    import geopandas as gpd
    from shapely.wkt import loads
except ImportError:
    pass


def server_connect(
        server: str, database: str, trusted_connection: bool = False, user: str = "api", password: str = "api",
) -> object:
    """
    creates and server engine that can be used to query data from SQL server using Pandas

    Parameters
    -----------
    server : str
        Server location
    database : str
        Database name
    trusted_connection : bool
        Designates if the connection is Trusted or not,
        When set to False and correct username and password must be entered, Boolean
    user : str
        Optional, username used to access the server if TrustedConnection is False
    password : str
        Optional, password to entered username to access the server

    Returns
    -------
    object
        Returns a SQLAlchemy engine
    """
    if platform.system().lower() == 'windows':
        driver = 'SQL Server'
    else:
        driver = 'ODBC Driver 17 for SQL Server'

    # connection string for database
    if trusted_connection:
        params = urllib.parse.quote_plus(
            "Driver={"+driver+"};Server="
            + server
            + ";Database="
            + database
            + ";Trusted_Connection=yes"
        )
    else:
        params = urllib.parse.quote_plus(
            "Driver={"+driver+"};Server="
            + server
            + ";Database="
            + database
            + ";UID="
            + user
            + ";PWD="
            + password
        )

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    return engine


def mssql_geom(sql: str, engine: object, epsg: int, to_latlon: bool=False) -> object:
    """
    Pass Microsoft SQL statement and return a Geopandas dataframe
    Geometry columns should be named "geometry" in sql statement.

    Parameters
    ----------
    sql : str
        T-SQL statement with a Spatial geometry column passed as 'geometry'
        in Well Known Text (wkt) via the T-SQL function > [GEOM].STAsText()
    engine : object
        SQL Alchemy engine should be passed into function. Assuming engine
        is already made under the variable 'engine' it is passed by default
    epsg : int
        the epsg code of the geometery you are importing
    to_latlon : bool
        whether or not to convert the geometry to lat lon coordinates in epsg:4326

    Returns
    -------
    object
        Returns a GeoPandas DataFrame

    Raises
    ------
    ValueError
        is STAsText T-SQL Syntac is not detected in sql string

    """

    if 'STAsText' not in sql:
        raise ValueError('GEOM column not passed as WKT by means of [GEOM].STAsText()')

    df = pd.read_sql_query(sql, engine)
    df['geometry'] = df['geometry'].apply(loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs={'init': f'epsg:{epsg}'})

    if to_latlon:
        gdf = gdf.to_crs({'init': 'epsg:4326'})

    return gdf
