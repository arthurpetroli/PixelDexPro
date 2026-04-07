from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models import Pokemon, Stat, PokemonType, PokemonAbility, Ability, Type, Evolution
from schemas import PokemonBase, StatBase


class PokemonRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, pokemon_id: int) -> Optional[Pokemon]:
        return self.db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

    def get_by_pokeapi_id(self, pokeapi_id: int) -> Optional[Pokemon]:
        return self.db.query(Pokemon).filter(Pokemon.pokeapi_id == pokeapi_id).first()

    def get_by_name(self, name: str) -> Optional[Pokemon]:
        return self.db.query(Pokemon).filter(Pokemon.name.ilike(name)).first()

    def list(
        self,
        skip: int = 0,
        limit: int = 50,
        type_filter: Optional[str] = None,
        generation: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[List[Pokemon], int]:
        query = self.db.query(Pokemon).filter(Pokemon.is_default == True)

        if search:
            query = query.filter(Pokemon.name.ilike(f"%{search}%"))

        if generation:
            query = query.filter(Pokemon.generation == generation)

        if type_filter:
            query = (
                query.join(PokemonType)
                .join(Type)
                .filter(Type.name == type_filter.lower())
            )

        total = query.count()
        items = query.offset(skip).limit(limit).all()

        return items, total

    def create(
        self,
        pokemon_data: Dict[str, Any],
        stats_data: Dict[str, Any],
        types_data: List[Dict],
        abilities_data: List[Dict],
    ) -> Pokemon:
        pokemon = Pokemon(**pokemon_data)
        self.db.add(pokemon)
        self.db.flush()

        if stats_data:
            stats = Stat(pokemon_id=pokemon.id, **stats_data)
            self.db.add(stats)

        for type_info in types_data:
            type_record = (
                self.db.query(Type)
                .filter(Type.name == type_info["name"].lower())
                .first()
            )
            if not type_record:
                type_record = Type(
                    name=type_info["name"].lower(),
                    pokeapi_id=type_info.get("pokeapi_id"),
                )
                self.db.add(type_record)
                self.db.flush()

            pokemon_type = PokemonType(
                pokemon_id=pokemon.id,
                type_id=type_record.id,
                slot=type_info["slot"],
            )
            self.db.add(pokemon_type)

        for ability_info in abilities_data:
            ability = (
                self.db.query(Ability)
                .filter(Ability.name == ability_info["name"].lower())
                .first()
            )
            if not ability:
                ability = Ability(
                    name=ability_info["name"].lower(),
                    pokeapi_id=ability_info.get("pokeapi_id"),
                    description=ability_info.get("description"),
                    is_hidden=ability_info.get("is_hidden", False),
                )
                self.db.add(ability)
                self.db.flush()

            pokemon_ability = PokemonAbility(
                pokemon_id=pokemon.id,
                ability_id=ability.id,
                slot=ability_info["slot"],
                is_hidden=ability_info.get("is_hidden", False),
            )
            self.db.add(pokemon_ability)

        self.db.commit()
        self.db.refresh(pokemon)
        return pokemon

    def update(self, pokemon_id: int, update_data: Dict[str, Any]) -> Optional[Pokemon]:
        pokemon = self.get_by_id(pokemon_id)
        if not pokemon:
            return None

        for key, value in update_data.items():
            setattr(pokemon, key, value)

        self.db.commit()
        self.db.refresh(pokemon)
        return pokemon

    def delete(self, pokemon_id: int) -> bool:
        pokemon = self.get_by_id(pokemon_id)
        if not pokemon:
            return False

        self.db.delete(pokemon)
        self.db.commit()
        return True

    def count(self) -> int:
        return self.db.query(Pokemon).count()
