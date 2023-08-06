SELECT
       a.[PointID]
	  ,[Depth]
      ,[Bottom]
	  ,[Elevation] - [Depth] AS Elevation_Top
	  ,[Elevation] - [Bottom] AS Elevation_Bottom
	  ,[Depth] - [Bottom] AS Thickness
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