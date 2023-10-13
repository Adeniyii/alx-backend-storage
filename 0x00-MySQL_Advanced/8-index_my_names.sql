--
-- Create a prefix index on the name column of the names table.
--

CREATE INDEX idx_name_first
ON names(name(1));
