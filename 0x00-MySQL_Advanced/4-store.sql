-- Create a trigger to decrease item quantity after a new order
CREATE TRIGGER after_insert_order
AFTER INSERT ON orders
FOR EACH ROW
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
