from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from repositories import FavoriteRepository, PokemonRepository
from services.pokemon_service import PokemonService
from schemas import FavoriteResponse, PokemonListItem

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.get("", response_model=list[FavoriteResponse])
def list_favorites(
    db: Session = Depends(get_db),
):
    """List all favorites (for anonymous user)."""
    repo = FavoriteRepository(db)
    service = PokemonService(db)
    favorites = repo.list_by_user(user_id=None)

    result = []
    for fav in favorites:
        pokemon = service.get_pokemon_by_id(fav.pokemon_id)
        if pokemon:
            result.append(
                FavoriteResponse(
                    id=fav.id,
                    pokemon_id=fav.pokemon_id,
                    pokemon=PokemonListItem(
                        id=pokemon.id,
                        pokeapi_id=pokemon.pokeapi_id,
                        name=pokemon.name,
                        pokedex_number=pokemon.pokedex_number,
                        sprite_url=pokemon.sprite_url,
                        types=pokemon.types,
                        generation=pokemon.generation,
                    ),
                    created_at=fav.created_at,
                )
            )

    return result


@router.post("/{pokemon_id}", response_model=FavoriteResponse)
def add_favorite(
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    """Add a Pokémon to favorites."""
    # Check if Pokémon exists
    pokemon_repo = PokemonRepository(db)
    pokemon = pokemon_repo.get_by_id(pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon not found")

    repo = FavoriteRepository(db)
    favorite = repo.add(user_id=None, pokemon_id=pokemon_id)

    service = PokemonService(db)
    pokemon_response = service.get_pokemon_by_id(pokemon_id)

    return FavoriteResponse(
        id=favorite.id,
        pokemon_id=favorite.pokemon_id,
        pokemon=PokemonListItem(
            id=pokemon_response.id,
            pokeapi_id=pokemon_response.pokeapi_id,
            name=pokemon_response.name,
            pokedex_number=pokemon_response.pokedex_number,
            sprite_url=pokemon_response.sprite_url,
            types=pokemon_response.types,
            generation=pokemon_response.generation,
        ),
        created_at=favorite.created_at,
    )


@router.delete("/{pokemon_id}")
def remove_favorite(
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    """Remove a Pokémon from favorites."""
    repo = FavoriteRepository(db)
    if not repo.remove(user_id=None, pokemon_id=pokemon_id):
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"status": "success", "message": "Removed from favorites"}


@router.get("/{pokemon_id}/check")
def check_favorite(
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    """Check if a Pokémon is favorited."""
    repo = FavoriteRepository(db)
    is_favorite = repo.is_favorite(user_id=None, pokemon_id=pokemon_id)
    return {"is_favorite": is_favorite}
