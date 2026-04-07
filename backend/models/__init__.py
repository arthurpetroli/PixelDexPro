from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teams = relationship("Team", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")


class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    pokeapi_id = Column(Integer, unique=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    pokedex_number = Column(Integer, index=True)
    height = Column(Float)
    weight = Column(Float)
    base_experience = Column(Integer)
    generation = Column(Integer, index=True)
    category = Column(String(100))
    description = Column(Text)
    sprite_url = Column(String(500))
    sprite_shiny_url = Column(String(500))
    sprite_official_url = Column(String(500))
    is_default = Column(Boolean, default=True)
    forms = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    types = relationship(
        "PokemonType", back_populates="pokemon", cascade="all, delete-orphan"
    )
    abilities = relationship(
        "PokemonAbility", back_populates="pokemon", cascade="all, delete-orphan"
    )
    stats = relationship(
        "Stat", back_populates="pokemon", uselist=False, cascade="all, delete-orphan"
    )
    evolutions = relationship(
        "Evolution",
        foreign_keys="[Evolution.from_pokemon_id]",
        back_populates="from_pokemon",
        cascade="all, delete-orphan",
    )
    evolved_from = relationship(
        "Evolution",
        foreign_keys="[Evolution.to_pokemon_id]",
        back_populates="to_pokemon",
    )
    cobblemon_spawns = relationship("CobblemonSpawn", back_populates="pokemon")
    cobblemon_drops = relationship("CobblemonDrop", back_populates="pokemon")
    favorites = relationship("Favorite", back_populates="pokemon")


class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    pokeapi_id = Column(Integer, unique=True)
    color = Column(String(20))

    pokemon_types = relationship("PokemonType", back_populates="type")


class PokemonType(Base):
    __tablename__ = "pokemon_types"
    __table_args__ = (UniqueConstraint("pokemon_id", "type_id", "slot"),)

    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("types.id"), nullable=False)
    slot = Column(Integer, nullable=False)

    pokemon = relationship("Pokemon", back_populates="types")
    type = relationship("Type", back_populates="pokemon_types")


class Ability(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    pokeapi_id = Column(Integer, unique=True)
    description = Column(Text)
    is_hidden = Column(Boolean, default=False)

    pokemon_abilities = relationship("PokemonAbility", back_populates="ability")


class PokemonAbility(Base):
    __tablename__ = "pokemon_abilities"
    __table_args__ = (UniqueConstraint("pokemon_id", "ability_id", "slot"),)

    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    ability_id = Column(Integer, ForeignKey("abilities.id"), nullable=False)
    slot = Column(Integer, nullable=False)
    is_hidden = Column(Boolean, default=False)

    pokemon = relationship("Pokemon", back_populates="abilities")
    ability = relationship("Ability", back_populates="pokemon_abilities")


class Stat(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), unique=True, nullable=False)
    hp = Column(Integer, default=0)
    attack = Column(Integer, default=0)
    defense = Column(Integer, default=0)
    special_attack = Column(Integer, default=0)
    special_defense = Column(Integer, default=0)
    speed = Column(Integer, default=0)
    total = Column(Integer, default=0)

    pokemon = relationship("Pokemon", back_populates="stats")


class Evolution(Base):
    __tablename__ = "evolutions"

    id = Column(Integer, primary_key=True, index=True)
    from_pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    to_pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    trigger = Column(String(100))
    min_level = Column(Integer)
    item = Column(String(100))
    condition = Column(Text)
    chain_order = Column(Integer, default=0)

    from_pokemon = relationship(
        "Pokemon", foreign_keys=[from_pokemon_id], back_populates="evolutions"
    )
    to_pokemon = relationship(
        "Pokemon", foreign_keys=[to_pokemon_id], back_populates="evolved_from"
    )


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    pokeapi_id = Column(Integer, unique=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text)
    category = Column(String(100))
    sprite_url = Column(String(500))
    effect = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class CobblemonSpawn(Base):
    __tablename__ = "cobblemon_spawns"

    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    entry_number = Column(Integer)
    bucket = Column(String(100))
    weight = Column(Float)
    min_level = Column(Integer)
    max_level = Column(Integer)
    biomes = Column(JSON, default=list)
    excluded_biomes = Column(JSON, default=list)
    time = Column(String(50))
    weather = Column(JSON, default=list)
    context = Column(String(100))
    presets = Column(JSON, default=list)
    conditions = Column(JSON, default=list)
    anticonditions = Column(JSON, default=list)
    skylight_min = Column(Integer)
    skylight_max = Column(Integer)
    can_see_sky = Column(Boolean)
    pattern_key_value = Column(JSON, default=dict)
    source_sheet = Column(String(500))
    source_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pokemon = relationship("Pokemon", back_populates="cobblemon_spawns")


class CobblemonDrop(Base):
    __tablename__ = "cobblemon_drops"

    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    item_name = Column(String(100), nullable=False)
    min_quantity = Column(Integer, default=1)
    max_quantity = Column(Integer, default=1)
    drop_chance = Column(Float)
    condition = Column(Text)
    source = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    pokemon = relationship("Pokemon", back_populates="cobblemon_drops")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="teams")
    team_pokemon = relationship(
        "TeamPokemon", back_populates="team", cascade="all, delete-orphan"
    )


class TeamPokemon(Base):
    __tablename__ = "team_pokemon"
    __table_args__ = (UniqueConstraint("team_id", "pokemon_id"),)

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    slot = Column(Integer, nullable=False)
    nickname = Column(String(100))
    level = Column(Integer, default=50)
    ability = Column(String(100))
    nature = Column(String(50))
    held_item = Column(String(100))
    moves = Column(JSON, default=list)

    team = relationship("Team", back_populates="team_pokemon")
    pokemon = relationship("Pokemon")


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "pokemon_id"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    pokemon = relationship("Pokemon", back_populates="favorites")
