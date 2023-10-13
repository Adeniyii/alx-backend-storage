--
-- Create procedure which inserts a new correction.
--

DROP PROCEDURE IF EXISTS AddBonus;

DELIMITER $$

CREATE PROCEDURE AddBonus (
	IN user_id INT,
	IN project_name VARCHAR(255),
	IN score INT
)
BEGIN
	DECLARE productID INT;

	SELECT id
	INTO productID
	FROM projects
	WHERE name = project_name;

	IF productID IS NULL THEN
		INSERT INTO projects (name)
		VALUES (project_name);
		SET productID = LAST_INSERT_ID();
	END IF;

	INSERT INTO corrections (user_id, project_id, score)
	VALUES (user_id, productID, score);
END$$

DELIMITER ;

