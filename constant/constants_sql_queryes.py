REPORT = """
SELECT COUNT(DISTINCT order_id) FROM history
UNION
SELECT COUNT(DISTINCT order_id) FROM history
WHERE order_id IN (SELECT order_id FROM history WHERE status='new') AND
    order_id IN (SELECT order_id FROM history WHERE status='to_provide') AND
    (order_id IN (SELECT order_id FROM history WHERE status='fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='partial_fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='reject'))
UNION
SELECT COUNT(DISTINCT order_id)-(SELECT COUNT(DISTINCT order_id) FROM history
WHERE order_id IN (SELECT order_id FROM history WHERE status='new') AND
    order_id IN (SELECT order_id FROM history WHERE status='to_provide') AND
    (order_id IN (SELECT order_id FROM history WHERE status='fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='partial_fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='reject'))) FROM history
WHERE order_id IN (SELECT order_id FROM history WHERE status='to_provide') AND
        (order_id IN (SELECT order_id FROM history WHERE status='fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='partial_fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='reject')) OR
        (order_id IN (SELECT order_id FROM history WHERE status='fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='partial_fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='reject'))
UNION
SELECT COUNT(DISTINCT order_id)-(SELECT COUNT(DISTINCT order_id)-(SELECT COUNT(DISTINCT order_id) FROM history
WHERE order_id IN (SELECT order_id FROM history WHERE status='new') AND
    order_id IN (SELECT order_id FROM history WHERE status='to_provide') AND
    (order_id IN (SELECT order_id FROM history WHERE status='fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='partial_fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='reject'))) FROM history
WHERE order_id IN (SELECT order_id FROM history WHERE status='to_provide') AND
        (order_id IN (SELECT order_id FROM history WHERE status='fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='partial_fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='reject')) OR
        (order_id IN (SELECT order_id FROM history WHERE status='fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='partial_fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='reject'))) - (SELECT COUNT(DISTINCT order_id) FROM history
WHERE order_id IN (SELECT order_id FROM history WHERE status='new') AND
    order_id IN (SELECT order_id FROM history WHERE status='to_provide') AND
    (order_id IN (SELECT order_id FROM history WHERE status='fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='partial_fill') OR
        order_id IN (SELECT order_id FROM history WHERE status='reject')))  FROM history


"""