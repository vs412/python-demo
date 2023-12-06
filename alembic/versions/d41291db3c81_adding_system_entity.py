"""adding system entity

Revision ID: d41291db3c81
Revises: cee1565497f2
Create Date: 2023-12-06 14:57:33.113463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d41291db3c81"
down_revision: Union[str, None] = "cee1565497f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "systems",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("supreme", sa.Text(), nullable=False),
        sa.Column("supreme_commander_name", sa.Text(), nullable=False),
        sa.Column("date_created", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("systems_pkey")),
        schema="interview",
    )
    op.add_column(
        "planets", sa.Column("system_id", sa.UUID(), nullable=False), schema="interview"
    )
    op.create_foreign_key(
        op.f("planets_system_id_fkey"),
        "planets",
        "systems",
        ["system_id"],
        ["id"],
        source_schema="interview",
        referent_schema="interview",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("planets_system_id_fkey"),
        "planets",
        schema="interview",
        type_="foreignkey",
    )
    op.drop_column("planets", "system_id", schema="interview")
    op.drop_table("systems", schema="interview")
    # ### end Alembic commands ###