import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { PokemonListItem, PokemonDetails, Team, TeamAnalysis } from '@/types';

// Favorites Store (local storage)
interface FavoritesState {
  favorites: number[];
  addFavorite: (pokemonId: number) => void;
  removeFavorite: (pokemonId: number) => void;
  isFavorite: (pokemonId: number) => boolean;
  clearFavorites: () => void;
}

export const useFavoritesStore = create<FavoritesState>()(
  persist(
    (set, get) => ({
      favorites: [],
      addFavorite: (pokemonId) =>
        set((state) => ({
          favorites: state.favorites.includes(pokemonId)
            ? state.favorites
            : [...state.favorites, pokemonId],
        })),
      removeFavorite: (pokemonId) =>
        set((state) => ({
          favorites: state.favorites.filter((id) => id !== pokemonId),
        })),
      isFavorite: (pokemonId) => get().favorites.includes(pokemonId),
      clearFavorites: () => set({ favorites: [] }),
    }),
    {
      name: 'pixeldex-favorites',
    }
  )
);

// Team Builder Store (local storage)
interface TeamSlot {
  pokemon: PokemonListItem | null;
  details: PokemonDetails | null;
}

interface TeamBuilderState {
  slots: TeamSlot[];
  teamName: string;
  setTeamName: (name: string) => void;
  addPokemon: (slot: number, pokemon: PokemonListItem, details: PokemonDetails) => void;
  removePokemon: (slot: number) => void;
  clearTeam: () => void;
  getPokemonIds: () => number[];
  getTeamTypes: () => string[][];
}

const emptySlots = (): TeamSlot[] =>
  Array(6).fill(null).map(() => ({ pokemon: null, details: null }));

export const useTeamBuilderStore = create<TeamBuilderState>()(
  persist(
    (set, get) => ({
      slots: emptySlots(),
      teamName: 'My Team',
      setTeamName: (name) => set({ teamName: name }),
      addPokemon: (slot, pokemon, details) =>
        set((state) => {
          const newSlots = [...state.slots];
          newSlots[slot] = { pokemon, details };
          return { slots: newSlots };
        }),
      removePokemon: (slot) =>
        set((state) => {
          const newSlots = [...state.slots];
          newSlots[slot] = { pokemon: null, details: null };
          return { slots: newSlots };
        }),
      clearTeam: () => set({ slots: emptySlots(), teamName: 'My Team' }),
      getPokemonIds: () =>
        get()
          .slots.filter((s) => s.pokemon !== null)
          .map((s) => s.pokemon!.id),
      getTeamTypes: () =>
        get()
          .slots.filter((s) => s.details !== null)
          .map((s) => s.details!.types.map((t) => t.type.name)),
    }),
    {
      name: 'pixeldex-team-builder',
    }
  )
);

// Compare Store
interface CompareState {
  pokemon1: PokemonListItem | null;
  pokemon2: PokemonListItem | null;
  setPokemon1: (pokemon: PokemonListItem | null) => void;
  setPokemon2: (pokemon: PokemonListItem | null) => void;
  swap: () => void;
  clear: () => void;
}

export const useCompareStore = create<CompareState>((set) => ({
  pokemon1: null,
  pokemon2: null,
  setPokemon1: (pokemon) => set({ pokemon1: pokemon }),
  setPokemon2: (pokemon) => set({ pokemon2: pokemon }),
  swap: () =>
    set((state) => ({
      pokemon1: state.pokemon2,
      pokemon2: state.pokemon1,
    })),
  clear: () => set({ pokemon1: null, pokemon2: null }),
}));

// UI State Store
interface UIState {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: false,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
}));
