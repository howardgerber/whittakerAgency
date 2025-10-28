-- Initial database setup for development
-- This file is automatically run when the MariaDB container first starts

-- Grant privileges to the application user
GRANT SELECT, INSERT, UPDATE, DELETE ON whittaker.* TO 'whittaker_user'@'%';
FLUSH PRIVILEGES;

-- Note: Tables will be created by Alembic migrations
