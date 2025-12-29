-- Seleccionamos la base de datos donde trabajaremos
USE rds_handle_business;
-- Creamos la tabla 'clientes' con sus columnas y tipos de datos
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- Creamos la tabla 'productos' con sus columnas y tipos de datos
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);
-- Creamos la tabla 'ventas' con sus columnas y relaciones
CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_producto INT NOT NULL,
    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    cantidad INT NOT NULL,
    CONSTRAINT fk_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    CONSTRAINT fk_producto
        FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Insert inicial de datos:
INSERT INTO clientes (nombre, ciudad, fecha_registro) VALUES
('Juan Pérez', 'Bogotá', '2023-01-15'),
('María López', 'Medellín', '2023-02-20'),
('Carlos Gómez', 'Cali', '2023-03-05'),
('Ana Torres', 'Bogotá', '2023-03-25'),
('Luis Ramírez', 'Barranquilla', '2023-04-10');
INSERT INTO productos (categoria, precio) VALUES
('Electrónica', 500.00),
('Electrónica', 1500.00),
('Hogar', 200.00),
('Hogar', 750.00),
('Ropa', 100.00);
INSERT INTO ventas (id_cliente, id_producto, fecha_venta, cantidad) VALUES
-- Juan Pérez
(1, 1, '2023-05-01', 2),  -- Electrónica
(1, 3, '2023-05-15', 1),  -- Hogar
-- María López
(2, 2, '2023-06-05', 1),  -- Electrónica
-- Carlos Gómez
(3, 3, '2023-06-20', 3),  -- Hogar
(3, 1, '2023-06-25', 1),  -- Electrónica
-- Ana Torres
(4, 5, '2023-07-10', 4),  -- Ropa
-- Luis Ramírez
(5, 2, '2023-07-15', 2),  -- Electrónica
(5, 1, '2023-07-20', 1);  -- Electrónica