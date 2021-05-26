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

-- Insert a couple of users
INSERT INTO usuario VALUES (1, "user1", "123");
INSERT INTO usuario VALUES (2, "user2", "123");
INSERT INTO usuario VALUES (3, "user3", "123");
INSERT INTO usuario VALUES (4, "user4", "123");

-- Insert messages to display
INSERT INTO mensaje VALUES (1, 1, 2, "Hi",                datetime('2021-02-15 10:14:00'));
INSERT INTO mensaje VALUES (2, 1, 2, "How are you?",      datetime('2021-02-15 10:14:01'));
INSERT INTO mensaje VALUES (3, 2, 1, "Hi",                datetime('2021-02-15 11:15:20'));
INSERT INTO mensaje VALUES (4, 2, 1, "I'm fine and you?", datetime('2021-02-15 11:15:21'));
INSERT INTO mensaje VALUES (5, 1, 2, "I'm great",         datetime('2021-02-15 11:15:30'));