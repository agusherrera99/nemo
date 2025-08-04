UPDATE OR ABORT tasks
SET title = ?
WHERE uuid = ?
RETURNING uuid;