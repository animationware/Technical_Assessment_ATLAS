# Consulta para obtener las ventas totales por mes y categoría de producto:

SELECT
    DATE_FORMAT(v.fecha_venta, '%Y-%m') AS mes,
    p.categoria,
    SUM(v.cantidad) AS total_unidades_vendidas
FROM ventas v
JOIN productos p ON v.id_producto = p.id_producto
GROUP BY
    mes,
    p.categoria
ORDER BY
    mes,
    p.categoria;

# Select de obtención TOP 5 de clientes con mayores compras en el último año:

SELECT
    c.id_cliente,
    c.nombre,
    SUM(v.cantidad * p.precio) AS total_comprado,
    YEAR(v.fecha_venta) As 'año'
FROM ventas v
JOIN clientes c ON v.id_cliente = c.id_cliente
JOIN productos p ON v.id_producto = p.id_producto
WHERE v.fecha_venta >= (
    SELECT DATE_SUB(MAX(fecha_venta), INTERVAL 1 YEAR)
    FROM ventas
)
GROUP BY c.id_cliente, c.nombre, YEAR(v.fecha_venta) 
ORDER BY total_comprado DESC
LIMIT 5;

# Creación de vista: cliente, ciudad, total de compras, última fecha de compra.

CREATE OR REPLACE VIEW vw_summary_purchases_by_customer AS
SELECT
    c.id_cliente,
    c.nombre AS cliente,
    c.ciudad,
    SUM(v.cantidad * p.precio) AS total_compras,
    MAX(v.fecha_venta) AS ultima_fecha_compra
FROM clientes c
LEFT JOIN ventas v
    ON c.id_cliente = v.id_cliente
LEFT JOIN productos p
    ON v.id_producto = p.id_producto
GROUP BY
    c.id_cliente,
    c.nombre,
    c.ciudad;
-- Validar vista:
SELECT * FROM vw_summary_purchases_by_customer;
