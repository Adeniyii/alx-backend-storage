--
-- Create procedure which inserts a new correction.
--

DROP PROCEDURE IF EXISTS AddBonus;

DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS AddBonus(user_id, project_name, score)
BEGIN
	DECLARE productID INT;

	SELECT id
	INTO productID
	FROM projects
	WHERE name = project_name;

	IF productID = NULL THEN
		INSERT INTO projects (name)
		VALUES (project_name);
		SET productID = LAST_INSERT_ID()
	END IF;

	INSERT INTO corrections (user_id, project_id, score)
	VALUES (user_id, productID, score);
END$$

DELIMITER ;

