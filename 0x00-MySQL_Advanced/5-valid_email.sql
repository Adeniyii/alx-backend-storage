--
-- Email validation trigger.
--

CREATE TRIGGER validate_email_before
BEFORE UPDATE
ON users FOR EACH ROW
IF NEW.email NOT REGEXP '^[^@]+@[^@]+\.[^@]{2,}$' THEN
	UPDATE users SET valid_email = 0 WHERE id = NEW.id;
ELSE 
	UPDATE users SET valid_email = 1 WHERE id = NEW.id;
END IF;
