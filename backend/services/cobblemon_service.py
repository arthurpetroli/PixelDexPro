from typing import Optional, List
from sqlalchemy.orm import Session
from repositories import CobblemonRepository, PokemonRepository
from models import CobblemonSpawn, Pokemon
from schemas import SpawnResponse, SpawnListResponse


class CobblemonService:
    """Service for Cobblemon-specific business logic."""

    def __init__(self, db: Session):
        self.db = db
        self.cobblemon_repo = CobblemonRepository(db)
        self.pokemon_repo = PokemonRepository(db)

    def _spawn_to_response(self, spawn: CobblemonSpawn) -> SpawnResponse:
        """Convert a CobblemonSpawn model to a response schema."""
        pokemon_name = None
        if spawn.pokemon:
            pokemon_name = spawn.pokemon.name

        return SpawnResponse(
            id=spawn.id,
            pokemon_id=spawn.pokemon_id,
            pokemon_name=pokemon_name,
            entry_number=spawn.entry_number,
            bucket=spawn.bucket,
            weight=spawn.weight,
            min_level=spawn.min_level,
            max_level=spawn.max_level,
            biomes=spawn.biomes or [],
            excluded_biomes=spawn.excluded_biomes or [],
            time=spawn.time,
            weather=spawn.weather or [],
            context=spawn.context,
            presets=spawn.presets or [],
            conditions=spawn.conditions or [],
            anticonditions=spawn.anticonditions or [],
            skylight_min=spawn.skylight_min,
            skylight_max=spawn.skylight_max,
            can_see_sky=spawn.can_see_sky,
            pattern_key_value=spawn.pattern_key_value or {},
            source_sheet=spawn.source_sheet,
            source_version=spawn.source_version,
        )

    def get_spawns_by_pokemon(self, pokemon_id: int) -> List[SpawnResponse]:
        """Get all spawn entries for a Pokémon."""
        spawns = self.cobblemon_repo.get_by_pokemon_id(pokemon_id)
        return [self._spawn_to_response(s) for s in spawns]

    def search_spawns(
        self,
        pokemon_name: Optional[str] = None,
        biome: Optional[str] = None,
        time: Optional[str] = None,
        weather: Optional[str] = None,
        min_level: Optional[int] = None,
        max_level: Optional[int] = None,
        context: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> SpawnListResponse:
        """Search spawns with filters."""
        skip = (page - 1) * page_size
        spawns, total = self.cobblemon_repo.list(
            skip=skip,
            limit=page_size,
            pokemon_name=pokemon_name,
            biome=biome,
            time=time,
            weather=weather,
            min_level=min_level,
            max_level=max_level,
            context=context,
        )

        items = [self._spawn_to_response(s) for s in spawns]

        return SpawnListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            has_next=skip + len(items) < total,
            has_prev=page > 1,
        )

    def get_all_biomes(self) -> List[str]:
        """Get all unique biomes from spawn data."""
        return self.cobblemon_repo.get_all_biomes()

    def get_spawn_times(self) -> List[str]:
        """Get all unique spawn times."""
        return ["any", "day", "night", "dawn", "dusk"]

    def get_spawn_weathers(self) -> List[str]:
        """Get all unique weather conditions."""
        return ["any", "clear", "rain", "thunder", "snow"]

    def get_spawn_contexts(self) -> List[str]:
        """Get all unique spawn contexts."""
        return ["grounded", "submerged", "surface", "seafloor"]
