--
-- Email validation trigger.
--

DROP TRIGGER IF EXISTS validate_email_before;

DELIMITER $$

CREATE TRIGGER validate_email_before
BEFORE UPDATE
ON users FOR EACH ROW
BEGIN
	IF NEW.email != OLD.email THEN
		SET NEW.valid_email = 0;
	END IF;
END $$

DELIMITER ;
