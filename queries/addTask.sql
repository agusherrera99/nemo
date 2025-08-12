INSERT OR ABORT INTO tasks
('uuid', 'title', 'description', 'estimatedDeadline', 'pin', 'state')
VALUES
(?, ?, ?, ?, ?, ?)
RETURNING uuid;
