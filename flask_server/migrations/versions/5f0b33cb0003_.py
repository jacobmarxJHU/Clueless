"""empty message

Revision ID: 5f0b33cb0003
Revises: 42b93b0ea0a5
Create Date: 2023-12-11 18:48:22.422559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f0b33cb0003'
down_revision = '42b93b0ea0a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Cards', schema=None) as batch_op:
        batch_op.drop_constraint('Cards_weaponId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Cards_locationId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Cards_characterId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Characters', ['characterId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Weapons', ['weaponId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Locations', ['locationId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Games', schema=None) as batch_op:
        batch_op.drop_constraint('Games_gameStatus_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'GameStatus', ['gameStatus'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Guesses', schema=None) as batch_op:
        batch_op.drop_constraint('Guesses_locationId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Guesses_gameId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Guesses_playerId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Guesses_characterId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Guesses_weaponId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Weapons', ['weaponId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Characters', ['characterId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Users', ['playerId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Locations', ['locationId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Games', ['gameId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Hands', schema=None) as batch_op:
        batch_op.drop_constraint('Hands_playerInfo_fkey', type_='foreignkey')
        batch_op.drop_constraint('Hands_gameId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Hands_cardId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Games', ['gameId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Cards', ['cardId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'PlayerInfos', ['playerInfo'], ['id'], referent_schema='cs')

    with op.batch_alter_table('MapSpots', schema=None) as batch_op:
        batch_op.drop_constraint('MapSpots_locationId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Locations', ['locationId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Paths', schema=None) as batch_op:
        batch_op.drop_constraint('Paths_locationId2_fkey', type_='foreignkey')
        batch_op.drop_constraint('Paths_locationId1_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Locations', ['locationId2'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Locations', ['locationId1'], ['id'], referent_schema='cs')

    with op.batch_alter_table('PlayerInfos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mapSpotId', sa.Integer(), nullable=True))
        batch_op.drop_constraint('PlayerInfos_characterId_fkey', type_='foreignkey')
        batch_op.drop_constraint('PlayerInfos_locationId_fkey', type_='foreignkey')
        batch_op.drop_constraint('PlayerInfos_playerId_fkey', type_='foreignkey')
        batch_op.drop_constraint('PlayerInfos_gameId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Locations', ['locationId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Games', ['gameId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Users', ['playerId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'MapSpots', ['mapSpotId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Characters', ['characterId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('PlayerOrder', schema=None) as batch_op:
        batch_op.drop_constraint('PlayerOrder_playerId_fkey', type_='foreignkey')
        batch_op.drop_constraint('PlayerOrder_gameId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Users', ['playerId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Games', ['gameId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Solutions', schema=None) as batch_op:
        batch_op.drop_constraint('Solutions_locationCard_fkey', type_='foreignkey')
        batch_op.drop_constraint('Solutions_characterCard_fkey', type_='foreignkey')
        batch_op.drop_constraint('Solutions_gameId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Solutions_weaponCard_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Cards', ['characterCard'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Games', ['gameId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Cards', ['locationCard'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Cards', ['weaponCard'], ['id'], referent_schema='cs')

    with op.batch_alter_table('StartLocations', schema=None) as batch_op:
        batch_op.drop_constraint('StartLocations_characterId_fkey', type_='foreignkey')
        batch_op.drop_constraint('StartLocations_locationId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Locations', ['locationId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Characters', ['characterId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.drop_constraint('Users_activeGame_fkey', type_='foreignkey')
        batch_op.drop_constraint('Users_playerStatus_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Games', ['activeGame'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'PlayerStatus', ['playerStatus'], ['id'], referent_schema='cs')

    with op.batch_alter_table('WeaponLocations', schema=None) as batch_op:
        batch_op.drop_constraint('WeaponLocations_locationId_fkey', type_='foreignkey')
        batch_op.drop_constraint('WeaponLocations_weapondId_fkey', type_='foreignkey')
        batch_op.drop_constraint('WeaponLocations_gameId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Locations', ['locationId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Games', ['gameId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Weapons', ['weapondId'], ['id'], referent_schema='cs')

    with op.batch_alter_table('Winners', schema=None) as batch_op:
        batch_op.drop_constraint('Winners_gameId_fkey', type_='foreignkey')
        batch_op.drop_constraint('Winners_playerId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Users', ['playerId'], ['id'], referent_schema='cs')
        batch_op.create_foreign_key(None, 'Games', ['gameId'], ['id'], referent_schema='cs')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Winners', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Winners_playerId_fkey', 'Users', ['playerId'], ['id'])
        batch_op.create_foreign_key('Winners_gameId_fkey', 'Games', ['gameId'], ['id'])

    with op.batch_alter_table('WeaponLocations', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('WeaponLocations_gameId_fkey', 'Games', ['gameId'], ['id'])
        batch_op.create_foreign_key('WeaponLocations_weapondId_fkey', 'Weapons', ['weapondId'], ['id'])
        batch_op.create_foreign_key('WeaponLocations_locationId_fkey', 'Locations', ['locationId'], ['id'])

    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Users_playerStatus_fkey', 'PlayerStatus', ['playerStatus'], ['id'])
        batch_op.create_foreign_key('Users_activeGame_fkey', 'Games', ['activeGame'], ['id'])

    with op.batch_alter_table('StartLocations', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('StartLocations_locationId_fkey', 'Locations', ['locationId'], ['id'])
        batch_op.create_foreign_key('StartLocations_characterId_fkey', 'Characters', ['characterId'], ['id'])

    with op.batch_alter_table('Solutions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Solutions_weaponCard_fkey', 'Cards', ['weaponCard'], ['id'])
        batch_op.create_foreign_key('Solutions_gameId_fkey', 'Games', ['gameId'], ['id'])
        batch_op.create_foreign_key('Solutions_characterCard_fkey', 'Cards', ['characterCard'], ['id'])
        batch_op.create_foreign_key('Solutions_locationCard_fkey', 'Cards', ['locationCard'], ['id'])

    with op.batch_alter_table('PlayerOrder', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('PlayerOrder_gameId_fkey', 'Games', ['gameId'], ['id'])
        batch_op.create_foreign_key('PlayerOrder_playerId_fkey', 'Users', ['playerId'], ['id'])

    with op.batch_alter_table('PlayerInfos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('PlayerInfos_gameId_fkey', 'Games', ['gameId'], ['id'])
        batch_op.create_foreign_key('PlayerInfos_playerId_fkey', 'Users', ['playerId'], ['id'])
        batch_op.create_foreign_key('PlayerInfos_locationId_fkey', 'Locations', ['locationId'], ['id'])
        batch_op.create_foreign_key('PlayerInfos_characterId_fkey', 'Characters', ['characterId'], ['id'])
        batch_op.drop_column('mapSpotId')

    with op.batch_alter_table('Paths', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Paths_locationId1_fkey', 'Locations', ['locationId1'], ['id'])
        batch_op.create_foreign_key('Paths_locationId2_fkey', 'Locations', ['locationId2'], ['id'])

    with op.batch_alter_table('MapSpots', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('MapSpots_locationId_fkey', 'Locations', ['locationId'], ['id'])

    with op.batch_alter_table('Hands', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Hands_cardId_fkey', 'Cards', ['cardId'], ['id'])
        batch_op.create_foreign_key('Hands_gameId_fkey', 'Games', ['gameId'], ['id'])
        batch_op.create_foreign_key('Hands_playerInfo_fkey', 'PlayerInfos', ['playerInfo'], ['id'])

    with op.batch_alter_table('Guesses', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Guesses_weaponId_fkey', 'Weapons', ['weaponId'], ['id'])
        batch_op.create_foreign_key('Guesses_characterId_fkey', 'Characters', ['characterId'], ['id'])
        batch_op.create_foreign_key('Guesses_playerId_fkey', 'Users', ['playerId'], ['id'])
        batch_op.create_foreign_key('Guesses_gameId_fkey', 'Games', ['gameId'], ['id'])
        batch_op.create_foreign_key('Guesses_locationId_fkey', 'Locations', ['locationId'], ['id'])

    with op.batch_alter_table('Games', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Games_gameStatus_fkey', 'GameStatus', ['gameStatus'], ['id'])

    with op.batch_alter_table('Cards', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Cards_characterId_fkey', 'Characters', ['characterId'], ['id'])
        batch_op.create_foreign_key('Cards_locationId_fkey', 'Locations', ['locationId'], ['id'])
        batch_op.create_foreign_key('Cards_weaponId_fkey', 'Weapons', ['weaponId'], ['id'])

    # ### end Alembic commands ###
