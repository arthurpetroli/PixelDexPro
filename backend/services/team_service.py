from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from repositories import TeamRepository, PokemonRepository
from models import Team, TeamPokemon, Pokemon
from services.type_effectiveness import (
    calculate_team_coverage,
    calculate_type_effectiveness,
    get_weaknesses,
)
from schemas import TeamResponse, TeamPokemonResponse, TeamAnalysis, TeamBase


class TeamService:
    """Service for team building and analysis."""

    def __init__(self, db: Session):
        self.db = db
        self.team_repo = TeamRepository(db)
        self.pokemon_repo = PokemonRepository(db)

    def _team_to_response(self, team: Team) -> TeamResponse:
        """Convert a Team model to a response schema."""
        team_pokemon = []
        for tp in sorted(team.team_pokemon, key=lambda x: x.slot):
            team_pokemon.append(
                TeamPokemonResponse(
                    id=tp.id,
                    team_id=tp.team_id,
                    pokemon_id=tp.pokemon_id,
                    slot=tp.slot,
                    nickname=tp.nickname,
                    level=tp.level,
                    ability=tp.ability,
                    nature=tp.nature,
                    held_item=tp.held_item,
                    moves=tp.moves or [],
                )
            )

        return TeamResponse(
            id=team.id,
            name=team.name,
            description=team.description,
            is_public=team.is_public,
            team_pokemon=team_pokemon,
            created_at=team.created_at,
            updated_at=team.updated_at,
        )

    def create_team(
        self, team_data: TeamBase, user_id: Optional[int] = None
    ) -> TeamResponse:
        """Create a new team."""
        team = self.team_repo.create(team_data.model_dump(), user_id)
        return self._team_to_response(team)

    def get_team(self, team_id: int) -> Optional[TeamResponse]:
        """Get a team by ID."""
        team = self.team_repo.get_by_id(team_id)
        if not team:
            return None
        return self._team_to_response(team)

    def add_pokemon_to_team(
        self,
        team_id: int,
        pokemon_id: int,
        slot: int,
        nickname: Optional[str] = None,
        level: int = 50,
    ) -> Optional[TeamPokemonResponse]:
        """Add a Pokémon to a team."""
        try:
            team_pokemon = self.team_repo.add_pokemon(
                team_id=team_id,
                pokemon_id=pokemon_id,
                slot=slot,
                nickname=nickname,
                level=level,
            )
            if not team_pokemon:
                return None

            return TeamPokemonResponse(
                id=team_pokemon.id,
                team_id=team_pokemon.team_id,
                pokemon_id=team_pokemon.pokemon_id,
                slot=team_pokemon.slot,
                nickname=team_pokemon.nickname,
                level=team_pokemon.level,
                ability=team_pokemon.ability,
                nature=team_pokemon.nature,
                held_item=team_pokemon.held_item,
                moves=team_pokemon.moves or [],
            )
        except ValueError:
            return None

    def remove_pokemon_from_team(self, team_id: int, pokemon_id: int) -> bool:
        """Remove a Pokémon from a team."""
        return self.team_repo.remove_pokemon(team_id, pokemon_id)

    def analyze_team(self, team_id: int) -> Optional[TeamAnalysis]:
        """Analyze a team's type coverage and balance."""
        team = self.team_repo.get_by_id(team_id)
        if not team:
            return None

        if not team.team_pokemon:
            return TeamAnalysis(
                team_id=team_id,
                weaknesses={},
                resistances={},
                immunities=[],
                shared_weaknesses={},
                problematic_types=[],
                role_distribution={},
                coverage_score=0.0,
                defensive_score=0.0,
                summary="Team is empty. Add Pokémon to analyze coverage.",
            )

        # Get types for each Pokémon in the team
        team_types = []
        pokemon_names = []
        for tp in team.team_pokemon:
            pokemon = self.pokemon_repo.get_by_id(tp.pokemon_id)
            if pokemon:
                types = [pt.type.name for pt in pokemon.types]
                team_types.append(types)
                pokemon_names.append(pokemon.name)

        # Calculate team coverage
        coverage = calculate_team_coverage(team_types)

        # Determine shared weaknesses by Pokémon name
        shared_weakness_pokemon: Dict[str, List[str]] = {}
        for i, types in enumerate(team_types):
            eff = calculate_type_effectiveness(types)
            weak = get_weaknesses(eff)
            for t in weak:
                if t not in shared_weakness_pokemon:
                    shared_weakness_pokemon[t] = []
                shared_weakness_pokemon[t].append(pokemon_names[i])

        # Filter to only shared (2+ Pokémon)
        shared_weaknesses = {
            t: names for t, names in shared_weakness_pokemon.items() if len(names) >= 2
        }

        # Analyze role distribution (basic heuristic based on stats)
        role_distribution = self._analyze_roles(team)

        # Calculate scores
        coverage_score = self._calculate_coverage_score(coverage)
        defensive_score = self._calculate_defensive_score(coverage)

        # Generate summary
        summary = self._generate_summary(
            coverage, shared_weaknesses, role_distribution, len(team.team_pokemon)
        )

        return TeamAnalysis(
            team_id=team_id,
            weaknesses=coverage["weaknesses"],
            resistances=coverage["resistances"],
            immunities=coverage["immunities"],
            shared_weaknesses=shared_weaknesses,
            problematic_types=coverage["problematic_types"],
            role_distribution=role_distribution,
            coverage_score=coverage_score,
            defensive_score=defensive_score,
            summary=summary,
        )

    def _analyze_roles(self, team: Team) -> Dict[str, int]:
        """Analyze the role distribution of a team based on stats."""
        roles = {
            "physical_attacker": 0,
            "special_attacker": 0,
            "physical_wall": 0,
            "special_wall": 0,
            "speedster": 0,
            "tank": 0,
        }

        for tp in team.team_pokemon:
            pokemon = self.pokemon_repo.get_by_id(tp.pokemon_id)
            if not pokemon or not pokemon.stats:
                continue

            stats = pokemon.stats

            # Determine primary role based on highest stats
            if stats.attack > stats.special_attack and stats.attack > 100:
                roles["physical_attacker"] += 1
            elif stats.special_attack > stats.attack and stats.special_attack > 100:
                roles["special_attacker"] += 1

            if stats.defense > 100:
                roles["physical_wall"] += 1
            if stats.special_defense > 100:
                roles["special_wall"] += 1
            if stats.speed > 100:
                roles["speedster"] += 1
            if stats.hp > 100:
                roles["tank"] += 1

        return {k: v for k, v in roles.items() if v > 0}

    def _calculate_coverage_score(self, coverage: Dict[str, Any]) -> float:
        """Calculate a coverage score (0-100) based on weaknesses and resistances."""
        weakness_count = len(coverage["weaknesses"])
        resistance_count = len(coverage["resistances"])
        immunity_count = len(coverage["immunities"])
        shared_count = len(coverage["shared_weaknesses"])

        # Base score
        score = 50.0

        # Penalize for weaknesses
        score -= weakness_count * 3

        # Penalize more for shared weaknesses
        score -= shared_count * 5

        # Bonus for resistances
        score += resistance_count * 2

        # Bonus for immunities
        score += immunity_count * 5

        return max(0.0, min(100.0, score))

    def _calculate_defensive_score(self, coverage: Dict[str, Any]) -> float:
        """Calculate a defensive score based on how well the team handles threats."""
        problematic_count = len(coverage["problematic_types"])
        immunity_count = len(coverage["immunities"])

        score = 70.0
        score -= problematic_count * 10
        score += immunity_count * 5

        return max(0.0, min(100.0, score))

    def _generate_summary(
        self,
        coverage: Dict[str, Any],
        shared_weaknesses: Dict[str, List[str]],
        roles: Dict[str, int],
        team_size: int,
    ) -> str:
        """Generate a human-readable summary of the team analysis."""
        parts = []

        if team_size < 6:
            parts.append(f"Team has {team_size}/6 Pokémon.")

        if shared_weaknesses:
            worst = sorted(
                shared_weaknesses.items(), key=lambda x: len(x[1]), reverse=True
            )[:3]
            weak_types = ", ".join([t for t, _ in worst])
            parts.append(
                f"Watch out for {weak_types} types - multiple team members are weak to them."
            )

        if coverage["immunities"]:
            parts.append(
                f"Team has immunities to: {', '.join(coverage['immunities'])}."
            )

        if not roles:
            parts.append(
                "Consider adding Pokémon with defined roles (attackers, walls, speedsters)."
            )
        else:
            role_summary = ", ".join(
                [f"{v} {k.replace('_', ' ')}" for k, v in roles.items()]
            )
            parts.append(f"Roles: {role_summary}.")

        return " ".join(parts) if parts else "Team looks balanced!"
