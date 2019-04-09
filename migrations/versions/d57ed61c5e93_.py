"""empty message

Revision ID: d57ed61c5e93
Revises: 
Create Date: 2019-04-04 19:14:38.330213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd57ed61c5e93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cart_info', sa.String(), nullable=False),
    sa.Column('date_created', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cc_number', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('zip_code', sa.Integer(), nullable=False),
    sa.Column('exp_date', sa.String(), nullable=False),
    sa.Column('cvv_code', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('source_url', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('number_of_blogs', sa.Integer(), nullable=True),
    sa.Column('blog_word_total', sa.Integer(), nullable=True),
    sa.Column('schedule', sa.String(), nullable=True),
    sa.Column('product_number', sa.String(), nullable=True),
    sa.Column('e_blast_software_name', sa.String(), nullable=True),
    sa.Column('e_blast_software_url', sa.String(), nullable=True),
    sa.Column('e_blast_software_user', sa.String(), nullable=True),
    sa.Column('e_blast_user_password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('business_name', sa.String(), nullable=True),
    sa.Column('business_username', sa.String(), nullable=True),
    sa.Column('business_password', sa.String(), nullable=True),
    sa.Column('website_url', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('google_profile_url', sa.String(), nullable=True),
    sa.Column('facebook_profile_url', sa.String(), nullable=True),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cart',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart')
    op.drop_table('user')
    op.drop_table('product')
    op.drop_table('payment')
    op.drop_table('history')
    # ### end Alembic commands ###
