from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from models import CobblemonSpawn, Pokemon
from schemas import CobblemonSpawnBase


class CobblemonRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, spawn_id: int) -> Optional[CobblemonSpawn]:
        return (
            self.db.query(CobblemonSpawn).filter(CobblemonSpawn.id == spawn_id).first()
        )

    def get_by_pokemon_id(self, pokemon_id: int) -> List[CobblemonSpawn]:
        return (
            self.db.query(CobblemonSpawn)
            .filter(CobblemonSpawn.pokemon_id == pokemon_id)
            .all()
        )

    def list(
        self,
        skip: int = 0,
        limit: int = 50,
        pokemon_name: Optional[str] = None,
        biome: Optional[str] = None,
        time: Optional[str] = None,
        weather: Optional[str] = None,
        min_level: Optional[int] = None,
        max_level: Optional[int] = None,
        context: Optional[str] = None,
    ) -> tuple[List[CobblemonSpawn], int]:
        query = self.db.query(CobblemonSpawn).join(Pokemon)

        if pokemon_name:
            query = query.filter(Pokemon.name.ilike(f"%{pokemon_name}%"))

        if biome:
            query = query.filter(CobblemonSpawn.biomes.contains([biome.lower()]))

        if time:
            query = query.filter(CobblemonSpawn.time == time.lower())

        if weather:
            query = query.filter(CobblemonSpawn.weather.contains([weather.lower()]))

        if min_level is not None:
            query = query.filter(CobblemonSpawn.max_level >= min_level)

        if max_level is not None:
            query = query.filter(CobblemonSpawn.min_level <= max_level)

        if context:
            query = query.filter(CobblemonSpawn.context == context.lower())

        total = query.count()
        items = query.offset(skip).limit(limit).all()

        return items, total

    def create(self, spawn_data: Dict) -> CobblemonSpawn:
        spawn = CobblemonSpawn(**spawn_data)
        self.db.add(spawn)
        self.db.commit()
        self.db.refresh(spawn)
        return spawn

    def upsert_by_pokemon_and_entry(
        self, pokemon_id: int, entry_number: Optional[int], spawn_data: Dict
    ) -> CobblemonSpawn:
        query = self.db.query(CobblemonSpawn).filter(
            CobblemonSpawn.pokemon_id == pokemon_id,
            CobblemonSpawn.entry_number == entry_number,
        )

        existing = query.first()
        if existing:
            for key, value in spawn_data.items():
                setattr(existing, key, value)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            return self.create(spawn_data)

    def delete_by_source(self, source_sheet: str) -> int:
        deleted = (
            self.db.query(CobblemonSpawn)
            .filter(CobblemonSpawn.source_sheet == source_sheet)
            .delete(synchronize_session=False)
        )
        self.db.commit()
        return deleted

    def get_all_biomes(self) -> List[str]:
        """Get all unique biomes from spawn data."""
        # Fetch all spawn entries and extract biomes from JSON arrays
        spawns = self.db.query(CobblemonSpawn.biomes).all()
        biomes_set = set()

        for spawn in spawns:
            if spawn[0]:  # Check if biomes field exists
                # biomes is a list in the JSON column
                if isinstance(spawn[0], list):
                    biomes_set.update(spawn[0])

        return sorted(list(biomes_set))
