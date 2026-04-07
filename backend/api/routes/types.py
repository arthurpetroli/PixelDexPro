from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Type
from services.type_effectiveness import TYPE_CHART, TYPE_COLORS, ALL_TYPES
from schemas import TypeResponse, TypeChartResponse

router = APIRouter(prefix="/types", tags=["Types"])


@router.get("", response_model=list[TypeResponse])
def list_types(db: Session = Depends(get_db)):
    """List all Pokémon types."""
    types = db.query(Type).order_by(Type.name).all()

    # If no types in DB, return from type chart
    if not types:
        return [
            TypeResponse(
                id=i,
                name=t,
                pokeapi_id=None,
                color=TYPE_COLORS.get(t),
            )
            for i, t in enumerate(ALL_TYPES, 1)
        ]

    return [
        TypeResponse(
            id=t.id,
            name=t.name,
            pokeapi_id=t.pokeapi_id,
            color=t.color or TYPE_COLORS.get(t.name),
        )
        for t in types
    ]


@router.get("/chart", response_model=TypeChartResponse)
def get_type_chart():
    """Get the full type effectiveness chart."""
    return TypeChartResponse(
        chart=TYPE_CHART,
        types=ALL_TYPES,
    )


@router.get("/colors")
def get_type_colors():
    """Get type color mappings."""
    return TYPE_COLORS
