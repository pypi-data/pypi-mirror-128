SELECT
       PointID,
       (SELECT TOP 1
                     PointID
       FROM
            POINT b
       WHERE
             a.GEOM.STDistance(b.GEOM) < 5 AND
             b.type = 'RO'
       ORDER BY
                a.GEOM.STDistance(b.GEOM)
           ) AS BoreHole
FROM
     POINT a
WHERE
      Type = 'CPT'