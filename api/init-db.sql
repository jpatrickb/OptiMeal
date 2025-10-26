-- Initialize OptiMeal database
-- This script runs automatically when the PostgreSQL container starts

-- Ensure the database exists (already created by POSTGRES_DB env var)
-- Create any extensions we might need
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE optimeal_dev TO optimeal_user;

-- Additional setup can be added here as needed
