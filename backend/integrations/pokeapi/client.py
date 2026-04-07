import httpx
from typing import Optional, Dict, Any, List
from core.config import get_settings

settings = get_settings()


class PokeAPIClient:
    """Client for consuming the PokéAPI."""

    def __init__(self):
        self.base_url = settings.POKEAPI_BASE_URL
        self.timeout = settings.POKEAPI_REQUEST_TIMEOUT

    async def _get(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make a GET request to the PokéAPI."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/{endpoint}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
            except httpx.RequestError:
                raise

    async def get_pokemon(self, name_or_id: str | int) -> Optional[Dict[str, Any]]:
        """Get a Pokémon by name or ID."""
        return await self._get(f"pokemon/{name_or_id}")

    async def get_pokemon_species(
        self, name_or_id: str | int
    ) -> Optional[Dict[str, Any]]:
        """Get Pokémon species data (includes description, generation, etc.)."""
        return await self._get(f"pokemon-species/{name_or_id}")

    async def get_evolution_chain(self, chain_id: int) -> Optional[Dict[str, Any]]:
        """Get an evolution chain by ID."""
        return await self._get(f"evolution-chain/{chain_id}")

    async def get_type(self, name_or_id: str | int) -> Optional[Dict[str, Any]]:
        """Get a type by name or ID."""
        return await self._get(f"type/{name_or_id}")

    async def get_ability(self, name_or_id: str | int) -> Optional[Dict[str, Any]]:
        """Get an ability by name or ID."""
        return await self._get(f"ability/{name_or_id}")

    async def get_item(self, name_or_id: str | int) -> Optional[Dict[str, Any]]:
        """Get an item by name or ID."""
        return await self._get(f"item/{name_or_id}")

    async def list_pokemon(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """List Pokémon with pagination."""
        result = await self._get(f"pokemon?limit={limit}&offset={offset}")
        return result or {"count": 0, "results": []}

    async def list_types(self) -> List[Dict[str, Any]]:
        """List all types."""
        result = await self._get("type")
        return result.get("results", []) if result else []

    async def list_generations(self) -> List[Dict[str, Any]]:
        """List all generations."""
        result = await self._get("generation")
        return result.get("results", []) if result else []


def parse_pokemon_data(
    pokemon_data: Dict[str, Any], species_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Parse raw PokéAPI data into our normalized format."""

    # Extract sprites
    sprites = pokemon_data.get("sprites", {})
    official_artwork = sprites.get("other", {}).get("official-artwork", {})

    # Extract stats
    stats_raw = pokemon_data.get("stats", [])
    stats = {
        "hp": 0,
        "attack": 0,
        "defense": 0,
        "special_attack": 0,
        "special_defense": 0,
        "speed": 0,
    }
    stat_mapping = {
        "hp": "hp",
        "attack": "attack",
        "defense": "defense",
        "special-attack": "special_attack",
        "special-defense": "special_defense",
        "speed": "speed",
    }
    for stat in stats_raw:
        stat_name = stat.get("stat", {}).get("name", "")
        if stat_name in stat_mapping:
            stats[stat_mapping[stat_name]] = stat.get("base_stat", 0)
    stats["total"] = sum(stats.values())

    # Extract types
    types = []
    for type_info in pokemon_data.get("types", []):
        types.append(
            {
                "name": type_info.get("type", {}).get("name", ""),
                "slot": type_info.get("slot", 1),
                "pokeapi_id": None,  # Will be populated separately
            }
        )

    # Extract abilities
    abilities = []
    for ability_info in pokemon_data.get("abilities", []):
        abilities.append(
            {
                "name": ability_info.get("ability", {}).get("name", ""),
                "slot": ability_info.get("slot", 1),
                "is_hidden": ability_info.get("is_hidden", False),
                "pokeapi_id": None,
            }
        )

    # Extract species data if available
    description = ""
    category = ""
    generation = None

    if species_data:
        # Get English description
        for entry in species_data.get("flavor_text_entries", []):
            if entry.get("language", {}).get("name") == "en":
                description = (
                    entry.get("flavor_text", "").replace("\n", " ").replace("\f", " ")
                )
                break

        # Get category/genus
        for genus in species_data.get("genera", []):
            if genus.get("language", {}).get("name") == "en":
                category = genus.get("genus", "")
                break

        # Get generation
        gen_url = species_data.get("generation", {}).get("url", "")
        if gen_url:
            try:
                generation = int(gen_url.rstrip("/").split("/")[-1])
            except ValueError:
                generation = None

    # Extract forms
    forms = [form.get("name", "") for form in pokemon_data.get("forms", [])]

    return {
        "pokemon": {
            "pokeapi_id": pokemon_data.get("id"),
            "name": pokemon_data.get("name", "").lower(),
            "pokedex_number": pokemon_data.get("id"),
            "height": pokemon_data.get("height", 0) / 10,  # Convert to meters
            "weight": pokemon_data.get("weight", 0) / 10,  # Convert to kg
            "base_experience": pokemon_data.get("base_experience"),
            "generation": generation,
            "category": category,
            "description": description,
            "sprite_url": sprites.get("front_default"),
            "sprite_shiny_url": sprites.get("front_shiny"),
            "sprite_official_url": official_artwork.get("front_default"),
            "is_default": pokemon_data.get("is_default", True),
            "forms": forms,
        },
        "stats": stats,
        "types": types,
        "abilities": abilities,
    }


def parse_evolution_chain(chain_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse evolution chain data into a list of evolution relationships."""
    evolutions = []

    def traverse_chain(chain: Dict[str, Any], order: int = 0):
        species_name = chain.get("species", {}).get("name", "")

        for evolution in chain.get("evolves_to", []):
            to_species = evolution.get("species", {}).get("name", "")

            # Get evolution details
            details = (
                evolution.get("evolution_details", [{}])[0]
                if evolution.get("evolution_details")
                else {}
            )

            trigger = details.get("trigger", {}).get("name", "")
            min_level = details.get("min_level")
            item = details.get("item", {}).get("name") if details.get("item") else None

            # Build condition string
            conditions = []
            if details.get("time_of_day"):
                conditions.append(f"time: {details['time_of_day']}")
            if details.get("location"):
                conditions.append(f"location: {details['location'].get('name', '')}")
            if details.get("held_item"):
                conditions.append(f"held_item: {details['held_item'].get('name', '')}")
            if details.get("min_happiness"):
                conditions.append(f"happiness: {details['min_happiness']}")
            if details.get("min_affection"):
                conditions.append(f"affection: {details['min_affection']}")

            evolutions.append(
                {
                    "from_pokemon_name": species_name,
                    "to_pokemon_name": to_species,
                    "trigger": trigger,
                    "min_level": min_level,
                    "item": item,
                    "condition": ", ".join(conditions) if conditions else None,
                    "chain_order": order,
                }
            )

            # Recursively process further evolutions
            traverse_chain(evolution, order + 1)

    traverse_chain(chain_data.get("chain", {}))
    return evolutions


pokeapi_client = PokeAPIClient()
