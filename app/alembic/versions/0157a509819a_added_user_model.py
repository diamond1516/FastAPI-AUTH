"""added user model

Revision ID: 0157a509819a
Revises: 17f3fb26e003
Create Date: 2024-06-24 09:37:21.793187

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0157a509819a"
down_revision: Union[str, None] = "17f3fb26e003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

status_enum = sa.Enum("ACTIVE", "INACTIVE", name="userstatus")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    status_enum.create(op.get_bind(), checkfirst=False)
    op.add_column(
        "users",
        sa.Column(
            "status",
            status_enum,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "status")
    status_enum.drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###
