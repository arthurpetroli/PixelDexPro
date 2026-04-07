from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from repositories import PokemonRepository, CobblemonRepository
from models import Pokemon, Type, PokemonType
from services.type_effectiveness import (
    calculate_type_effectiveness,
    get_weaknesses,
    get_resistances,
    get_immunities,
    get_quadruple_weaknesses,
    get_quadruple_resistances,
    get_strategic_tags,
)
from schemas import (
    PokemonResponse,
    PokemonListResponse,
    PokemonListItem,
    PokemonDetailsResponse,
    PokemonTypeResponse,
    PokemonAbilityResponse,
    StatResponse,
    EvolutionResponse,
    TypeResponse,
    AbilityBase,
    SpawnResponse,
)


class PokemonService:
    """Service for Pokémon business logic."""

    def __init__(self, db: Session):
        self.db = db
        self.pokemon_repo = PokemonRepository(db)
        self.cobblemon_repo = CobblemonRepository(db)

    def _pokemon_to_list_item(self, pokemon: Pokemon) -> PokemonListItem:
        """Convert a Pokemon model to a list item schema."""
        types = []
        for pt in pokemon.types:
            types.append(
                PokemonTypeResponse(
                    type=TypeResponse(
                        id=pt.type.id,
                        name=pt.type.name,
                        pokeapi_id=pt.type.pokeapi_id,
                        color=pt.type.color,
                    ),
                    slot=pt.slot,
                )
            )

        return PokemonListItem(
            id=pokemon.id,
            pokeapi_id=pokemon.pokeapi_id,
            name=pokemon.name,
            pokedex_number=pokemon.pokedex_number,
            sprite_url=pokemon.sprite_url,
            types=types,
            generation=pokemon.generation,
        )

    def _pokemon_to_response(self, pokemon: Pokemon) -> PokemonResponse:
        """Convert a Pokemon model to a response schema."""
        types = []
        for pt in sorted(pokemon.types, key=lambda x: x.slot):
            types.append(
                PokemonTypeResponse(
                    type=TypeResponse(
                        id=pt.type.id,
                        name=pt.type.name,
                        pokeapi_id=pt.type.pokeapi_id,
                        color=pt.type.color,
                    ),
                    slot=pt.slot,
                )
            )

        abilities = []
        for pa in sorted(pokemon.abilities, key=lambda x: x.slot):
            abilities.append(
                PokemonAbilityResponse(
                    ability=AbilityBase(
                        name=pa.ability.name,
                        description=pa.ability.description,
                        is_hidden=pa.ability.is_hidden,
                    ),
                    slot=pa.slot,
                    is_hidden=pa.is_hidden,
                )
            )

        stats = None
        if pokemon.stats:
            stats = StatResponse(
                id=pokemon.stats.id,
                pokemon_id=pokemon.id,
                hp=pokemon.stats.hp,
                attack=pokemon.stats.attack,
                defense=pokemon.stats.defense,
                special_attack=pokemon.stats.special_attack,
                special_defense=pokemon.stats.special_defense,
                speed=pokemon.stats.speed,
                total=pokemon.stats.total,
            )

        evolutions = []
        for evo in pokemon.evolutions:
            evolutions.append(
                EvolutionResponse(
                    to_pokemon_id=evo.to_pokemon_id,
                    trigger=evo.trigger,
                    min_level=evo.min_level,
                    item=evo.item,
                    condition=evo.condition,
                    chain_order=evo.chain_order,
                )
            )

        return PokemonResponse(
            id=pokemon.id,
            pokeapi_id=pokemon.pokeapi_id,
            name=pokemon.name,
            pokedex_number=pokemon.pokedex_number,
            height=pokemon.height,
            weight=pokemon.weight,
            base_experience=pokemon.base_experience,
            generation=pokemon.generation,
            category=pokemon.category,
            description=pokemon.description,
            sprite_url=pokemon.sprite_url,
            sprite_shiny_url=pokemon.sprite_shiny_url,
            sprite_official_url=pokemon.sprite_official_url,
            is_default=pokemon.is_default,
            forms=pokemon.forms or [],
            types=types,
            abilities=abilities,
            stats=stats,
            evolutions=evolutions,
        )

    def get_pokemon_by_id(self, pokemon_id: int) -> Optional[PokemonResponse]:
        """Get a Pokémon by ID."""
        pokemon = self.pokemon_repo.get_by_id(pokemon_id)
        if not pokemon:
            return None
        return self._pokemon_to_response(pokemon)

    def get_pokemon_by_name(self, name: str) -> Optional[PokemonResponse]:
        """Get a Pokémon by name."""
        pokemon = self.pokemon_repo.get_by_name(name)
        if not pokemon:
            return None
        return self._pokemon_to_response(pokemon)

    def list_pokemon(
        self,
        page: int = 1,
        page_size: int = 50,
        type_filter: Optional[str] = None,
        generation: Optional[int] = None,
        search: Optional[str] = None,
        pokemon_pool: str = "all",
    ) -> PokemonListResponse:
        """List Pokémon with pagination and filters."""
        skip = (page - 1) * page_size
        items, total = self.pokemon_repo.list(
            skip=skip,
            limit=page_size,
            type_filter=type_filter,
            generation=generation,
            search=search,
            pokemon_pool=pokemon_pool,
        )

        pokemon_items = [self._pokemon_to_list_item(p) for p in items]

        return PokemonListResponse(
            items=pokemon_items,
            total=total,
            page=page,
            page_size=page_size,
            has_next=skip + len(items) < total,
            has_prev=page > 1,
        )

    def get_pokemon_details(self, pokemon_id: int) -> Optional[PokemonDetailsResponse]:
        """Get detailed Pokémon info including type effectiveness and spawns."""
        pokemon = self.pokemon_repo.get_by_id(pokemon_id)
        if not pokemon:
            return None

        base_response = self._pokemon_to_response(pokemon)

        # Calculate type effectiveness
        pokemon_types = [pt.type.name for pt in pokemon.types]
        effectiveness = calculate_type_effectiveness(pokemon_types)

        weaknesses = get_weaknesses(effectiveness)
        resistances = get_resistances(effectiveness)
        immunities = get_immunities(effectiveness)
        quad_weak = get_quadruple_weaknesses(effectiveness)
        quad_resist = get_quadruple_resistances(effectiveness)
        strategic_tags = get_strategic_tags(pokemon_types, effectiveness)

        # Get Cobblemon spawns
        spawns = self.cobblemon_repo.get_by_pokemon_id(pokemon_id)
        spawn_responses = []
        for spawn in spawns:
            spawn_responses.append(
                SpawnResponse(
                    id=spawn.id,
                    pokemon_id=spawn.pokemon_id,
                    pokemon_name=pokemon.name,
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
            )

        return PokemonDetailsResponse(
            **base_response.model_dump(),
            weaknesses=weaknesses,
            resistances=resistances,
            immunities=immunities,
            quadruple_weaknesses=quad_weak,
            quadruple_resistances=quad_resist,
            strategic_tags=strategic_tags,
            cobblemon_spawns=spawn_responses,
        )

    def search_pokemon(self, query: str, limit: int = 20) -> List[PokemonListItem]:
        """Search Pokémon by name."""
        items, _ = self.pokemon_repo.list(skip=0, limit=limit, search=query)
        return [self._pokemon_to_list_item(p) for p in items]
