from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from db import get_db
from services.team_service import TeamService
from services.team_suggestion_service import TeamSuggestionService
from schemas import TeamResponse, TeamPokemonResponse, TeamAnalysis, TeamBase

router = APIRouter(prefix="/teams", tags=["Teams"])


class AddPokemonRequest(BaseModel):
    pokemon_id: int
    slot: int
    nickname: Optional[str] = None
    level: int = 50


@router.post("", response_model=TeamResponse)
def create_team(
    team: TeamBase,
    db: Session = Depends(get_db),
):
    """Create a new team."""
    service = TeamService(db)
    return service.create_team(team)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
):
    """Get a team by ID."""
    service = TeamService(db)
    team = service.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.post("/{team_id}/pokemon", response_model=TeamPokemonResponse)
def add_pokemon_to_team(
    team_id: int,
    request: AddPokemonRequest,
    db: Session = Depends(get_db),
):
    """Add a Pokémon to a team."""
    service = TeamService(db)
    result = service.add_pokemon_to_team(
        team_id=team_id,
        pokemon_id=request.pokemon_id,
        slot=request.slot,
        nickname=request.nickname,
        level=request.level,
    )
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Failed to add Pokémon. Team may be full or Pokémon already in team.",
        )
    return result


@router.delete("/{team_id}/pokemon/{pokemon_id}")
def remove_pokemon_from_team(
    team_id: int,
    pokemon_id: int,
    db: Session = Depends(get_db),
):
    """Remove a Pokémon from a team."""
    service = TeamService(db)
    if not service.remove_pokemon_from_team(team_id, pokemon_id):
        raise HTTPException(status_code=404, detail="Pokémon not found in team")
    return {"status": "success", "message": "Pokémon removed from team"}


@router.get("/{team_id}/analysis", response_model=TeamAnalysis)
def analyze_team(
    team_id: int,
    db: Session = Depends(get_db),
):
    """Get a detailed analysis of a team's coverage and balance."""
    service = TeamService(db)
    analysis = service.analyze_team(team_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Team not found")
    return analysis


@router.get("/suggest/complete")
def suggest_complete_team(
    strategy: str = Query(
        "balanced", description="Team strategy: balanced, offensive, defensive, stall"
    ),
    generation: Optional[int] = Query(None, description="Limit to specific generation"),
    db: Session = Depends(get_db),
):
    """Get AI-generated team suggestions based on strategy."""
    service = TeamSuggestionService(db)
    suggestions = service.suggest_team(
        strategy=strategy,
        generation=generation,
    )
    return {
        "strategy": strategy,
        "suggestions": suggestions,
        "count": len(suggestions),
    }


class CompleteTeamRequest(BaseModel):
    pokemon_ids: List[int]
    prioritize: str = "coverage"  # coverage, defense, or synergy


@router.post("/suggest/autocomplete")
def autocomplete_team(
    request: CompleteTeamRequest,
    db: Session = Depends(get_db),
):
    """Get suggestions to complete an existing team based on weaknesses and gaps."""
    service = TeamSuggestionService(db)
    suggestions = service.complete_team(
        existing_pokemon_ids=request.pokemon_ids,
        prioritize=request.prioritize,
    )
    return {
        "existing_count": len(request.pokemon_ids),
        "suggestions": suggestions,
        "prioritize": request.prioritize,
    }
