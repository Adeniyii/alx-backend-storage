--
-- stored procedure `ComputeAverageScoreForUser` that computes and store the average score for a student.
--

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
	IN id INT
)
BEGIN
	DECLARE avg_score FLOAT;

	SELECT AVG(score)
	INTO avg_score
	FROM corrections
	WHERE user_id = id;

	UPDATE users as u
	SET average_score = avg_score
	WHERE u.id = id;
END$$

DELIMITER ;
