DELETE FROM tasks
WHERE uuid = ?
RETURNING uuid;