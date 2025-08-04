UPDATE OR ABORT tasks
SET state = ?
WHERE uuid = ?
RETURNING uuid;