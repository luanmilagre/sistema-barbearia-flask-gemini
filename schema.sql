DROP TABLE IF EXISTS agendamentos;

CREATE TABLE agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cliente TEXT NOT NULL,
    data_agendamento TEXT NOT NULL,
    hora_agendamento TEXT NOT NULL
);