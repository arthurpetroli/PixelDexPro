from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from db import get_db
from services.pokemon_service import PokemonService
from schemas import (
    PokemonResponse,
    PokemonListResponse,
    PokemonDetailsResponse,
    PokemonListItem,
)

router = APIRouter(prefix="/pokemon", tags=["Pokemon"])


@router.get("", response_model=PokemonListResponse)
def list_pokemon(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    type: Optional[str] = None,
    generation: Optional[int] = None,
    search: Optional[str] = None,
    pokemon_pool: str = Query("all", pattern="^(all|pixelmon)$"),
    db: Session = Depends(get_db),
):
    """List Pokémon with optional filters and pagination."""
    service = PokemonService(db)
    return service.list_pokemon(
        page=page,
        page_size=page_size,
        type_filter=type,
        generation=generation,
        search=search,
        pokemon_pool=pokemon_pool,
    )


@router.get("/search", response_model=list[PokemonListItem])
def search_pokemon(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Search Pokémon by name."""
    service = PokemonService(db)
    return service.search_pokemon(query=q, limit=limit)


@router.get("/{pokemon_id}", response_model=PokemonResponse)
def get_pokemon(
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    """Get a Pokémon by ID."""
    service = PokemonService(db)
    pokemon = service.get_pokemon_by_id(pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemon


@router.get("/{pokemon_id}/details", response_model=PokemonDetailsResponse)
def get_pokemon_details(
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    """Get detailed Pokémon info including type effectiveness and spawns."""
    service = PokemonService(db)
    details = service.get_pokemon_details(pokemon_id)
    if not details:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return details


@router.get("/name/{name}", response_model=PokemonResponse)
def get_pokemon_by_name(
    name: str,
    db: Session = Depends(get_db),
):
    """Get a Pokémon by name."""
    service = PokemonService(db)
    pokemon = service.get_pokemon_by_name(name.lower())
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemon
