import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { pokemonApi, typesApi, cobblemonApi, compareApi, teamsApi, syncApi } from '@/services/api';
import type { PokemonFilters, SpawnFilters } from '@/types';

// Pokemon hooks
export function usePokemonList(filters: PokemonFilters = {}) {
  return useQuery({
    queryKey: ['pokemon', 'list', filters],
    queryFn: () => pokemonApi.list(filters),
  });
}

export function usePokemon(id: number | null) {
  return useQuery({
    queryKey: ['pokemon', id],
    queryFn: () => pokemonApi.getById(id!),
    enabled: id !== null,
  });
}

export function usePokemonDetails(id: number | null) {
  return useQuery({
    queryKey: ['pokemon', 'details', id],
    queryFn: () => pokemonApi.getDetails(id!),
    enabled: id !== null,
  });
}

export function usePokemonSearch(query: string) {
  return useQuery({
    queryKey: ['pokemon', 'search', query],
    queryFn: () => pokemonApi.search(query),
    enabled: query.length >= 2,
  });
}

// Types hooks
export function useTypes() {
  return useQuery({
    queryKey: ['types'],
    queryFn: typesApi.list,
    staleTime: Infinity,
  });
}

export function useTypeChart() {
  return useQuery({
    queryKey: ['types', 'chart'],
    queryFn: typesApi.getChart,
    staleTime: Infinity,
  });
}

// Cobblemon hooks
export function useSpawnList(filters: SpawnFilters = {}) {
  return useQuery({
    queryKey: ['spawns', 'list', filters],
    queryFn: () => cobblemonApi.listSpawns(filters),
  });
}

export function usePokemonSpawns(pokemonId: number | null) {
  return useQuery({
    queryKey: ['spawns', 'pokemon', pokemonId],
    queryFn: () => cobblemonApi.getSpawnsByPokemon(pokemonId!),
    enabled: pokemonId !== null,
  });
}

export function useBiomes() {
  return useQuery({
    queryKey: ['biomes'],
    queryFn: cobblemonApi.getBiomes,
    staleTime: Infinity,
  });
}

export function useBiomesFromSheets() {
  return useQuery({
    queryKey: ['biomes', 'sheets'],
    queryFn: cobblemonApi.getBiomesFromSheets,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useSpawnsFromSheets(pokemon?: string, biome?: string) {
  return useQuery({
    queryKey: ['spawns', 'sheets', pokemon, biome],
    queryFn: () => cobblemonApi.getSpawnsFromSheets(pokemon, biome),
    enabled: !!(pokemon || biome),
  });
}

// Compare hooks
export function useCompare(pokemon1Id: number | null, pokemon2Id: number | null) {
  return useQuery({
    queryKey: ['compare', pokemon1Id, pokemon2Id],
    queryFn: () => compareApi.compare(pokemon1Id!, pokemon2Id!),
    enabled: pokemon1Id !== null && pokemon2Id !== null,
  });
}

// Teams hooks
export function useTeam(id: number | null) {
  return useQuery({
    queryKey: ['team', id],
    queryFn: () => teamsApi.getById(id!),
    enabled: id !== null,
  });
}

export function useTeamAnalysis(id: number | null) {
  return useQuery({
    queryKey: ['team', 'analysis', id],
    queryFn: () => teamsApi.analyze(id!),
    enabled: id !== null,
  });
}

export function useCreateTeam() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ name, description }: { name: string; description?: string }) =>
      teamsApi.create(name, description),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['teams'] });
    },
  });
}

// Sync hooks
export function useSyncPokemon() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (nameOrId: string) => syncApi.syncPokemon(nameOrId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pokemon'] });
    },
  });
}

export function useSyncPokemonBatch() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ limit, offset }: { limit?: number; offset?: number }) =>
      syncApi.syncPokemonBatch(limit, offset),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pokemon'] });
    },
  });
}

export function useSyncTypes() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => syncApi.syncTypes(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['types'] });
    },
  });
}

export function useSyncCobblemonSpawns() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ sheetUrl, version }: { sheetUrl: string; version?: string }) =>
      syncApi.syncCobblemonSpawns(sheetUrl, version),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['spawns'] });
    },
  });
}
