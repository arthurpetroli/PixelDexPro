from typing import Optional
from sqlalchemy.orm import Session
from services.pokemon_service import PokemonService
from services.cobblemon_service import CobblemonService
from services.type_effectiveness import (
    calculate_type_effectiveness,
    get_weaknesses,
    get_resistances,
    get_immunities,
    get_quadruple_weaknesses,
    get_quadruple_resistances,
)
from schemas import CompareResponse, PokemonDetailsResponse


class CompareService:
    """Service for comparing two Pokémon."""

    def __init__(self, db: Session):
        self.db = db
        self.pokemon_service = PokemonService(db)
        self.cobblemon_service = CobblemonService(db)

    def compare_pokemon(
        self, pokemon1_id: int, pokemon2_id: int
    ) -> Optional[CompareResponse]:
        """Compare two Pokémon side by side."""
        pokemon1 = self.pokemon_service.get_pokemon_details(pokemon1_id)
        pokemon2 = self.pokemon_service.get_pokemon_details(pokemon2_id)

        if not pokemon1 or not pokemon2:
            return None

        # Compare stats
        stat_comparison = self._compare_stats(pokemon1, pokemon2)

        # Compare types
        type_comparison = self._compare_types(pokemon1, pokemon2)

        # Compare spawns
        spawn_comparison = self._compare_spawns(pokemon1, pokemon2)

        return CompareResponse(
            pokemon1=pokemon1,
            pokemon2=pokemon2,
            stat_comparison=stat_comparison,
            type_comparison=type_comparison,
            spawn_comparison=spawn_comparison,
        )

    def _compare_stats(
        self, pokemon1: PokemonDetailsResponse, pokemon2: PokemonDetailsResponse
    ) -> dict:
        """Compare the stats of two Pokémon."""
        stats1 = pokemon1.stats
        stats2 = pokemon2.stats

        if not stats1 or not stats2:
            return {}

        stat_names = [
            "hp",
            "attack",
            "defense",
            "special_attack",
            "special_defense",
            "speed",
            "total",
        ]
        comparison = {}

        for stat in stat_names:
            val1 = getattr(stats1, stat, 0)
            val2 = getattr(stats2, stat, 0)
            diff = val1 - val2
            winner = (
                pokemon1.name if diff > 0 else (pokemon2.name if diff < 0 else "tie")
            )

            comparison[stat] = {
                "pokemon1_value": val1,
                "pokemon2_value": val2,
                "difference": diff,
                "winner": winner,
            }

        return comparison

    def _compare_types(
        self, pokemon1: PokemonDetailsResponse, pokemon2: PokemonDetailsResponse
    ) -> dict:
        """Compare type effectiveness of two Pokémon."""
        return {
            "pokemon1_types": [t.type.name for t in pokemon1.types],
            "pokemon2_types": [t.type.name for t in pokemon2.types],
            "pokemon1_weaknesses": list(pokemon1.weaknesses.keys()),
            "pokemon2_weaknesses": list(pokemon2.weaknesses.keys()),
            "pokemon1_resistances": list(pokemon1.resistances.keys()),
            "pokemon2_resistances": list(pokemon2.resistances.keys()),
            "pokemon1_immunities": pokemon1.immunities,
            "pokemon2_immunities": pokemon2.immunities,
            "shared_weaknesses": [
                t for t in pokemon1.weaknesses.keys() if t in pokemon2.weaknesses
            ],
            "shared_resistances": [
                t for t in pokemon1.resistances.keys() if t in pokemon2.resistances
            ],
        }

    def _compare_spawns(
        self, pokemon1: PokemonDetailsResponse, pokemon2: PokemonDetailsResponse
    ) -> dict:
        """Compare Cobblemon spawn data of two Pokémon."""
        spawns1 = pokemon1.cobblemon_spawns
        spawns2 = pokemon2.cobblemon_spawns

        # Extract biomes
        biomes1 = set()
        biomes2 = set()
        for spawn in spawns1:
            biomes1.update(spawn.biomes)
        for spawn in spawns2:
            biomes2.update(spawn.biomes)

        return {
            "pokemon1_spawn_count": len(spawns1),
            "pokemon2_spawn_count": len(spawns2),
            "pokemon1_biomes": list(biomes1),
            "pokemon2_biomes": list(biomes2),
            "shared_biomes": list(biomes1.intersection(biomes2)),
            "pokemon1_has_spawns": len(spawns1) > 0,
            "pokemon2_has_spawns": len(spawns2) > 0,
        }
