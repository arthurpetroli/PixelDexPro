from typing import List, Dict, Optional, Set, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pokemon, PokemonType
from repositories.pokemon_repository import PokemonRepository
from services.type_effectiveness import TypeEffectiveness


class TeamSuggestionService:
    """Service for AI-powered team building suggestions."""

    def __init__(self, db: Session):
        self.db = db
        self.pokemon_repo = PokemonRepository(db)
        self.type_calc = TypeEffectiveness()

    def _get_pokemon_defenses(
        self, pokemon: Pokemon
    ) -> Tuple[Dict[str, float], Dict[str, float], Set[str]]:
        """Calculate weaknesses, resistances, and immunities for a Pokemon."""
        pokemon_types = [pt.type.name for pt in pokemon.types]
        return self.type_calc.get_defensive_profile(pokemon_types)

    def suggest_team(
        self,
        strategy: str = "balanced",
        generation: Optional[int] = None,
    ) -> List[Dict]:
        """
        Suggest a complete team based on strategy.

        Strategies:
        - balanced: Good mix of types and roles
        - offensive: High attack coverage
        - defensive: Strong defensive typing
        - stall: Focus on bulk and recovery
        """
        if strategy == "balanced":
            return self._suggest_balanced_team(generation)
        elif strategy == "offensive":
            return self._suggest_offensive_team(generation)
        elif strategy == "defensive":
            return self._suggest_defensive_team(generation)
        elif strategy == "stall":
            return self._suggest_stall_team(generation)
        else:
            return self._suggest_balanced_team(generation)

    def complete_team(
        self,
        existing_pokemon_ids: List[int],
        prioritize: str = "coverage",
    ) -> List[Dict]:
        """
        Suggest Pokemon to complete a team based on weaknesses and gaps.

        Args:
            existing_pokemon_ids: IDs of Pokemon already in the team
            prioritize: What to prioritize - "coverage", "defense", or "synergy"
        """
        # Get existing team Pokemon
        existing_team = []
        for pid in existing_pokemon_ids:
            pokemon = self.pokemon_repo.get_by_id(pid)
            if pokemon:
                existing_team.append(pokemon)

        if not existing_team:
            return self.suggest_team("balanced")

        # Analyze team weaknesses
        team_analysis = self._analyze_team(existing_team)

        # Get suggestions based on gaps
        slots_needed = 6 - len(existing_team)
        if slots_needed <= 0:
            return []

        suggestions = self._find_complementary_pokemon(
            existing_team,
            team_analysis,
            slots_needed,
            prioritize,
        )

        return suggestions

    def _suggest_balanced_team(self, generation: Optional[int]) -> List[Dict]:
        """Suggest a balanced team with good type coverage and roles."""
        # Target type coverage: Try to have diverse types
        target_types = [
            "water",  # Good defensive type
            "fire",  # Offensive coverage
            "electric",  # Speed and special attack
            "grass",  # Status and support
            "steel",  # Defensive anchor
            "dragon",  # Mixed attacker
        ]

        team = []
        used_primary_types = set()

        for target_type in target_types:
            # Find strong Pokemon of this type
            candidates = self._get_pokemon_by_criteria(
                primary_type=target_type,
                generation=generation,
                exclude_ids=[p["id"] for p in team],
                min_base_stat_total=450,
            )

            if candidates:
                # Pick the best candidate based on stats
                best = max(candidates, key=lambda p: self._calculate_stat_total(p))
                team.append(self._pokemon_to_suggestion(best))
                used_primary_types.add(target_type)

        return team

    def _suggest_offensive_team(self, generation: Optional[int]) -> List[Dict]:
        """Suggest an offensive team with high attack stats."""
        # Focus on Pokemon with high attack/special attack
        candidates = self._get_pokemon_by_criteria(
            generation=generation,
            min_base_stat_total=500,
        )

        # Sort by attack power (Attack + Special Attack)
        candidates.sort(
            key=lambda p: ((p.stats.attack + p.stats.special_attack) if p.stats else 0),
            reverse=True,
        )

        # Pick top 6 with type diversity
        team = []
        used_types = set()

        for pokemon in candidates:
            if len(team) >= 6:
                break

            # Get Pokemon types
            types = {pt.type.name for pt in pokemon.types}

            # Prefer Pokemon with new types
            if not types.intersection(used_types) or len(team) < 3:
                team.append(self._pokemon_to_suggestion(pokemon))
                used_types.update(types)

        return team

    def _suggest_defensive_team(self, generation: Optional[int]) -> List[Dict]:
        """Suggest a defensive team with strong resistances."""
        # Target defensive types
        defensive_types = ["steel", "fairy", "water", "dragon", "ghost", "ground"]

        team = []
        for target_type in defensive_types:
            candidates = self._get_pokemon_by_criteria(
                primary_type=target_type,
                generation=generation,
                exclude_ids=[p["id"] for p in team],
                min_defense=80,
            )

            if candidates:
                # Pick Pokemon with highest defense + sp_def
                best = max(
                    candidates,
                    key=lambda p: (
                        (p.stats.defense + p.stats.special_defense) if p.stats else 0
                    ),
                )
                team.append(self._pokemon_to_suggestion(best))

        return team

    def _suggest_stall_team(self, generation: Optional[int]) -> List[Dict]:
        """Suggest a stall team focused on bulk."""
        candidates = self._get_pokemon_by_criteria(
            generation=generation,
            min_hp=90,
            min_defense=70,
        )

        # Sort by bulk (HP * (Def + SpDef))
        candidates.sort(
            key=lambda p: (
                (p.stats.hp * (p.stats.defense + p.stats.special_defense))
                if p.stats
                else 0
            ),
            reverse=True,
        )

        team = []
        used_types = set()

        for pokemon in candidates[:6]:
            types = {pt.type.name for pt in pokemon.types}
            if not types.intersection(used_types) or len(team) < 3:
                team.append(self._pokemon_to_suggestion(pokemon))
                used_types.update(types)

        return team[:6]

    def _analyze_team(self, team: List[Pokemon]) -> Dict:
        """Analyze team weaknesses, resistances, and coverage."""
        weaknesses: Dict[str, int] = {}
        resistances: Dict[str, int] = {}
        immunities: Set[str] = set()
        type_coverage: Set[str] = set()

        for pokemon in team:
            # Collect types
            for pt in pokemon.types:
                type_coverage.add(pt.type.name)

            # Calculate weaknesses/resistances using type calculator
            poke_weaknesses, poke_resistances, poke_immunities = (
                self._get_pokemon_defenses(pokemon)
            )

            for type_name, multiplier in poke_weaknesses.items():
                if multiplier > 1:
                    weaknesses[type_name] = weaknesses.get(type_name, 0) + 1

            for type_name, multiplier in poke_resistances.items():
                if multiplier < 1:
                    resistances[type_name] = resistances.get(type_name, 0) + 1

            immunities.update(poke_immunities)

        return {
            "weaknesses": weaknesses,
            "resistances": resistances,
            "immunities": immunities,
            "type_coverage": type_coverage,
            "problematic_weaknesses": [
                type_name for type_name, count in weaknesses.items() if count >= 3
            ],
        }

    def _find_complementary_pokemon(
        self,
        existing_team: List[Pokemon],
        analysis: Dict,
        count: int,
        prioritize: str,
    ) -> List[Dict]:
        """Find Pokemon that complement the existing team."""
        suggestions = []
        problematic_weaknesses = analysis["problematic_weaknesses"]
        existing_coverage = analysis["type_coverage"]

        # Get all viable Pokemon
        existing_ids = [p.id for p in existing_team]
        candidates = self._get_pokemon_by_criteria(
            exclude_ids=existing_ids,
            min_base_stat_total=400,
        )

        # Score each candidate
        scored_candidates = []
        for pokemon in candidates:
            score = self._score_team_fit(
                pokemon,
                existing_team,
                analysis,
                prioritize,
            )
            scored_candidates.append((score, pokemon))

        # Sort by score and take top N
        scored_candidates.sort(reverse=True, key=lambda x: x[0])

        for score, pokemon in scored_candidates[:count]:
            suggestions.append(
                {
                    **self._pokemon_to_suggestion(pokemon),
                    "fit_score": round(score, 2),
                    "reason": self._explain_suggestion(pokemon, analysis),
                }
            )

        return suggestions

    def _score_team_fit(
        self,
        pokemon: Pokemon,
        existing_team: List[Pokemon],
        analysis: Dict,
        prioritize: str,
    ) -> float:
        """Score how well a Pokemon fits the team."""
        score = 0.0

        # Get Pokemon types
        pokemon_types = {pt.type.name for pt in pokemon.types}

        # Calculate this Pokemon's defenses
        poke_weaknesses, poke_resistances, poke_immunities = self._get_pokemon_defenses(
            pokemon
        )

        # Check resistance to problematic weaknesses
        for weak_type in analysis["problematic_weaknesses"]:
            if weak_type in poke_resistances:
                mult = poke_resistances[weak_type]
                if mult <= 0.5:
                    score += 15.0  # Resists problematic weakness
                elif mult < 1.0:
                    score += 8.0

        # Check immunities to weaknesses
        for weak_type in analysis["problematic_weaknesses"]:
            if weak_type in poke_immunities:
                score += 20.0  # Immune to problematic weakness

        # Type diversity bonus
        new_types = pokemon_types - analysis["type_coverage"]
        score += len(new_types) * 5.0

        # Stats bonus based on prioritization
        if prioritize == "coverage":
            # Favor offensive Pokemon with diverse moves
            if pokemon.stats:
                score += pokemon.stats.attack * 0.1 + pokemon.stats.special_attack * 0.1
        elif prioritize == "defense":
            # Favor defensive Pokemon
            if pokemon.stats:
                score += (
                    pokemon.stats.defense * 0.1
                    + pokemon.stats.special_defense * 0.1
                    + pokemon.stats.hp * 0.15
                )
        else:  # synergy
            # Balanced scoring
            stat_total = self._calculate_stat_total(pokemon)
            score += stat_total * 0.02

        return score

    def _explain_suggestion(self, pokemon: Pokemon, analysis: Dict) -> str:
        """Generate explanation for why this Pokemon is suggested."""
        reasons = []

        # Calculate this Pokemon's defenses
        poke_weaknesses, poke_resistances, poke_immunities = self._get_pokemon_defenses(
            pokemon
        )

        # Check for resistances to weaknesses
        resisted = [
            t for t in analysis["problematic_weaknesses"] if t in poke_resistances
        ]
        if resisted:
            reasons.append(f"Resists team's {', '.join(resisted)} weakness")

        # Check for immunities
        immune_to_weaknesses = poke_immunities.intersection(
            set(analysis["problematic_weaknesses"])
        )
        if immune_to_weaknesses:
            reasons.append(f"Immune to {', '.join(immune_to_weaknesses)}")

        # Check for new type coverage
        pokemon_types = {pt.type.name for pt in pokemon.types}
        new_types = pokemon_types - analysis["type_coverage"]
        if new_types:
            reasons.append(f"Adds {', '.join(new_types)} coverage")

        # Check stats
        stat_total = self._calculate_stat_total(pokemon)
        if stat_total >= 520:
            reasons.append("Strong stats")

        return " • ".join(reasons) if reasons else "Balanced addition to team"

    def _get_pokemon_by_criteria(
        self,
        primary_type: Optional[str] = None,
        generation: Optional[int] = None,
        exclude_ids: Optional[List[int]] = None,
        min_base_stat_total: Optional[int] = None,
        min_hp: Optional[int] = None,
        min_defense: Optional[int] = None,
    ) -> List[Pokemon]:
        """Get Pokemon matching specific criteria."""
        query = self.db.query(Pokemon)

        if primary_type:
            query = (
                query.join(PokemonType, Pokemon.id == PokemonType.pokemon_id)
                .join(PokemonType.type)
                .filter(
                    PokemonType.type.has(name=primary_type),
                    PokemonType.slot == 1,
                )
            )

        if generation:
            query = query.filter(Pokemon.generation == generation)

        if exclude_ids:
            query = query.filter(Pokemon.id.notin_(exclude_ids))

        results = query.all()

        # Filter by stats if needed
        if min_base_stat_total or min_hp or min_defense:
            filtered = []
            for pokemon in results:
                if pokemon.stats:
                    if min_base_stat_total:
                        total = self._calculate_stat_total(pokemon)
                        if total < min_base_stat_total:
                            continue
                    if min_hp and pokemon.stats.hp < min_hp:
                        continue
                    if min_defense and pokemon.stats.defense < min_defense:
                        continue
                    filtered.append(pokemon)
            return filtered

        return results

    def _calculate_stat_total(self, pokemon: Pokemon) -> int:
        """Calculate total base stats."""
        if not pokemon.stats:
            return 0
        return pokemon.stats.total or (
            pokemon.stats.hp
            + pokemon.stats.attack
            + pokemon.stats.defense
            + pokemon.stats.special_attack
            + pokemon.stats.special_defense
            + pokemon.stats.speed
        )

    def _pokemon_to_suggestion(self, pokemon: Pokemon) -> Dict:
        """Convert Pokemon model to suggestion dict."""
        stats_dict = None
        if pokemon.stats:
            stats_dict = {
                "hp": pokemon.stats.hp,
                "attack": pokemon.stats.attack,
                "defense": pokemon.stats.defense,
                "special_attack": pokemon.stats.special_attack,
                "special_defense": pokemon.stats.special_defense,
                "speed": pokemon.stats.speed,
            }

        return {
            "id": pokemon.id,
            "name": pokemon.name,
            "pokedex_number": pokemon.pokedex_number,
            "sprite_url": pokemon.sprite_url,
            "types": [{"name": pt.type.name, "slot": pt.slot} for pt in pokemon.types],
            "stats": stats_dict,
            "stat_total": self._calculate_stat_total(pokemon),
        }
