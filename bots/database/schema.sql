-- Project Apex SQLite schema (full)
-- Keep this file aligned with migrations/001_initial_schema.sql

CREATE TABLE IF NOT EXISTS migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    bot_name TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    marked_for_deletion_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_conversation_user_id
    ON conversation_history (user_id);
CREATE INDEX IF NOT EXISTS idx_conversation_created_at
    ON conversation_history (created_at);
CREATE INDEX IF NOT EXISTS idx_conversation_bot_name
    ON conversation_history (bot_name);

CREATE TABLE IF NOT EXISTS task_queues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bot_name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_task_queue_bot_name
    ON task_queues (bot_name);
CREATE INDEX IF NOT EXISTS idx_task_queue_status
    ON task_queues (status);
CREATE INDEX IF NOT EXISTS idx_task_queue_created_at
    ON task_queues (created_at);

CREATE TABLE IF NOT EXISTS bot_state (
    bot_name TEXT PRIMARY KEY,
    state_data TEXT NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_bot_state_updated_at
    ON bot_state (updated_at);

CREATE TABLE IF NOT EXISTS scheduled_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bot_name TEXT NOT NULL,
    action_type TEXT NOT NULL,
    schedule_time DATETIME NOT NULL,
    payload TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_scheduled_actions_bot_name
    ON scheduled_actions (bot_name);
CREATE INDEX IF NOT EXISTS idx_scheduled_actions_schedule_time
    ON scheduled_actions (schedule_time);
CREATE INDEX IF NOT EXISTS idx_scheduled_actions_status
    ON scheduled_actions (status);

CREATE TABLE IF NOT EXISTS failover_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    primary_model TEXT NOT NULL,
    fallback_model TEXT NOT NULL,
    reason TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_failover_events_created_at
    ON failover_events (created_at);
