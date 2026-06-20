-- Esquema relacional del Sistema de Gestión de Biblioteca.
-- Nota: usamos comillas SIMPLES para literales de texto. El enunciado usa
-- comillas dobles (DEFAULT "activo"), que en SQL estándar son IDENTIFICADORES,
-- no cadenas. SQLite lo tolera, pero lo correcto es comilla simple.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS autores (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre           VARCHAR(100) NOT NULL,
    nacionalidad     VARCHAR(50),
    fecha_nacimiento DATE
);

CREATE TABLE IF NOT EXISTS libros (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo           VARCHAR(200) NOT NULL,
    isbn             VARCHAR(13) UNIQUE NOT NULL,
    genero           VARCHAR(50),
    anio_publicacion INTEGER CHECK (anio_publicacion > 1000 AND anio_publicacion <= 2026),
    autor_id         INTEGER NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS usuarios (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre   VARCHAR(100) NOT NULL,
    email    VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS prestamos (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    libro_id         INTEGER NOT NULL,
    usuario_id       INTEGER NOT NULL,
    fecha_prestamo   DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_devolucion DATE,
    estado           VARCHAR(20) DEFAULT 'activo'
                     CHECK (estado IN ('activo', 'devuelto', 'vencido')),
    -- El enunciado NO declara ON DELETE para estas FKs. Lo hacemos explícito
    -- (RESTRICT) para que el comportamiento sea consciente y defendible.
    FOREIGN KEY (libro_id)   REFERENCES libros(id)   ON DELETE RESTRICT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT
);
