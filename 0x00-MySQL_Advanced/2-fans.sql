--
-- Rank deez bands country of origin by no of fans.
--

SELECT origin, SUM(fans) AS nb_fans FROM metal_bands GROUP BY origin ORDER BY nb_fans DESC;
