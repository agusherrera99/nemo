UPDATE OR ABORT tasks
SET pin = ?
WHERE uuid = ?
RETURNING uuid;