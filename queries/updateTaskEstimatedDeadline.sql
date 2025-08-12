UPDATE OR ABORT tasks
SET estimatedDeadline = ?
WHERE uuid = ?
RETURNING uuid;