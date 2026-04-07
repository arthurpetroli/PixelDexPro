from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import get_db
from services.sync_service import SyncService
from schemas import SyncStatus

router = APIRouter(prefix="/sync", tags=["Sync"])


class SpawnSyncRequest(BaseModel):
    sheet_url: str
    version: str = "1.0"


@router.post("/pokeapi/pokemon/{name_or_id}", response_model=SyncStatus)
async def sync_pokemon(
    name_or_id: str,
    db: Session = Depends(get_db),
):
    """Sync a single Pokémon from PokéAPI."""
    service = SyncService(db)
    return await service.sync_pokemon(name_or_id)


@router.post("/pokeapi/pokemon", response_model=SyncStatus)
async def sync_pokemon_batch(
    limit: int = Query(151, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Sync multiple Pokémon from PokéAPI."""
    service = SyncService(db)
    return await service.sync_pokemon_batch(limit=limit, offset=offset)


@router.post("/pokeapi/types", response_model=SyncStatus)
async def sync_types(
    db: Session = Depends(get_db),
):
    """Sync all types from PokéAPI."""
    service = SyncService(db)
    return await service.sync_types()


@router.post("/cobblemon/spawns", response_model=SyncStatus)
async def sync_cobblemon_spawns(
    request: SpawnSyncRequest,
    db: Session = Depends(get_db),
):
    """Sync Cobblemon spawn data from a Google Sheet."""
    service = SyncService(db)
    return await service.sync_cobblemon_spawns(
        sheet_url=request.sheet_url,
        version=request.version,
    )
