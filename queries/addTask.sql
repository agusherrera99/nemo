INSERT OR ABORT INTO tasks
('uuid', 'title', 'description', 'state')
VALUES
(?, ?, ?, ?)
RETURNING rowid;
