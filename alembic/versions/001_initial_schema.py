from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'donors',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('organization_type', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_table(
        'donations',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('donor_id', sa.String(), sa.ForeignKey('donors.id'), nullable=False),
        sa.Column('food_type', sa.String(), nullable=False),
        sa.Column('quantity_kg', sa.Float(), nullable=False),
        sa.Column('available_from', sa.DateTime(timezone=True), nullable=True),
        sa.Column('available_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('requires_refrigeration', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index('idx_donations_donor_id', 'donations', ['donor_id'])

    op.create_table(
        'agencies',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('demand_kg', sa.Float(), nullable=False),
        sa.Column('storage_capacity_kg', sa.Float(), nullable=False),
        sa.Column('requires_refrigeration', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'volunteers',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('capacity_kg', sa.Float(), nullable=False),
        sa.Column('has_refrigeration', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('available_from', sa.DateTime(timezone=True), nullable=True),
        sa.Column('available_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('current_workload_kg', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('max_travel_distance_km', sa.Float(), nullable=False, server_default='15.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'rescue_requests',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('donation_id', sa.String(), sa.ForeignKey('donations.id'), nullable=False),
        sa.Column('agency_id', sa.String(), sa.ForeignKey('agencies.id'), nullable=False),
        sa.Column('requested_quantity_kg', sa.Float(), nullable=False),
        sa.Column('pickup_deadline', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index('idx_rescue_requests_status', 'rescue_requests', ['status'])

    op.create_table(
        'allocation_records',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('donation_id', sa.String(), sa.ForeignKey('donations.id'), nullable=False),
        sa.Column('agency_id', sa.String(), sa.ForeignKey('agencies.id'), nullable=False),
        sa.Column('quantity_kg', sa.Float(), nullable=False),
        sa.Column('algorithm', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'dispatch_records',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('rescue_request_id', sa.String(), sa.ForeignKey('rescue_requests.id'), nullable=False),
        sa.Column('volunteer_id', sa.String(), sa.ForeignKey('volunteers.id'), nullable=False),
        sa.Column('algorithm', sa.String(), nullable=False),
        sa.Column('distance_km', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

def downgrade() -> None:
    for tbl in ['dispatch_records', 'allocation_records', 'rescue_requests', 'volunteers', 'agencies', 'donations', 'donors']:
        op.drop_table(tbl)
