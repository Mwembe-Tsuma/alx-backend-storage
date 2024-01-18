-- Create a trigger to decrease item quantity after a new order
DELIMITER //

CREATE TRIGGER after_insert_order
AFTER INSERT ON orders FOR EACH ROW
BEGIN
    DECLARE ordered_quantity INT;

    -- Get the quantity ordered in the new order
    SELECT number INTO ordered_quantity
    FROM orders
    WHERE item_name = NEW.item_name
    ORDER BY number DESC
    LIMIT 1;

    -- Decrease the item quantity in the items table
    UPDATE items
    SET quantity = quantity - ordered_quantity
    WHERE name = NEW.item_name;
END;
//
DELIMITER ;
