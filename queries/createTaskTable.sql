CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT,
    title TEXT,
    description TEXT,
    state INTEGER
);
