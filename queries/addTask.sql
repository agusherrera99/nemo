INSERT OR ABORT INTO tasks
('uuid', 'title', 'description', 'pin', 'state')
VALUES
(?, ?, ?, ?, ?)
RETURNING uuid;
