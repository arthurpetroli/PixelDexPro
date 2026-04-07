from typing import Optional, List
from sqlalchemy.orm import Session
from models import Favorite, Pokemon, User


class FavoriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, favorite_id: int) -> Optional[Favorite]:
        return self.db.query(Favorite).filter(Favorite.id == favorite_id).first()

    def list_by_user(self, user_id: Optional[int] = None) -> List[Favorite]:
        query = self.db.query(Favorite)
        if user_id:
            query = query.filter(Favorite.user_id == user_id)
        return query.order_by(Favorite.created_at.desc()).all()

    def add(self, user_id: Optional[int], pokemon_id: int) -> Optional[Favorite]:
        existing = (
            self.db.query(Favorite)
            .filter(
                Favorite.user_id == user_id,
                Favorite.pokemon_id == pokemon_id,
            )
            .first()
        )

        if existing:
            return existing

        favorite = Favorite(user_id=user_id, pokemon_id=pokemon_id)
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def remove(self, user_id: Optional[int], pokemon_id: int) -> bool:
        favorite = (
            self.db.query(Favorite)
            .filter(
                Favorite.user_id == user_id,
                Favorite.pokemon_id == pokemon_id,
            )
            .first()
        )

        if not favorite:
            return False

        self.db.delete(favorite)
        self.db.commit()
        return True

    def is_favorite(self, user_id: Optional[int], pokemon_id: int) -> bool:
        return (
            self.db.query(Favorite)
            .filter(
                Favorite.user_id == user_id,
                Favorite.pokemon_id == pokemon_id,
            )
            .first()
            is not None
        )
