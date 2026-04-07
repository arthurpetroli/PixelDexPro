"""Initial migration

Revision ID: 001_initial
Revises:
Create Date: 2024-01-15

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True, default=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    # Types table
    op.create_table(
        "types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("pokeapi_id", sa.Integer(), nullable=True),
        sa.Column("color", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_types_id"), "types", ["id"], unique=False)
    op.create_index(op.f("ix_types_name"), "types", ["name"], unique=True)

    # Abilities table
    op.create_table(
        "abilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("pokeapi_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_hidden", sa.Boolean(), nullable=True, default=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_abilities_id"), "abilities", ["id"], unique=False)
    op.create_index(op.f("ix_abilities_name"), "abilities", ["name"], unique=True)

    # Pokemon table
    op.create_table(
        "pokemon",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pokeapi_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("pokedex_number", sa.Integer(), nullable=True),
        sa.Column("height", sa.Float(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("base_experience", sa.Integer(), nullable=True),
        sa.Column("generation", sa.Integer(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sprite_url", sa.String(length=500), nullable=True),
        sa.Column("sprite_shiny_url", sa.String(length=500), nullable=True),
        sa.Column("sprite_official_url", sa.String(length=500), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=True, default=True),
        sa.Column("forms", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pokemon_id"), "pokemon", ["id"], unique=False)
    op.create_index(op.f("ix_pokemon_name"), "pokemon", ["name"], unique=True)
    op.create_index(
        op.f("ix_pokemon_pokeapi_id"), "pokemon", ["pokeapi_id"], unique=True
    )
    op.create_index(
        op.f("ix_pokemon_pokedex_number"), "pokemon", ["pokedex_number"], unique=False
    )
    op.create_index(
        op.f("ix_pokemon_generation"), "pokemon", ["generation"], unique=False
    )

    # PokemonType table
    op.create_table(
        "pokemon_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pokemon_id", sa.Integer(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("slot", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pokemon_id"],
            ["pokemon.id"],
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pokemon_id", "type_id", "slot"),
    )
    op.create_index(op.f("ix_pokemon_types_id"), "pokemon_types", ["id"], unique=False)

    # PokemonAbility table
    op.create_table(
        "pokemon_abilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pokemon_id", sa.Integer(), nullable=False),
        sa.Column("ability_id", sa.Integer(), nullable=False),
        sa.Column("slot", sa.Integer(), nullable=False),
        sa.Column("is_hidden", sa.Boolean(), nullable=True, default=False),
        sa.ForeignKeyConstraint(
            ["ability_id"],
            ["abilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["pokemon_id"],
            ["pokemon.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pokemon_id", "ability_id", "slot"),
    )
    op.create_index(
        op.f("ix_pokemon_abilities_id"), "pokemon_abilities", ["id"], unique=False
    )

    # Stats table
    op.create_table(
        "stats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pokemon_id", sa.Integer(), nullable=False),
        sa.Column("hp", sa.Integer(), nullable=True, default=0),
        sa.Column("attack", sa.Integer(), nullable=True, default=0),
        sa.Column("defense", sa.Integer(), nullable=True, default=0),
        sa.Column("special_attack", sa.Integer(), nullable=True, default=0),
        sa.Column("special_defense", sa.Integer(), nullable=True, default=0),
        sa.Column("speed", sa.Integer(), nullable=True, default=0),
        sa.Column("total", sa.Integer(), nullable=True, default=0),
        sa.ForeignKeyConstraint(
            ["pokemon_id"],
            ["pokemon.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pokemon_id"),
    )
    op.create_index(op.f("ix_stats_id"), "stats", ["id"], unique=False)

    # Evolutions table
    op.create_table(
        "evolutions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("from_pokemon_id", sa.Integer(), nullable=False),
        sa.Column("to_pokemon_id", sa.Integer(), nullable=False),
        sa.Column("trigger", sa.String(length=100), nullable=True),
        sa.Column("min_level", sa.Integer(), nullable=True),
        sa.Column("item", sa.String(length=100), nullable=True),
        sa.Column("condition", sa.Text(), nullable=True),
        sa.Column("chain_order", sa.Integer(), nullable=True, default=0),
        sa.ForeignKeyConstraint(
            ["from_pokemon_id"],
            ["pokemon.id"],
        ),
        sa.ForeignKeyConstraint(
            ["to_pokemon_id"],
            ["pokemon.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_evolutions_id"), "evolutions", ["id"], unique=False)

    # Items table
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pokeapi_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("sprite_url", sa.String(length=500), nullable=True),
        sa.Column("effect", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_items_id"), "items", ["id"], unique=False)
    op.create_index(op.f("ix_items_name"), "items", ["name"], unique=True)

    # CobblemonSpawn table
    op.create_table(
        "cobblemon_spawns",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pokemon_id", sa.Integer(), nullable=False),
        sa.Column("entry_number", sa.Integer(), nullable=True),
        sa.Column("bucket", sa.String(length=100), nullable=True),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("min_level", sa.Integer(), nullable=True),
        sa.Column("max_level", sa.Integer(), nullable=True),
        sa.Column("biomes", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "excluded_biomes", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("time", sa.String(length=50), nullable=True),
        sa.Column("weather", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("context", sa.String(length=100), nullable=True),
        sa.Column("presets", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("conditions", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "anticonditions", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("skylight_min", sa.Integer(), nullable=True),
        sa.Column("skylight_max", sa.Integer(), nullable=True),
        sa.Column("can_see_sky", sa.Boolean(), nullable=True),
        sa.Column(
            "pattern_key_value", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("source_sheet", sa.String(length=500), nullable=True),
        sa.Column("source_version", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["pokemon_id"],
            ["pokemon.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_cobblemon_spawns_id"), "cobblemon_spawns", ["id"], unique=False
    )

    # CobblemonDrop table
    op.create_table(
        "cobblemon_drops",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pokemon_id", sa.Integer(), nullable=False),
        sa.Column("item_name", sa.String(length=100), nullable=False),
        sa.Column("min_quantity", sa.Integer(), nullable=True, default=1),
        sa.Column("max_quantity", sa.Integer(), nullable=True, default=1),
        sa.Column("drop_chance", sa.Float(), nullable=True),
        sa.Column("condition", sa.Text(), nullable=True),
        sa.Column("source", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["pokemon_id"],
            ["pokemon.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_cobblemon_drops_id"), "cobblemon_drops", ["id"], unique=False
    )

    # Teams table
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_public", sa.Boolean(), nullable=True, default=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_teams_id"), "teams", ["id"], unique=False)

    # TeamPokemon table
    op.create_table(
        "team_pokemon",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("pokemon_id", sa.Integer(), nullable=False),
        sa.Column("slot", sa.Integer(), nullable=False),
        sa.Column("nickname", sa.String(length=100), nullable=True),
        sa.Column("level", sa.Integer(), nullable=True, default=50),
        sa.Column("ability", sa.String(length=100), nullable=True),
        sa.Column("nature", sa.String(length=50), nullable=True),
        sa.Column("held_item", sa.String(length=100), nullable=True),
        sa.Column("moves", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(
            ["pokemon_id"],
            ["pokemon.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("team_id", "pokemon_id"),
    )
    op.create_index(op.f("ix_team_pokemon_id"), "team_pokemon", ["id"], unique=False)

    # Favorites table
    op.create_table(
        "favorites",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("pokemon_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["pokemon_id"],
            ["pokemon.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "pokemon_id"),
    )
    op.create_index(op.f("ix_favorites_id"), "favorites", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("favorites")
    op.drop_table("team_pokemon")
    op.drop_table("teams")
    op.drop_table("cobblemon_drops")
    op.drop_table("cobblemon_spawns")
    op.drop_table("items")
    op.drop_table("evolutions")
    op.drop_table("stats")
    op.drop_table("pokemon_abilities")
    op.drop_table("pokemon_types")
    op.drop_table("pokemon")
    op.drop_table("abilities")
    op.drop_table("types")
    op.drop_table("users")
