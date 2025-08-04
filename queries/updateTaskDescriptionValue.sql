UPDATE OR ABORT tasks
SET description = ?
WHERE uuid = ?
RETURNING uuid;