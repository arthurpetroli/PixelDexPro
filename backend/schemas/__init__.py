from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TypeBase(BaseModel):
    name: str
    pokeapi_id: Optional[int] = None
    color: Optional[str] = None


class TypeResponse(TypeBase):
    id: int

    class Config:
        from_attributes = True


class StatBase(BaseModel):
    hp: int = 0
    attack: int = 0
    defense: int = 0
    special_attack: int = 0
    special_defense: int = 0
    speed: int = 0
    total: int = 0


class StatResponse(StatBase):
    id: int
    pokemon_id: int

    class Config:
        from_attributes = True


class PokemonTypeResponse(BaseModel):
    type: TypeResponse
    slot: int

    class Config:
        from_attributes = True


class AbilityBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_hidden: bool = False


class PokemonAbilityResponse(BaseModel):
    ability: AbilityBase
    slot: int
    is_hidden: bool

    class Config:
        from_attributes = True


class EvolutionResponse(BaseModel):
    to_pokemon_id: int
    trigger: Optional[str] = None
    min_level: Optional[int] = None
    item: Optional[str] = None
    condition: Optional[str] = None
    chain_order: int = 0

    class Config:
        from_attributes = True


class PokemonBase(BaseModel):
    name: str
    pokedex_number: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    base_experience: Optional[int] = None
    generation: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    sprite_url: Optional[str] = None
    sprite_shiny_url: Optional[str] = None
    sprite_official_url: Optional[str] = None


class PokemonResponse(PokemonBase):
    id: int
    pokeapi_id: Optional[int] = None
    is_default: bool = True
    forms: List[str] = []
    types: List[PokemonTypeResponse] = []
    abilities: List[PokemonAbilityResponse] = []
    stats: Optional[StatResponse] = None
    evolutions: List[EvolutionResponse] = []

    class Config:
        from_attributes = True


class PokemonListItem(BaseModel):
    id: int
    pokeapi_id: Optional[int] = None
    name: str
    pokedex_number: Optional[int] = None
    sprite_url: Optional[str] = None
    types: List[PokemonTypeResponse] = []
    generation: Optional[int] = None

    class Config:
        from_attributes = True


class PokemonListResponse(BaseModel):
    items: List[PokemonListItem]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


class PokemonFilterParams(BaseModel):
    type: Optional[str] = None
    generation: Optional[int] = None
    ability: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    page_size: int = 50


class PokemonDetailsResponse(PokemonResponse):
    weaknesses: Dict[str, float] = {}
    resistances: Dict[str, float] = {}
    immunities: List[str] = []
    quadruple_weaknesses: List[str] = []
    quadruple_resistances: List[str] = []
    strategic_tags: List[str] = []
    cobblemon_spawns: List["SpawnResponse"] = []


class CobblemonSpawnBase(BaseModel):
    entry_number: Optional[int] = None
    bucket: Optional[str] = None
    weight: Optional[float] = None
    min_level: Optional[int] = None
    max_level: Optional[int] = None
    biomes: List[str] = []
    excluded_biomes: List[str] = []
    time: Optional[str] = None
    weather: List[str] = []
    context: Optional[str] = None
    presets: List[str] = []
    conditions: List[str] = []
    anticonditions: List[str] = []
    skylight_min: Optional[int] = None
    skylight_max: Optional[int] = None
    can_see_sky: Optional[bool] = None
    pattern_key_value: Dict[str, Any] = {}
    source_sheet: Optional[str] = None
    source_version: Optional[str] = None


class SpawnResponse(CobblemonSpawnBase):
    id: int
    pokemon_id: int
    pokemon_name: Optional[str] = None

    class Config:
        from_attributes = True


class SpawnSearchParams(BaseModel):
    pokemon_name: Optional[str] = None
    biome: Optional[str] = None
    time: Optional[str] = None
    weather: Optional[str] = None
    min_level: Optional[int] = None
    max_level: Optional[int] = None
    context: Optional[str] = None
    page: int = 1
    page_size: int = 50


class SpawnListResponse(BaseModel):
    items: List[SpawnResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


class TypeEffectivenessChart(BaseModel):
    attacking_type: str
    defending_type: str
    multiplier: float


class TypeChartResponse(BaseModel):
    chart: Dict[str, Dict[str, float]]
    types: List[str]


class CompareResponse(BaseModel):
    pokemon1: PokemonDetailsResponse
    pokemon2: PokemonDetailsResponse
    stat_comparison: Dict[str, Dict[str, Any]]
    type_comparison: Dict[str, Any]
    spawn_comparison: Dict[str, Any]


class TeamPokemonBase(BaseModel):
    pokemon_id: int
    slot: int
    nickname: Optional[str] = None
    level: int = 50
    ability: Optional[str] = None
    nature: Optional[str] = None
    held_item: Optional[str] = None
    moves: List[str] = []


class TeamPokemonResponse(TeamPokemonBase):
    id: int
    team_id: int

    class Config:
        from_attributes = True


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False


class TeamResponse(TeamBase):
    id: int
    team_pokemon: List[TeamPokemonResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TeamAnalysis(BaseModel):
    team_id: int
    weaknesses: Dict[str, float]
    resistances: Dict[str, float]
    immunities: List[str]
    shared_weaknesses: Dict[str, List[str]]
    problematic_types: List[str]
    role_distribution: Dict[str, int]
    coverage_score: float
    defensive_score: float
    summary: str


class FavoriteResponse(BaseModel):
    id: int
    pokemon_id: int
    pokemon: PokemonListItem
    created_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class SyncStatus(BaseModel):
    status: str
    message: str
    synced_count: int = 0
    errors: List[str] = []
