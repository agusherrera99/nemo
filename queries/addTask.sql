INSERT OR ABORT INTO tasks
('uuid', 'title', 'description', 'estimatedTime', 'pin', 'state')
VALUES
(?, ?, ?, ?, ?, ?)
RETURNING uuid;
