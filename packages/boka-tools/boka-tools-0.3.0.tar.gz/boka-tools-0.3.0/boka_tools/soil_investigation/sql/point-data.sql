SELECT PointID, Easting, Northing, ElevationStart AS Elevation, DateTime, Area, Box
FROM POINT
WHERE PointID in {pointids}