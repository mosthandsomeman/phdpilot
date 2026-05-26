"""crawler module tables and position extensions

Revision ID: 002
Revises: 001
Create Date: 2026-05-26

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op when status is VARCHAR; safe if native enum exists from older DBs
    op.execute(
        """
        DO $$ BEGIN
            ALTER TYPE positionstatus ADD VALUE IF NOT EXISTS 'possibly_closed';
        EXCEPTION
            WHEN undefined_object THEN NULL;
        END $$;
        """
    )

    op.add_column("phd_positions", sa.Column("application_url", sa.String(length=1000), nullable=True))
    op.add_column(
        "phd_positions",
        sa.Column("first_seen_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
    )
    op.create_index(
        "ix_phd_positions_source_url_unique",
        "phd_positions",
        ["source_url"],
        unique=True,
        postgresql_where=sa.text("source_url IS NOT NULL"),
    )
    op.create_index(op.f("ix_phd_positions_source_name"), "phd_positions", ["source_name"], unique=False)

    op.create_table(
        "crawler_runs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source_name", sa.String(length=100), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="running"),
        sa.Column("total_fetched", sa.Integer(), server_default="0", nullable=False),
        sa.Column("total_created", sa.Integer(), server_default="0", nullable=False),
        sa.Column("total_updated", sa.Integer(), server_default="0", nullable=False),
        sa.Column("total_skipped", sa.Integer(), server_default="0", nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crawler_runs_source_name"), "crawler_runs", ["source_name"], unique=False)

    op.create_table(
        "crawler_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("source_name", sa.String(length=100), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], ["crawler_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_crawler_items_run_id"), "crawler_items", ["run_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_crawler_items_run_id"), table_name="crawler_items")
    op.drop_table("crawler_items")
    op.drop_index(op.f("ix_crawler_runs_source_name"), table_name="crawler_runs")
    op.drop_table("crawler_runs")
    op.drop_index(op.f("ix_phd_positions_source_name"), table_name="phd_positions")
    op.drop_index("ix_phd_positions_source_url_unique", table_name="phd_positions")
    op.drop_column("phd_positions", "first_seen_at")
    op.drop_column("phd_positions", "application_url")
