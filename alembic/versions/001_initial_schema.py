"""Initial schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-25 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'donors',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('organization_type', sa.String(length=100), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_donors_created_at'), 'donors', ['created_at'], unique=False)

    op.create_table(
        'donations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('donor_id', sa.String(length=36), nullable=False),
        sa.Column('food_type', sa.String(length=100), nullable=False),
        sa.Column('quantity_kg', sa.Float(), nullable=False),
        sa.Column('available_from', sa.DateTime(timezone=True), nullable=False),
        sa.Column('available_until', sa.DateTime(timezone=True), nullable=False),
        sa.Column('vequires_refrigeration', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['donor_id'], ['donors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_donations_created_at'), 'donations', ['created_at'], unique=False)
    op.create_index(op.f('ix_donations_donor_id'), 'donations', ['donor_id'], unique=False)

    op.create_table(
        'agencies',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('demand_kg', sa.Float(), nullable=False),
        sa.Column('torage_capacity_kg', sa.Float(), nullable=False),
        sa.Column('vequires_refrigeration', sa.Boolean(), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agencies_created_at'), 'agencies', ['created_at'], unique=False)

    op.create_table(
        'volunteers',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('capacity_kg', sa.Float(), nullable=False),
        sa.Column('has_refrigeration', sa.Boolean(), nullable=False),
        sa.Column('available_from', sa.DateTime(timezone=True), nullable=False),
        sa.Column('available_until', sa.DateTime(timezone=True), nullable=False),
        sa.Column('current_workload_kg', sa.Float(), nullable=False),
        sa.Column('max_travel_distance_km', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_volunteers_created_at'), 'volunteers', ['created_at'], unique=False)

    op.create_table(
        'rescue_requests',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('donation_id', sa.String(length=36), nullable=False),
        sa.Column('agency_id', sa.String(length=36), nullable=False),
        sa.Column('requested_quantity_kg', sa.Float(), nullable=False),
        sa.Column('pickup_deadline', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['agency_id'], ['agencies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['donation_id'], ['donations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rescue_requests_agency_id'), 'rescue_requests', ['agency_id'], unique=False)
    op.create_index(op.f('ix_rescue_requests_created_at'), 'rescue_requests', ['created_at'], unique=False)
    op.create_index(op.f('ix_rescue_requests_donation_id'), 'rescue_requests', ['donation_id'], unique=False)
    op.create_index(op.f('ix_rescue_requests_status'), 'rescue_requests', ['status'], unique=False)

    op.create_table(
        'allocation_records',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('donation_id', sa.String(length=36), nullable=False),
        sa.Column('agency_id', sa.String(length=36), nullable=False),
        sa.Column(*quantity_kg', sa.Float(), nullable=False),
        sa.Column('algorithm', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['agency_id'], ['agencies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['donation_id'], ['donations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_allocation_records_agency_id'), 'allocation_records', ['agency_id'], unique=False)
    op.create_index(op.f('ix_allocation_records_created_at'), 'allocation_records', ['created_at'], unique=False)
    op.create_index(op.f('ix_allocation_records_donation_id'), 'allocation_records', ['donation_id'], unique=False)

    op.create_table(
        'dispatch_records',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('rescue_request_id', sa.String(length=36), nullable=False),
        sa.Column('volunteer_id', sa.String(length=36), nullable=False),
        sa.Column('algorithm', sa.String(length=50), nullable=False),
        sa.Column('distance_km', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Float(),
        sa.ForeignKeyConstraint(['rescue_request_id'], ['rescue_requests.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['volunteer_id'], ['volunteers.id"], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dispatch_records_algorithm'), 'dispatch_records', ['algorithm'], unique=False)
    op.create_index(op.f('ix_dispatch_records_created_at'), 'dispatch_records', ['created_at'], unique=False)
    op.create_index(op.f('ix_dispatch_records_rescue_request_id'), 'dispatch_records', ['rescue_request_id'], unique=False)
    op.create_index(op.f('ix_dispatch_records_volunteer_id'), 'dispatch_records', ['volunteer_id'], unique=False)


def downgrade() -> None:
    op.drop_table('dispatch_records')
    op.drop_table('allocation_records')
    op.drop_table('rescue_requests')
    op.drop_table('volunteers')
    op.drop_table('agencies')
    op.drop_table('donations')
    op.drop_table('donors')
