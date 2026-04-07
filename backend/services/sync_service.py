from typing import List, Optional
from sqlalchemy.orm import Session
from repositories import PokemonRepository, CobblemonRepository
from models import (
    Pokemon,
    Type,
    Stat,
    PokemonType,
    Ability,
    PokemonAbility,
    CobblemonSpawn,
    Evolution,
)
from integrations.pokeapi.client import (
    pokeapi_client,
    parse_pokemon_data,
    parse_evolution_chain,
)
from integrations.cobblemon.sheet_ingestion import cobblemon_ingestion
from schemas import SyncStatus
from services.type_effectiveness import TYPE_COLORS


class SyncService:
    """Service for synchronizing data from external sources."""

    def __init__(self, db: Session):
        self.db = db
        self.pokemon_repo = PokemonRepository(db)
        self.cobblemon_repo = CobblemonRepository(db)

    async def sync_pokemon(self, name_or_id: str) -> SyncStatus:
        """Sync a single Pokémon from PokéAPI."""
        errors = []

        try:
            # Fetch Pokémon data
            pokemon_data = await pokeapi_client.get_pokemon(name_or_id)
            if not pokemon_data:
                return SyncStatus(
                    status="error",
                    message=f"Pokémon '{name_or_id}' not found in PokéAPI",
                    synced_count=0,
                )

            # Fetch species data for additional info
            species_data = await pokeapi_client.get_pokemon_species(pokemon_data["id"])

            # Parse the data
            parsed = parse_pokemon_data(pokemon_data, species_data)

            # Check if Pokémon exists
            existing = self.pokemon_repo.get_by_pokeapi_id(pokemon_data["id"])

            if existing:
                # Update existing
                for key, value in parsed["pokemon"].items():
                    setattr(existing, key, value)

                # Update stats
                if existing.stats:
                    for key, value in parsed["stats"].items():
                        setattr(existing.stats, key, value)

                self.db.commit()
                pokemon = existing
            else:
                # Create new
                pokemon = self.pokemon_repo.create(
                    pokemon_data=parsed["pokemon"],
                    stats_data=parsed["stats"],
                    types_data=parsed["types"],
                    abilities_data=parsed["abilities"],
                )

            return SyncStatus(
                status="success",
                message=f"Successfully synced {pokemon.name}",
                synced_count=1,
            )

        except Exception as e:
            errors.append(str(e))
            return SyncStatus(
                status="error",
                message=f"Failed to sync Pokémon: {str(e)}",
                synced_count=0,
                errors=errors,
            )

    async def sync_pokemon_batch(self, limit: int = 151, offset: int = 0) -> SyncStatus:
        """Sync multiple Pokémon from PokéAPI."""
        errors = []
        synced = 0

        try:
            # Get list of Pokémon
            pokemon_list = await pokeapi_client.list_pokemon(limit=limit, offset=offset)

            for pokemon_ref in pokemon_list.get("results", []):
                try:
                    result = await self.sync_pokemon(pokemon_ref["name"])
                    if result.status == "success":
                        synced += 1
                    else:
                        errors.extend(result.errors)
                except Exception as e:
                    errors.append(f"Error syncing {pokemon_ref['name']}: {str(e)}")

            return SyncStatus(
                status="success" if synced > 0 else "error",
                message=f"Synced {synced}/{limit} Pokémon",
                synced_count=synced,
                errors=errors,
            )

        except Exception as e:
            return SyncStatus(
                status="error",
                message=f"Failed to sync batch: {str(e)}",
                synced_count=synced,
                errors=errors + [str(e)],
            )

    async def sync_types(self) -> SyncStatus:
        """Sync all types from PokéAPI."""
        errors = []
        synced = 0

        try:
            types_list = await pokeapi_client.list_types()

            for type_ref in types_list:
                try:
                    type_data = await pokeapi_client.get_type(type_ref["name"])
                    if not type_data:
                        continue

                    type_name = type_data["name"].lower()

                    # Check if type exists
                    existing = (
                        self.db.query(Type).filter(Type.name == type_name).first()
                    )

                    if existing:
                        existing.pokeapi_id = type_data["id"]
                        existing.color = TYPE_COLORS.get(type_name)
                    else:
                        new_type = Type(
                            name=type_name,
                            pokeapi_id=type_data["id"],
                            color=TYPE_COLORS.get(type_name),
                        )
                        self.db.add(new_type)

                    synced += 1

                except Exception as e:
                    errors.append(f"Error syncing type {type_ref['name']}: {str(e)}")

            self.db.commit()

            return SyncStatus(
                status="success",
                message=f"Synced {synced} types",
                synced_count=synced,
                errors=errors,
            )

        except Exception as e:
            return SyncStatus(
                status="error",
                message=f"Failed to sync types: {str(e)}",
                synced_count=synced,
                errors=errors + [str(e)],
            )

    async def sync_cobblemon_spawns(
        self, sheet_url: str, version: str = "1.0"
    ) -> SyncStatus:
        """Sync Cobblemon spawn data from a Google Sheet."""
        errors = []
        synced = 0

        try:
            # Fetch and parse spawn data
            spawns = await cobblemon_ingestion.ingest_from_url(sheet_url, version)

            for spawn_data in spawns:
                try:
                    # Find the Pokémon
                    pokemon = self.pokemon_repo.get_by_name(spawn_data["pokemon_name"])
                    if not pokemon:
                        errors.append(
                            f"Pokémon not found: {spawn_data['pokemon_name']}"
                        )
                        continue

                    # Remove pokemon_name and add pokemon_id
                    del spawn_data["pokemon_name"]
                    spawn_data["pokemon_id"] = pokemon.id

                    # Upsert the spawn
                    self.cobblemon_repo.upsert_by_pokemon_and_entry(
                        pokemon_id=pokemon.id,
                        entry_number=spawn_data.get("entry_number"),
                        spawn_data=spawn_data,
                    )
                    synced += 1

                except Exception as e:
                    errors.append(f"Error processing spawn: {str(e)}")

            return SyncStatus(
                status="success" if synced > 0 else "error",
                message=f"Synced {synced} spawn entries",
                synced_count=synced,
                errors=errors,
            )

        except Exception as e:
            return SyncStatus(
                status="error",
                message=f"Failed to sync spawns: {str(e)}",
                synced_count=synced,
                errors=errors + [str(e)],
            )
