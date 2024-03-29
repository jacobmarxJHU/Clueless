"""empty message

Revision ID: acda46412898
Revises: e880aece3143
Create Date: 2023-11-09 11:22:22.280509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acda46412898'
down_revision = 'e880aece3143'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('weaponId', sa.Integer(), nullable=True),
    sa.Column('roomId', sa.Integer(), nullable=True),
    sa.Column('characterId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['characterId'], ['cs.Characters.id'], ),
    sa.ForeignKeyConstraint(['roomId'], ['cs.Rooms.id'], ),
    sa.ForeignKeyConstraint(['weaponId'], ['cs.Weapons.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='cs'
    )
    with op.batch_alter_table('ActiveGames', schema=None) as batch_op:
        batch_op.drop_constraint('ActiveGames_gameStatus_fkey', type_='foreignkey')
        batch_op.drop_constraint('ActiveGames_currentPlayer_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'ActivePlayers', ['currentPlayer'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'GameStatus', ['gameStatus'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Guesses', schema=None) as batch_op:
        batch_op.drop_constraint('Guesses_playerId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Guesses_roomId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Guesses_gameId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Guesses_characterId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Guesses_weaponId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Rooms', ['roomId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'ActiveGames', ['gameId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Weapons', ['weaponId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'ActivePlayers', ['playerId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Characters', ['characterId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Paths', schema=None) as batch_op:
        batch_op.drop_constraint('Paths_locationId2_fkey', type_='foreignkey')
        batch_op.drop_constraint('Paths_locationId1_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Locations', ['locationId2'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Locations', ['locationId1'], ['id'], referent_schema='cs')

    with op.batch_alter_table('PlayerLocations', schema=None) as batch_op:
        batch_op.drop_constraint('PlayerLocations_gameId_fkey', type_='foreignkey')
        batch_op.drop_constraint('PlayerLocations_playerId_fkey', type_='foreignkey')
        batch_op.drop_constraint('PlayerLocations_characterId_fkey', type_='foreignkey')
        batch_op.drop_constraint('PlayerLocations_locationId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'ActivePlayers', ['playerId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Characters', ['characterId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Locations', ['locationId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'ActiveGames', ['gameId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('PlayerOrder', schema=None) as batch_op:
        batch_op.drop_constraint('PlayerOrder_gameId_fkey', type_='foreignkey')
        batch_op.drop_constraint('PlayerOrder_playerId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'ActiveGames', ['gameId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'ActivePlayers', ['playerId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Solutions', schema=None) as batch_op:
        batch_op.drop_constraint('Solutions_characterId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Solutions_gameId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Solutions_weaponId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Solutions_roomId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Characters', ['characterId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Rooms', ['roomId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'ActiveGames', ['gameId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Weapons', ['weaponId'], ['id'], referent_schema='cs')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Solutions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Solutions_roomId_fkey', 'Rooms', ['roomId'], ['id'])
        batch_op.create_foreign_key('Solutions_weaponId_fkey', 'Weapons', ['weaponId'], ['id'])
        batch_op.create_foreign_key('Solutions_gameId_fkey', 'ActiveGames', ['gameId'], ['id'])
        batch_op.create_foreign_key('Solutions_characterId_fkey', 'Characters', ['characterId'], ['id'])

    with op.batch_alter_table('PlayerOrder', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('PlayerOrder_playerId_fkey', 'ActivePlayers', ['playerId'], ['id'])
        batch_op.create_foreign_key('PlayerOrder_gameId_fkey', 'ActiveGames', ['gameId'], ['id'])

    with op.batch_alter_table('PlayerLocations', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('PlayerLocations_locationId_fkey', 'Locations', ['locationId'], ['id'])
        batch_op.create_foreign_key('PlayerLocations_characterId_fkey', 'Characters', ['characterId'], ['id'])
        batch_op.create_foreign_key('PlayerLocations_playerId_fkey', 'ActivePlayers', ['playerId'], ['id'])
        batch_op.create_foreign_key('PlayerLocations_gameId_fkey', 'ActiveGames', ['gameId'], ['id'])

    with op.batch_alter_table('Paths', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Paths_locationId1_fkey', 'Locations', ['locationId1'], ['id'])
        batch_op.create_foreign_key('Paths_locationId2_fkey', 'Locations', ['locationId2'], ['id'])

    with op.batch_alter_table('Guesses', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Guesses_weaponId_fkey', 'Weapons', ['weaponId'], ['id'])
        batch_op.create_foreign_key('Guesses_characterId_fkey', 'Characters', ['characterId'], ['id'])
        batch_op.create_foreign_key('Guesses_gameId_fkey', 'ActiveGames', ['gameId'], ['id'])
        batch_op.create_foreign_key('Guesses_roomId_fkey', 'Rooms', ['roomId'], ['id'])
        batch_op.create_foreign_key('Guesses_playerId_fkey', 'ActivePlayers', ['playerId'], ['id'])

    with op.batch_alter_table('ActiveGames', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('ActiveGames_currentPlayer_fkey', 'ActivePlayers', ['currentPlayer'], ['id'])
        batch_op.create_foreign_key('ActiveGames_gameStatus_fkey', 'GameStatus', ['gameStatus'], ['id'])

    op.drop_table('Card', schema='cs')
    # ### end Alembic commands ###
