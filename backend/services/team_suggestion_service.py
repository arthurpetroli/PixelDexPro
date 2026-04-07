from typing import List, Dict, Optional, Set, Tuple
from sqlalchemy.orm import Session
from models import Pokemon, PokemonType
from repositories.pokemon_repository import PokemonRepository
from services.type_effectiveness import TypeEffectiveness


class TeamSuggestionService:
    """Service for AI-powered team building suggestions."""

    VALID_LEGENDARY_FILTERS = {
        "all",
        "include",
        "exclude",
        "legendaries",
        "non-legendaries",
    }

    LEGENDARY_KEYWORDS = [
        "legend",
        "mythical",
        "ultra beast",
        "sub-legendary",
    ]

    LEGENDARY_BASE_NAMES = {
        "articuno",
        "zapdos",
        "moltres",
        "mewtwo",
        "mew",
        "raikou",
        "entei",
        "suicune",
        "lugia",
        "ho-oh",
        "celebi",
        "regirock",
        "regice",
        "registeel",
        "latias",
        "latios",
        "kyogre",
        "groudon",
        "rayquaza",
        "jirachi",
        "deoxys",
        "uxie",
        "mesprit",
        "azelf",
        "dialga",
        "palkia",
        "heatran",
        "regigigas",
        "giratina",
        "cresselia",
        "phione",
        "manaphy",
        "darkrai",
        "shaymin",
        "arceus",
        "victini",
        "cobalion",
        "terrakion",
        "virizion",
        "tornadus",
        "thundurus",
        "reshiram",
        "zekrom",
        "landorus",
        "kyurem",
        "keldeo",
        "meloetta",
        "genesect",
        "xerneas",
        "yveltal",
        "zygarde",
        "diancie",
        "hoopa",
        "volcanion",
        "tapu-koko",
        "tapu-lele",
        "tapu-bulu",
        "tapu-fini",
        "cosmog",
        "cosmoem",
        "solgaleo",
        "lunala",
        "nihilego",
        "buzzwole",
        "pheromosa",
        "xurkitree",
        "celesteela",
        "kartana",
        "guzzlord",
        "necrozma",
        "magearna",
        "marshadow",
        "poipole",
        "naganadel",
        "stakataka",
        "blacephalon",
        "zeraora",
        "meltan",
        "melmetal",
        "zacian",
        "zamazenta",
        "eternatus",
        "kubfu",
        "urshifu",
        "zarude",
        "regieleki",
        "regidrago",
        "glastrier",
        "spectrier",
        "calyrex",
        "enamorus",
        "wo-chien",
        "chien-pao",
        "ting-lu",
        "chi-yu",
        "koraidon",
        "miraidon",
        "walking-wake",
        "iron-leaves",
        "okidogi",
        "munkidori",
        "fezandipiti",
        "ogerpon",
        "terapagos",
        "pecharunt",
        "gouging-fire",
        "raging-bolt",
        "iron-boulder",
        "iron-crown",
    }

    FORM_SUFFIX_TOKENS = {
        "attack",
        "defense",
        "speed",
        "normal",
        "origin",
        "altered",
        "sky",
        "incarnate",
        "therian",
        "white",
        "black",
        "resolute",
        "blade",
        "shield",
        "ordinary",
        "aria",
        "pirouette",
        "dawn",
        "dusk",
        "midday",
        "midnight",
        "complete",
        "10",
        "50",
        "school",
        "busted",
        "disguised",
        "noice",
        "hangry",
        "hero",
        "crowned",
        "sword",
        "shield",
        "eternamax",
        "gmax",
        "mega",
        "x",
        "y",
        "alola",
        "galar",
        "hisui",
        "paldea",
    }

    LEGENDARY_LIKE_POKEDEX_NUMBERS = {
        144,
        145,
        146,
        150,
        151,
        243,
        244,
        245,
        249,
        250,
        251,
        377,
        378,
        379,
        380,
        381,
        382,
        383,
        384,
        385,
        386,
        480,
        481,
        482,
        483,
        484,
        485,
        486,
        487,
        488,
        489,
        490,
        491,
        492,
        493,
        494,
        638,
        639,
        640,
        641,
        642,
        643,
        644,
        645,
        646,
        647,
        648,
        649,
        716,
        717,
        718,
        719,
        720,
        721,
        785,
        786,
        787,
        788,
        789,
        790,
        791,
        792,
        793,
        794,
        795,
        796,
        797,
        798,
        799,
        800,
        801,
        802,
        803,
        804,
        805,
        806,
        807,
        808,
        809,
        888,
        889,
        890,
        891,
        892,
        893,
        894,
        895,
        896,
        897,
        898,
        905,
        1001,
        1002,
        1003,
        1004,
        1007,
        1008,
        1009,
        1010,
        1014,
        1015,
        1016,
        1017,
        1024,
        1025,
    }

    def __init__(self, db: Session):
        self.db = db
        self.pokemon_repo = PokemonRepository(db)
        self.type_calc = TypeEffectiveness()
        self._legendary_by_name_cache: Dict[str, bool] = {}

    def _resolve_filter_mode(
        self, include_legendaries: bool, legendary_filter: str
    ) -> str:
        """Normalize and resolve legendary filter mode."""
        normalized_filter = (legendary_filter or "all").strip().lower()
        if normalized_filter not in self.VALID_LEGENDARY_FILTERS:
            normalized_filter = "all"

        if normalized_filter == "all":
            return "include" if include_legendaries else "exclude"

        return normalized_filter

    def _is_legendary_by_fields(self, pokemon: Pokemon) -> bool:
        """Check legendary status using direct pokemon fields."""
        dex_number = pokemon.pokedex_number or pokemon.pokeapi_id
        if dex_number in self.LEGENDARY_LIKE_POKEDEX_NUMBERS:
            return True

        if not pokemon.category:
            return False

        category_lower = pokemon.category.lower()
        return any(keyword in category_lower for keyword in self.LEGENDARY_KEYWORDS)

    def _get_name_base_candidates(self, pokemon_name: str) -> List[str]:
        """Generate possible base names for form variants."""
        name = (pokemon_name or "").strip().lower()
        if not name:
            return []

        parts = name.split("-")
        candidates = [name]

        while len(parts) > 1:
            last = parts[-1]
            if last in self.FORM_SUFFIX_TOKENS or last.isdigit():
                parts = parts[:-1]
                candidate = "-".join(parts)
                if candidate and candidate not in candidates:
                    candidates.append(candidate)
            else:
                break

        # Fallback: aggressively strip suffixes for unknown form names
        fallback_parts = name.split("-")
        while len(fallback_parts) > 1:
            fallback_parts = fallback_parts[:-1]
            candidate = "-".join(fallback_parts)
            if candidate and candidate not in candidates:
                candidates.append(candidate)

        return candidates

    def _is_legendary(self, pokemon: Pokemon) -> bool:
        """Check if a Pokemon should be treated as legendary/mythical."""
        if self._is_legendary_by_fields(pokemon):
            return True

        name = (pokemon.name or "").strip().lower()
        if not name:
            return False

        cached = self._legendary_by_name_cache.get(name)
        if cached is not None:
            return cached

        base_candidates = self._get_name_base_candidates(name)
        if any(candidate in self.LEGENDARY_BASE_NAMES for candidate in base_candidates):
            self._legendary_by_name_cache[name] = True
            return True

        for candidate_name in base_candidates[1:]:
            cached_candidate = self._legendary_by_name_cache.get(candidate_name)
            if cached_candidate is not None and cached_candidate:
                self._legendary_by_name_cache[name] = True
                return True

            base_pokemon = (
                self.db.query(Pokemon)
                .filter(Pokemon.name == candidate_name)
                .order_by(Pokemon.is_default.desc())
                .first()
            )
            if base_pokemon and self._is_legendary_by_fields(base_pokemon):
                self._legendary_by_name_cache[candidate_name] = True
                self._legendary_by_name_cache[name] = True
                return True

        self._legendary_by_name_cache[name] = False
        return False

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
        include_legendaries: bool = True,
        legendary_filter: str = "all",
        pokemon_pool: str = "all",
    ) -> List[Dict]:
        """
        Suggest a complete team based on strategy.

        Strategies:
        - balanced: Good mix of types and roles
        - offensive: High attack coverage
        - defensive: Strong defensive typing
        - stall: Focus on bulk and recovery

        Args:
            include_legendaries: Whether to include legendary Pokemon
            legendary_filter: Filter mode - "all", "legendaries", "non-legendaries"
            pokemon_pool: Pokemon source pool - "all" or "pixelmon"
        """
        filter_mode = self._resolve_filter_mode(include_legendaries, legendary_filter)

        if strategy == "balanced":
            return self._suggest_balanced_team(generation, filter_mode, pokemon_pool)
        elif strategy == "offensive":
            return self._suggest_offensive_team(generation, filter_mode, pokemon_pool)
        elif strategy == "defensive":
            return self._suggest_defensive_team(generation, filter_mode, pokemon_pool)
        elif strategy == "stall":
            return self._suggest_stall_team(generation, filter_mode, pokemon_pool)
        else:
            return self._suggest_balanced_team(generation, filter_mode, pokemon_pool)

    def complete_team(
        self,
        existing_pokemon_ids: List[int],
        prioritize: str = "coverage",
        include_legendaries: bool = True,
        legendary_filter: str = "all",
        pokemon_pool: str = "all",
    ) -> List[Dict]:
        """
        Suggest Pokemon to complete a team based on weaknesses and gaps.

        Args:
            existing_pokemon_ids: IDs of Pokemon already in the team
            prioritize: What to prioritize - "coverage", "defense", or "synergy"
            include_legendaries: Whether to include legendary Pokemon
            legendary_filter: Filter mode - "all", "legendaries", "non-legendaries"
            pokemon_pool: Pokemon source pool - "all" or "pixelmon"
        """
        filter_mode = self._resolve_filter_mode(include_legendaries, legendary_filter)

        # Get existing team Pokemon
        existing_team = []
        for pid in existing_pokemon_ids:
            pokemon = self.pokemon_repo.get_by_id(pid)
            if pokemon:
                existing_team.append(pokemon)

        if not existing_team:
            return self.suggest_team(
                strategy="balanced",
                include_legendaries=include_legendaries,
                legendary_filter=legendary_filter,
                pokemon_pool=pokemon_pool,
            )

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
            filter_mode,
            pokemon_pool,
        )

        return suggestions

    def _empty_team_analysis(self) -> Dict:
        """Return an empty team analysis structure."""
        return {
            "weaknesses": {},
            "resistances": {},
            "immunities": set(),
            "type_coverage": set(),
            "problematic_weaknesses": [],
        }

    def _get_primary_type(self, pokemon: Pokemon) -> Optional[str]:
        """Get Pokemon primary type name."""
        primary = next((pt for pt in pokemon.types if pt.slot == 1), None)
        if primary:
            return primary.type.name
        return pokemon.types[0].type.name if pokemon.types else None

    def _score_candidate_for_strategy(
        self,
        pokemon: Pokemon,
        current_team: List[Pokemon],
        analysis: Dict,
        strategy: str,
    ) -> float:
        """Score candidate quality for a team generation strategy."""
        score = 0.0
        pokemon_types = {pt.type.name for pt in pokemon.types}
        stat_total = self._calculate_stat_total(pokemon)

        # Slightly favor accessible Pokemon in mixed pools
        if strategy == "balanced" and self._is_legendary(pokemon):
            score -= 8.0
        elif not self._is_legendary(pokemon):
            score += 4.0

        # Baseline quality and type diversity
        score += stat_total * (0.08 if not current_team else 0.03)
        new_types = pokemon_types - analysis["type_coverage"]
        score += len(new_types) * 12.0

        # Resist team weaknesses and avoid adding more shared weaknesses
        poke_weaknesses, poke_resistances, poke_immunities = self._get_pokemon_defenses(
            pokemon
        )
        for weak_type, count in analysis["weaknesses"].items():
            if weak_type in poke_immunities:
                score += 10.0 * count
                continue

            resistance_mult = poke_resistances.get(weak_type, 1.0)
            weakness_mult = poke_weaknesses.get(weak_type, 1.0)

            if resistance_mult < 1.0:
                score += (8.0 if resistance_mult <= 0.5 else 4.0) * count
            elif weakness_mult > 1.0:
                score -= (9.0 if weakness_mult >= 2.0 else 6.0) * count

        for weak_type in analysis["problematic_weaknesses"]:
            if weak_type in poke_immunities:
                score += 20.0
            elif poke_resistances.get(weak_type, 1.0) < 1.0:
                score += 14.0
            elif poke_weaknesses.get(weak_type, 1.0) > 1.0:
                score -= 16.0

        # Penalize type stacking
        candidate_primary = self._get_primary_type(pokemon)
        primary_count = sum(
            1
            for member in current_team
            if self._get_primary_type(member) == candidate_primary
        )
        score -= primary_count * 8.0

        overlap_count = sum(
            1
            for member in current_team
            if pokemon_types.intersection({pt.type.name for pt in member.types})
        )
        score -= overlap_count * 2.5

        if not pokemon.stats:
            return score

        offense = pokemon.stats.attack + pokemon.stats.special_attack
        bulk = pokemon.stats.hp + pokemon.stats.defense + pokemon.stats.special_defense
        speed = pokemon.stats.speed

        has_fast = any(m.stats and m.stats.speed >= 100 for m in current_team)
        has_wall = any(
            m.stats and (m.stats.hp + m.stats.defense + m.stats.special_defense) >= 255
            for m in current_team
        )
        has_breaker = any(
            m.stats and (m.stats.attack + m.stats.special_attack) >= 230
            for m in current_team
        )

        if not has_fast and speed >= 100:
            score += 10.0
        if not has_wall and bulk >= 255:
            score += 10.0
        if not has_breaker and offense >= 230:
            score += 10.0

        if strategy == "offensive":
            score += (
                pokemon.stats.attack * 0.16
                + pokemon.stats.special_attack * 0.16
                + pokemon.stats.speed * 0.14
                - (pokemon.stats.defense + pokemon.stats.special_defense) * 0.02
            )
        elif strategy == "defensive":
            score += (
                pokemon.stats.hp * 0.14
                + pokemon.stats.defense * 0.17
                + pokemon.stats.special_defense * 0.17
                - pokemon.stats.speed * 0.01
            )
        elif strategy == "stall":
            score += (
                pokemon.stats.hp * 0.20
                + pokemon.stats.defense * 0.15
                + pokemon.stats.special_defense * 0.15
                - pokemon.stats.attack * 0.03
                - pokemon.stats.special_attack * 0.03
            )
        else:  # balanced
            score += (
                (pokemon.stats.attack + pokemon.stats.special_attack) * 0.08
                + (pokemon.stats.defense + pokemon.stats.special_defense) * 0.08
                + pokemon.stats.speed * 0.05
            )

        return score

    def _build_team_from_candidates(
        self,
        candidates: List[Pokemon],
        strategy: str,
        filter_mode: str,
        team_size: int = 6,
    ) -> List[Dict]:
        """Build a team greedily while re-balancing after each slot."""
        pool = [pokemon for pokemon in candidates if pokemon.types and pokemon.stats]
        selected: List[Pokemon] = []
        strategy_legendary_cap = {
            "balanced": 2,
            "offensive": 3,
            "defensive": 2,
            "stall": 2,
        }
        max_legendaries = strategy_legendary_cap.get(strategy, 2)

        while pool and len(selected) < team_size:
            analysis = (
                self._analyze_team(selected)
                if selected
                else self._empty_team_analysis()
            )

            legendary_count = sum(
                1 for pokemon in selected if self._is_legendary(pokemon)
            )
            if filter_mode == "include" and legendary_count >= max_legendaries:
                eligible_pool = [
                    pokemon for pokemon in pool if not self._is_legendary(pokemon)
                ]
            else:
                eligible_pool = pool

            if not eligible_pool:
                eligible_pool = pool

            best = max(
                eligible_pool,
                key=lambda pokemon: self._score_candidate_for_strategy(
                    pokemon,
                    selected,
                    analysis,
                    strategy,
                ),
            )
            selected.append(best)
            pool = [pokemon for pokemon in pool if pokemon.id != best.id]

        return [self._pokemon_to_suggestion(pokemon) for pokemon in selected]

    def _filter_by_legendary(
        self, pokemon_list: List[Pokemon], filter_mode: str
    ) -> List[Pokemon]:
        """Filter Pokemon list by legendary status."""
        if filter_mode == "all" or filter_mode == "include":
            return pokemon_list
        elif filter_mode == "legendaries":
            return [p for p in pokemon_list if self._is_legendary(p)]
        elif filter_mode == "non-legendaries":
            return [p for p in pokemon_list if not self._is_legendary(p)]
        elif filter_mode == "exclude":
            return [p for p in pokemon_list if not self._is_legendary(p)]
        return pokemon_list

    def _suggest_balanced_team(
        self,
        generation: Optional[int],
        filter_mode: str = "include",
        pokemon_pool: str = "all",
    ) -> List[Dict]:
        """Suggest a balanced team with good type coverage and roles."""
        candidates = self._get_pokemon_by_criteria(
            generation=generation,
            min_base_stat_total=430,
            pokemon_pool=pokemon_pool,
        )
        candidates = self._filter_by_legendary(candidates, filter_mode)
        return self._build_team_from_candidates(
            candidates,
            strategy="balanced",
            filter_mode=filter_mode,
        )

    def _suggest_offensive_team(
        self,
        generation: Optional[int],
        filter_mode: str = "include",
        pokemon_pool: str = "all",
    ) -> List[Dict]:
        """Suggest an offensive team with high attack stats."""
        candidates = self._get_pokemon_by_criteria(
            generation=generation,
            min_base_stat_total=460,
            pokemon_pool=pokemon_pool,
        )
        candidates = self._filter_by_legendary(candidates, filter_mode)
        return self._build_team_from_candidates(
            candidates,
            strategy="offensive",
            filter_mode=filter_mode,
        )

    def _suggest_defensive_team(
        self,
        generation: Optional[int],
        filter_mode: str = "include",
        pokemon_pool: str = "all",
    ) -> List[Dict]:
        """Suggest a defensive team with strong resistances."""
        candidates = self._get_pokemon_by_criteria(
            generation=generation,
            min_base_stat_total=420,
            min_defense=75,
            pokemon_pool=pokemon_pool,
        )
        candidates = self._filter_by_legendary(candidates, filter_mode)
        return self._build_team_from_candidates(
            candidates,
            strategy="defensive",
            filter_mode=filter_mode,
        )

    def _suggest_stall_team(
        self,
        generation: Optional[int],
        filter_mode: str = "include",
        pokemon_pool: str = "all",
    ) -> List[Dict]:
        """Suggest a stall team focused on bulk."""
        candidates = self._get_pokemon_by_criteria(
            generation=generation,
            min_base_stat_total=400,
            min_hp=85,
            min_defense=80,
            pokemon_pool=pokemon_pool,
        )
        candidates = self._filter_by_legendary(candidates, filter_mode)
        return self._build_team_from_candidates(
            candidates,
            strategy="stall",
            filter_mode=filter_mode,
        )

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
        filter_mode: str = "include",
        pokemon_pool: str = "all",
    ) -> List[Dict]:
        """Find Pokemon that complement the existing team."""
        suggestions = []
        existing_ids = [p.id for p in existing_team]
        candidates = self._get_pokemon_by_criteria(
            exclude_ids=existing_ids,
            min_base_stat_total=400,
            pokemon_pool=pokemon_pool,
        )
        candidates = self._filter_by_legendary(candidates, filter_mode)
        max_legendaries = 2

        simulated_team = list(existing_team)
        available = [
            pokemon for pokemon in candidates if pokemon.types and pokemon.stats
        ]

        while available and len(suggestions) < count:
            current_analysis = self._analyze_team(simulated_team)

            current_legendary_count = sum(
                1 for pokemon in simulated_team if self._is_legendary(pokemon)
            )
            if filter_mode == "include" and current_legendary_count >= max_legendaries:
                eligible_available = [
                    pokemon for pokemon in available if not self._is_legendary(pokemon)
                ]
            else:
                eligible_available = available

            if not eligible_available:
                eligible_available = available

            best_score, best_pokemon = max(
                (
                    (
                        self._score_team_fit(
                            pokemon,
                            simulated_team,
                            current_analysis,
                            prioritize,
                        ),
                        pokemon,
                    )
                    for pokemon in eligible_available
                ),
                key=lambda item: item[0],
            )

            suggestions.append(
                {
                    **self._pokemon_to_suggestion(best_pokemon),
                    "fit_score": round(best_score, 2),
                    "reason": self._explain_suggestion(best_pokemon, current_analysis),
                }
            )
            simulated_team.append(best_pokemon)
            available = [
                pokemon for pokemon in available if pokemon.id != best_pokemon.id
            ]

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

        # Penalize adding to current weak points
        for weak_type, count in analysis["weaknesses"].items():
            if poke_weaknesses.get(weak_type, 1.0) > 1.0:
                score -= 4.0 * count

        # Penalize repetitive typing
        overlap_count = sum(
            1
            for member in existing_team
            if pokemon_types.intersection({pt.type.name for pt in member.types})
        )
        score -= overlap_count * 1.5

        # Slightly prefer non-legendaries in mixed pools
        if not self._is_legendary(pokemon):
            score += 4.0

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
        pokemon_pool: str = "all",
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

        if pokemon_pool == "pixelmon":
            query = query.filter(Pokemon.cobblemon_spawns.any())

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
