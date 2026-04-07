import axios from 'axios';
import type {
  Pokemon,
  PokemonDetails,
  PokemonListResponse,
  PokemonFilters,
  PokemonListItem,
  Spawn,
  SpawnListResponse,
  SpawnFilters,
  CompareResponse,
  Team,
  TeamAnalysis,
  Favorite,
  TypeChartResponse,
  SyncStatus,
} from '@/types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Pokemon endpoints
export const pokemonApi = {
  list: async (filters: PokemonFilters = {}): Promise<PokemonListResponse> => {
    const params = new URLSearchParams();
    if (filters.type) params.append('type', filters.type);
    if (filters.generation) params.append('generation', filters.generation.toString());
    if (filters.search) params.append('search', filters.search);
    if (filters.pokemon_pool) params.append('pokemon_pool', filters.pokemon_pool);
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.page_size) params.append('page_size', filters.page_size.toString());
    
    const { data } = await api.get<PokemonListResponse>(`/pokemon?${params}`);
    return data;
  },

  getById: async (id: number): Promise<Pokemon> => {
    const { data } = await api.get<Pokemon>(`/pokemon/${id}`);
    return data;
  },

  getDetails: async (id: number): Promise<PokemonDetails> => {
    const { data } = await api.get<PokemonDetails>(`/pokemon/${id}/details`);
    return data;
  },

  search: async (query: string, limit: number = 20): Promise<PokemonListItem[]> => {
    const { data } = await api.get<PokemonListItem[]>(`/pokemon/search?q=${query}&limit=${limit}`);
    return data;
  },
};

// Types endpoints
export const typesApi = {
  list: async () => {
    const { data } = await api.get<{ id: number; name: string; color: string }[]>('/types');
    return data;
  },

  getChart: async (): Promise<TypeChartResponse> => {
    const { data } = await api.get<TypeChartResponse>('/types/chart');
    return data;
  },
};

// Cobblemon endpoints
export const cobblemonApi = {
  listSpawns: async (filters: SpawnFilters = {}): Promise<SpawnListResponse> => {
    const params = new URLSearchParams();
    if (filters.pokemon) params.append('pokemon', filters.pokemon);
    if (filters.biome) params.append('biome', filters.biome);
    if (filters.time) params.append('time', filters.time);
    if (filters.weather) params.append('weather', filters.weather);
    if (filters.min_level) params.append('min_level', filters.min_level.toString());
    if (filters.max_level) params.append('max_level', filters.max_level.toString());
    if (filters.context) params.append('context', filters.context);
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.page_size) params.append('page_size', filters.page_size.toString());
    
    const { data } = await api.get<SpawnListResponse>(`/cobblemon/spawns?${params}`);
    return data;
  },

  getSpawnsByPokemon: async (pokemonId: number): Promise<Spawn[]> => {
    const { data } = await api.get<Spawn[]>(`/cobblemon/spawns/${pokemonId}`);
    return data;
  },

  getBiomes: async (): Promise<string[]> => {
    const { data } = await api.get<string[]>('/cobblemon/biomes');
    return data;
  },

  getBiomesFromSheets: async (): Promise<string[]> => {
    const { data } = await api.get<string[]>('/cobblemon/sheets/biomes');
    return data;
  },

  getSpawnsFromSheets: async (pokemon?: string, biome?: string): Promise<any[]> => {
    const params = new URLSearchParams();
    if (pokemon) params.append('pokemon', pokemon);
    if (biome) params.append('biome', biome);
    
    const { data } = await api.get<any[]>(`/cobblemon/sheets/spawns?${params}`);
    return data;
  },
};

// Compare endpoints
export const compareApi = {
  compare: async (pokemon1Id: number, pokemon2Id: number): Promise<CompareResponse> => {
    const { data } = await api.get<CompareResponse>(`/compare?pokemon1=${pokemon1Id}&pokemon2=${pokemon2Id}`);
    return data;
  },
};

