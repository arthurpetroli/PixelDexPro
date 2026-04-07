from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_db
from services.compare_service import CompareService
from schemas import CompareResponse

router = APIRouter(prefix="/compare", tags=["Compare"])


@router.get("", response_model=CompareResponse)
def compare_pokemon(
    pokemon1: int = Query(..., description="First Pokémon ID"),
    pokemon2: int = Query(..., description="Second Pokémon ID"),
    db: Session = Depends(get_db),
):
    """Compare two Pokémon side by side."""
    if pokemon1 == pokemon2:
        raise HTTPException(
            status_code=400, detail="Cannot compare a Pokémon with itself"
        )

    service = CompareService(db)
    result = service.compare_pokemon(pokemon1, pokemon2)

    if not result:
        raise HTTPException(status_code=404, detail="One or both Pokémon not found")

    return result
