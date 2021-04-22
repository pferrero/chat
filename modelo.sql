-- Enable foreign keys
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY,
    username   TEXT UNIQUE NOT NULL,
    pass       TEXT
);

CREATE TABLE IF NOT EXISTS mensaje (
    id_mensaje INTEGER PRIMARY KEY,
    from_user  INTEGER NOT NULL,
    to_user    INTEGER NOT NULL,
    msj        TEXT,
    fecha_hora DATETIME,
    FOREIGN KEY (from_user) REFERENCES usuario(id_usuario),
    FOREIGN KEY (to_user)   REFERENCES usuario(id_usuario)
);

