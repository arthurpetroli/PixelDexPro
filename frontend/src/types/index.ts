// Base Types
export interface Type {
  id: number;
  name: string;
  pokeapi_id: number | null;
  color: string | null;
}

export interface PokemonType {
  type: Type;
  slot: number;
}

export interface Ability {
  name: string;
  description: string | null;
  is_hidden: boolean;
}

export interface PokemonAbility {
  ability: Ability;
  slot: number;
  is_hidden: boolean;
}

export interface Stats {
  id: number;
  pokemon_id: number;
  hp: number;
  attack: number;
  defense: number;
  special_attack: number;
  special_defense: number;
  speed: number;
  total: number;
}

export interface Evolution {
  to_pokemon_id: number;
  trigger: string | null;
  min_level: number | null;
  item: string | null;
  condition: string | null;
  chain_order: number;
}

// Pokemon
export interface Pokemon {
  id: number;
  pokeapi_id: number | null;
  name: string;
  pokedex_number: number | null;
  height: number | null;
  weight: number | null;
  base_experience: number | null;
  generation: number | null;
  category: string | null;
  description: string | null;
  sprite_url: string | null;
  sprite_shiny_url: string | null;
  sprite_official_url: string | null;
  is_default: boolean;
  forms: string[];
  types: PokemonType[];
  abilities: PokemonAbility[];
  stats: Stats | null;
  evolutions: Evolution[];
}

export interface PokemonListItem {
  id: number;
  pokeapi_id: number | null;
  name: string;
  pokedex_number: number | null;
  sprite_url: string | null;
  types: PokemonType[];
  generation: number | null;
}

export interface PokemonListResponse {
  items: PokemonListItem[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface PokemonDetails extends Pokemon {
  weaknesses: Record<string, number>;
  resistances: Record<string, number>;
  immunities: string[];
  quadruple_weaknesses: string[];
  quadruple_resistances: string[];
  strategic_tags: string[];
  cobblemon_spawns: Spawn[];
}

// Cobblemon
export interface Spawn {
  id: number;
  pokemon_id: number;
  pokemon_name: string | null;
  entry_number: number | null;
  bucket: string | null;
  weight: number | null;
  min_level: number | null;
  max_level: number | null;
  biomes: string[];
  excluded_biomes: string[];
  time: string | null;
  weather: string[];
  context: string | null;
  presets: string[];
  conditions: string[];
  anticonditions: string[];
  skylight_min: number | null;
  skylight_max: number | null;
  can_see_sky: boolean | null;
  pattern_key_value: Record<string, string>;
  source_sheet: string | null;
  source_version: string | null;
}

export interface SpawnListResponse {
  items: Spawn[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
  has_prev: boolean;
}

// Compare
export interface StatComparison {
  pokemon1_value: number;
  pokemon2_value: number;
  difference: number;
  winner: string;
}

export interface CompareResponse {
  pokemon1: PokemonDetails;
  pokemon2: PokemonDetails;
  stat_comparison: Record<string, StatComparison>;
  type_comparison: {
    pokemon1_types: string[];
    pokemon2_types: string[];
    pokemon1_weaknesses: string[];
    pokemon2_weaknesses: string[];
    pokemon1_resistances: string[];
    pokemon2_resistances: string[];
    pokemon1_immunities: string[];
    pokemon2_immunities: string[];
    shared_weaknesses: string[];
    shared_resistances: string[];
  };
  spawn_comparison: {
    pokemon1_spawn_count: number;
    pokemon2_spawn_count: number;
    pokemon1_biomes: string[];
    pokemon2_biomes: string[];
    shared_biomes: string[];
    pokemon1_has_spawns: boolean;
    pokemon2_has_spawns: boolean;
  };
}

// Teams
export interface TeamPokemon {
  id: number;
  team_id: number;
  pokemon_id: number;
  slot: number;
  nickname: string | null;
  level: number;
  ability: string | null;
  nature: string | null;
  held_item: string | null;
  moves: string[];
}

export interface Team {
  id: number;
  name: string;
  description: string | null;
  is_public: boolean;
  team_pokemon: TeamPokemon[];
  created_at: string;
  updated_at: string;
}

export interface TeamAnalysis {
  team_id: number;
  weaknesses: Record<string, number>;
  resistances: Record<string, number>;
  immunities: string[];
  shared_weaknesses: Record<string, string[]>;
  problematic_types: string[];
  role_distribution: Record<string, number>;
  coverage_score: number;
  defensive_score: number;
  summary: string;
}

// Favorites
export interface Favorite {
  id: number;
  pokemon_id: number;
  pokemon: PokemonListItem;
  created_at: string;
}

// Type Chart
export interface TypeChartResponse {
  chart: Record<string, Record<string, number>>;
  types: string[];
}

// Sync
export interface SyncStatus {
  status: string;
  message: string;
  synced_count: number;
  errors: string[];
}

// Filter params
export interface PokemonFilters {
  type?: string;
  generation?: number;
  search?: string;
  page?: number;
  page_size?: number;
}

export interface SpawnFilters {
  pokemon?: string;
  biome?: string;
  time?: string;
  weather?: string;
  min_level?: number;
  max_level?: number;
  context?: string;
  page?: number;
  page_size?: number;
}