// Teams endpoints
export const teamsApi = {
  create: async (name: string, description?: string): Promise<Team> => {
    const { data } = await api.post<Team>('/teams', { name, description });
    return data;
  },

  getById: async (id: number): Promise<Team> => {
    const { data } = await api.get<Team>(`/teams/${id}`);
    return data;
  },

  addPokemon: async (teamId: number, pokemonId: number, slot: number, nickname?: string) => {
    const { data } = await api.post(`/teams/${teamId}/pokemon`, {
      pokemon_id: pokemonId,
      slot,
      nickname,
    });
    return data;
  },

  removePokemon: async (teamId: number, pokemonId: number) => {
    const { data } = await api.delete(`/teams/${teamId}/pokemon/${pokemonId}`);
    return data;
  },

  analyze: async (teamId: number): Promise<TeamAnalysis> => {
    const { data } = await api.get<TeamAnalysis>(`/teams/${teamId}/analysis`);
    return data;
  },

  suggestComplete: async (
    strategy: string = 'balanced',
    generation?: number,
    includeLegendaries: boolean = true,
    legendaryFilter: string = 'all',
    pokemonPool: 'all' | 'pixelmon' = 'all'
  ): Promise<any> => {
    const params = new URLSearchParams();
    params.append('strategy', strategy);
    if (generation) params.append('generation', generation.toString());
    params.append('include_legendaries', includeLegendaries.toString());
    params.append('legendary_filter', legendaryFilter);
    params.append('pokemon_pool', pokemonPool);
    
    const { data } = await api.get(`/teams/suggest/complete?${params}`);
    return data;
  },

  suggestAutocomplete: async (
    pokemonIds: number[],
    prioritize: string = 'coverage',
    includeLegendaries: boolean = true,
    legendaryFilter: string = 'all',
    pokemonPool: 'all' | 'pixelmon' = 'all'
  ): Promise<any> => {
    const { data } = await api.post('/teams/suggest/autocomplete', {
      pokemon_ids: pokemonIds,
      prioritize,
      include_legendaries: includeLegendaries,
      legendary_filter: legendaryFilter,
      pokemon_pool: pokemonPool,
    });
    return data;
  },
};

// Favorites endpoints
export const favoritesApi = {
  list: async (): Promise<Favorite[]> => {
    const { data } = await api.get<Favorite[]>('/favorites');
    return data;
  },

  add: async (pokemonId: number): Promise<Favorite> => {
    const { data } = await api.post<Favorite>(`/favorites/${pokemonId}`);
    return data;
  },

  remove: async (pokemonId: number) => {
    const { data } = await api.delete(`/favorites/${pokemonId}`);
    return data;
  },

  check: async (pokemonId: number): Promise<boolean> => {
    const { data } = await api.get<{ is_favorite: boolean }>(`/favorites/${pokemonId}/check`);
    return data.is_favorite;
  },
};

// Sync endpoints
export const syncApi = {
  syncPokemon: async (nameOrId: string): Promise<SyncStatus> => {
    const { data } = await api.post<SyncStatus>(`/sync/pokeapi/pokemon/${nameOrId}`);
    return data;
  },

  syncPokemonBatch: async (limit: number = 151, offset: number = 0): Promise<SyncStatus> => {
    const { data } = await api.post<SyncStatus>(`/sync/pokeapi/pokemon?limit=${limit}&offset=${offset}`);
    return data;
  },

  syncTypes: async (): Promise<SyncStatus> => {
    const { data } = await api.post<SyncStatus>('/sync/pokeapi/types');
    return data;
  },

  syncCobblemonSpawns: async (sheetUrl: string, version: string = '1.0'): Promise<SyncStatus> => {
    const { data } = await api.post<SyncStatus>('/sync/cobblemon/spawns', {
      sheet_url: sheetUrl,
      version,
    });
    return data;
  },
};

export default api;
