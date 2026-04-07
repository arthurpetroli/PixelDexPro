from typing import Optional, List
from sqlalchemy.orm import Session
from models import Team, TeamPokemon, Pokemon


class TeamRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, team_id: int) -> Optional[Team]:
        return self.db.query(Team).filter(Team.id == team_id).first()

    def list_by_user(
        self, user_id: Optional[int] = None, skip: int = 0, limit: int = 50
    ) -> List[Team]:
        query = self.db.query(Team)
        if user_id:
            query = query.filter(Team.user_id == user_id)
        return query.offset(skip).limit(limit).all()

    def create(self, team_data: dict, user_id: Optional[int] = None) -> Team:
        team = Team(**team_data, user_id=user_id)
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team

    def add_pokemon(
        self, team_id: int, pokemon_id: int, slot: int, **kwargs
    ) -> Optional[TeamPokemon]:
        team = self.get_by_id(team_id)
        if not team:
            return None

        existing_count = (
            self.db.query(TeamPokemon).filter(TeamPokemon.team_id == team_id).count()
        )
        if existing_count >= 6:
            raise ValueError("Team is full (max 6 Pokemon)")

        existing = (
            self.db.query(TeamPokemon)
            .filter(
                TeamPokemon.team_id == team_id,
                TeamPokemon.pokemon_id == pokemon_id,
            )
            .first()
        )
        if existing:
            raise ValueError("Pokemon already in team")

        team_pokemon = TeamPokemon(
            team_id=team_id,
            pokemon_id=pokemon_id,
            slot=slot,
            **kwargs,
        )
        self.db.add(team_pokemon)
        self.db.commit()
        self.db.refresh(team_pokemon)
        return team_pokemon

    def remove_pokemon(self, team_id: int, pokemon_id: int) -> bool:
        team_pokemon = (
            self.db.query(TeamPokemon)
            .filter(
                TeamPokemon.team_id == team_id,
                TeamPokemon.pokemon_id == pokemon_id,
            )
            .first()
        )

        if not team_pokemon:
            return False

        self.db.delete(team_pokemon)
        self.db.commit()
        return True

    def delete(self, team_id: int) -> bool:
        team = self.get_by_id(team_id)
        if not team:
            return False

        self.db.delete(team)
        self.db.commit()
        return True
