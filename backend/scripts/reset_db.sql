-- Reset public schema (fixes half-applied migrations / duplicate enum types).
-- Usage:
--   docker compose exec -T postgres psql -U phdpilot -d phdpilot < backend/scripts/reset_db.sql

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO phdpilot;
GRANT ALL ON SCHEMA public TO public;
CREATE EXTENSION IF NOT EXISTS vector;
