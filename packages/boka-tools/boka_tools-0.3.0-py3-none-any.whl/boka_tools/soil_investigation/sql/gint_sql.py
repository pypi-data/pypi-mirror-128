cpt_data = """
SELECT
       *
FROM
     [PulauTekongGintDatgel].[dbo].vw_CPT_DATA_COMB
WHERE PointID = '{pointid}'
ORDER BY Depth
"""

bh_data = """
SELECT
       a.[PointID]
       ,a.[Depth]
       ,[Bottom]
       ,[Elevation] - a.[Depth] AS Elevation_Top
       ,[Elevation] - [Bottom] AS Elevation_Bottom
       ,a.[Depth] - [Bottom] AS Thickness
       ,[Graphic]
      ,[Description]
      ,[Geology_Unit_1]
      ,[Geology_Unit_2]
      ,[Geology_Unit_3]
FROM
     [PulauTekongGintDatgel].[dbo].[STRATA_MAIN] a,
     [PulauTekongGintDatgel].[dbo].[POINT] b
WHERE
      a.PointID = '{pointid}' AND
      b.PointID = '{pointid}' 
ORDER BY
         [Depth]
"""

lab_data = """
SELECT
       *
FROM
     PulauTekongGintDatgel.dbo.vw_BH_ALL
WHERE
      PointID = '{pointid}'
"""

point_data = """
SELECT PointID, Easting, Northing, ElevationStart AS Elevation, DateTime, Area, Box
FROM POINT
WHERE PointID IN {pointids}
"""

point_data_single = """
SELECT PointID, Easting, Northing, ElevationStart AS Elevation, DateTime, Area, Box
FROM POINT
WHERE PointID = '{pointid}'
"""

spt_data = """
SELECT * FROM PulauTekongGintDatgel.dbo.vw_SPT WHERE PointID = '{pointid}' ORDER BY Depth
"""

fvst_data = """
SELECT 
    a.PointID,
    Elevation - Depth AS Elevation,
    Vane_Peak_Uncorrected_Su,
    Vane_Remoulded_Uncorrected_Su
FROM 
    PulauTekongGintDatgel.dbo.IN_SITU_VANE a,
    PulauTekongGintDatgel.dbo.POINT b
WHERE 
    a.PointID = '{pointid}' AND
    b.PointID = '{pointid}'
"""