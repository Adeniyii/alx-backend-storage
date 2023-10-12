--
-- Rank `glam rock` bands by longevity.
--

SELECT band_name, (IFNULL(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE IFNULL(FIND_IN_SET('Glam rock', style), 0) > 0
ORDER BY lifespan DESC;
