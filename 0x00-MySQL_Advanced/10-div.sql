--
-- Simple stored function
--

DELIMITER $$

CREATE FUNCTION SafeDiv(
	a INT,
	b INT
)
RETURNS FLOAT
DETERMINISTIC
BEGIN
	DECLARE v FLOAT;
	IF b = 0 THEN
		SET v = 0;
	ELSE
		SET v = a/b;
	END IF;

	RETURN (v);
END$$

DELIMITER :
