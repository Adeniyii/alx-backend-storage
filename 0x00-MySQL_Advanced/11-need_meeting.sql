--
-- Create view which finds students with score > 80 AND no last meeting OR last meeting was over a month ago.
--

DROP VIEW IF EXISTS need_meeting;

CREATE VIEW need_meeting
AS
SELECT name FROM students
	WHERE score < 80
	AND (last_meeting IS NULL
	OR TIMESTAMPDIFF(DAY, last_meeting, CURDATE()) > 30);
