"""empty message

Revision ID: 71654fcd2bf9
Revises: 
Create Date: 2021-08-21 09:09:51.771350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71654fcd2bf9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogger',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('full_name', sa.String(length=500), nullable=True),
    sa.Column('followers', sa.Integer(), nullable=True),
    sa.Column('count_likes', sa.Integer(), nullable=True),
    sa.Column('count_comments', sa.Integer(), nullable=True),
    sa.Column('count_posts', sa.Integer(), nullable=True),
    sa.Column('er', sa.Float(), nullable=True),
    sa.Column('profile_pic_url', sa.String(length=500), nullable=True),
    sa.Column('is_business_account', sa.Boolean(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('verify', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('hashtag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('invitation_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label')
    )
    op.create_table('media',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('src', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('src'),
    sa.UniqueConstraint('type')
    )
    op.create_table('place',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('route',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('key', sa.String(length=40), nullable=True),
    sa.Column('value', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key'),
    sa.UniqueConstraint('value')
    )
    op.create_table('status_trip',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('label', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label'),
    sa.UniqueConstraint('name')
    )
    op.create_table('type_media',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(length=40), nullable=True),
    sa.Column('pass_hash', sa.String(length=128), nullable=True),
    sa.Column('registered', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('blogger_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('count_likes', sa.Integer(), nullable=True),
    sa.Column('count_comments', sa.Integer(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('audience_coverage', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blogger_id'], ['blogger.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('route_place',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], ),
    sa.ForeignKeyConstraint(['route_id'], ['route.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trip',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.Column('invitation_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('min_count_folowers', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['invitation_id'], ['invitation_info.id'], ),
    sa.ForeignKeyConstraint(['route_id'], ['route.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('blogger_post',
    sa.Column('blogger_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['blogger_id'], ['blogger.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('blogger_id', 'post_id')
    )
    op.create_table('blogger_trip',
    sa.Column('blogger_id', sa.Integer(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['blogger_id'], ['blogger.id'], ),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.PrimaryKeyConstraint('blogger_id', 'trip_id')
    )
    op.create_table('hashtag_post',
    sa.Column('hashtag_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hashtag_id'], ['hashtag.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('hashtag_id', 'post_id')
    )
    op.create_table('hashtag_trip',
    sa.Column('hashtag_id', sa.Integer(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hashtag_id'], ['hashtag.id'], ),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.PrimaryKeyConstraint('hashtag_id', 'trip_id')
    )
    op.create_table('post_trip',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.PrimaryKeyConstraint('post_id', 'trip_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_trip')
    op.drop_table('hashtag_trip')
    op.drop_table('hashtag_post')
    op.drop_table('blogger_trip')
    op.drop_table('blogger_post')
    op.drop_table('trip')
    op.drop_table('route_place')
    op.drop_table('post')
    op.drop_table('user')
    op.drop_table('type_media')
    op.drop_table('status_trip')
    op.drop_table('settings')
    op.drop_table('route')
    op.drop_table('place')
    op.drop_table('media')
    op.drop_table('invitation_info')
    op.drop_table('hashtag')
    op.drop_table('blogger')
    # ### end Alembic commands ###
