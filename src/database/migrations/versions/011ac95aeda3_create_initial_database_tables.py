# ruff: noqa
"""Create initial database tables

Revision ID: 011ac95aeda3
Revises: 
Create Date: 2023-04-23 18:25:58.439500

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "011ac95aeda3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "TickerSymbols",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "ticker_symbol",
            sa.Enum("EURUSD", "GBPUSD", "BTCUSD", name="tickersymbols"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "TimeFrames",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("time_frame", sa.Enum("hour", "day", name="timeframes"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "HistoricalData",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticker_symbol_id", sa.Integer(), nullable=False),
        sa.Column("time_frames_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["ticker_symbol_id"], ["TickerSymbols.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["time_frames_id"], ["TimeFrames.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("HistoricalData")
    op.drop_table("TimeFrames")
    op.drop_table("TickerSymbols")
