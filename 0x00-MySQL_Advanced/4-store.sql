--
-- Middle finger on the trigger
--

DROP TRIGGER IF EXISTS after_order_placement;

CREATE TRIGGER after_order_placement
AFTER INSERT
ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
