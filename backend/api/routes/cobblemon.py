from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from db import get_db
from services.cobblemon_service import CobblemonService
from services.google_sheets_service import GoogleSheetsService
from schemas import SpawnResponse, SpawnListResponse

router = APIRouter(prefix="/cobblemon", tags=["Cobblemon"])
sheets_service = GoogleSheetsService()


@router.get("/spawns", response_model=SpawnListResponse)
def list_spawns(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    pokemon: Optional[str] = None,
    biome: Optional[str] = None,
    time: Optional[str] = None,
    weather: Optional[str] = None,
    min_level: Optional[int] = None,
    max_level: Optional[int] = None,
    context: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Search spawns with optional filters."""
    service = CobblemonService(db)
    return service.search_spawns(
        pokemon_name=pokemon,
        biome=biome,
        time=time,
        weather=weather,
        min_level=min_level,
        max_level=max_level,
        context=context,
        page=page,
        page_size=page_size,
    )


@router.get("/spawns/{pokemon_id}", response_model=list[SpawnResponse])
def get_pokemon_spawns(
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    """Get all spawn entries for a specific Pokémon."""
    service = CobblemonService(db)
    return service.get_spawns_by_pokemon(pokemon_id)


@router.get("/biomes", response_model=list[str])
def get_biomes(db: Session = Depends(get_db)):
    """Get all unique biomes from spawn data."""
    service = CobblemonService(db)
    return service.get_all_biomes()


@router.get("/times", response_model=list[str])
def get_spawn_times():
    """Get all possible spawn times."""
    return ["any", "day", "night", "dawn", "dusk"]


@router.get("/weathers", response_model=list[str])
def get_spawn_weathers():
    """Get all possible weather conditions."""
    return ["any", "clear", "rain", "thunder", "snow"]


@router.get("/contexts", response_model=list[str])
def get_spawn_contexts():
    """Get all possible spawn contexts."""
    return ["grounded", "submerged", "surface", "seafloor"]


@router.get("/sheets/biomes", response_model=List[str])
async def get_biomes_from_sheets():
    """Get all unique biomes directly from Google Sheets."""
    try:
        biomes = await sheets_service.get_unique_biomes()
        return biomes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching biomes from Google Sheets: {str(e)}",
        )


@router.get("/sheets/spawns", response_model=List[Dict[str, Any]])
async def get_spawns_from_sheets(
    pokemon: Optional[str] = Query(None, description="Filter by Pokémon name"),
    biome: Optional[str] = Query(None, description="Filter by biome"),
):
    """Get spawn data directly from Google Sheets with optional filters."""
    try:
        if pokemon:
            spawns = await sheets_service.get_spawns_by_pokemon(pokemon)
        elif biome:
            spawns = await sheets_service.get_spawns_by_biome(biome)
        else:
            spawns = await sheets_service.fetch_spawn_data()

        return spawns
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching spawns from Google Sheets: {str(e)}",
        )
