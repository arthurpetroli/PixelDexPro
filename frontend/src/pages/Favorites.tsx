import { useMemo } from 'react';
import { Heart, Trash2, Grid, List } from 'lucide-react';
import { useState } from 'react';
import { PokemonCard } from '@/components/pokemon/PokemonCard';
import { TypeBadge } from '@/components/pokemon/TypeBadge';
import { LoadingPage } from '@/components/ui/Loading';
import { useFavoritesStore } from '@/store';
import { usePokemonList } from '@/hooks/useApi';
import { formatPokemonName, formatPokedexNumber } from '@/utils/pokemon';
import { cn } from '@/utils/helpers';
import type { PokemonListItem } from '@/types';

type ViewMode = 'grid' | 'list';

export default function Favorites() {
  const { favorites, removeFavorite, clearFavorites } = useFavoritesStore();
  const [viewMode, setViewMode] = useState<ViewMode>('grid');

  // Fetch all pokemon to filter by favorites
  // In a real app, we'd have an endpoint that accepts multiple IDs
  const { data: allPokemon, isLoading } = usePokemonList({ page_size: 1000 });

  // Filter to only show favorites
  const favoritePokemon = useMemo(() => {
    if (!allPokemon) return [];
    return allPokemon.items.filter((p) => favorites.includes(p.id));
  }, [allPokemon, favorites]);

  // Sort favorites in the order they were added (based on favorites array order)
  const sortedFavorites = useMemo(() => {
    return [...favoritePokemon].sort(
      (a, b) => favorites.indexOf(a.id) - favorites.indexOf(b.id)
    );
  }, [favoritePokemon, favorites]);

  if (isLoading) {
    return <LoadingPage message="Loading favorites..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Heart className="w-8 h-8 text-red-500 fill-red-500" />
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Favorites</h1>
            <p className="text-sm text-gray-500">
              {favorites.length} {favorites.length === 1 ? 'Pokémon' : 'Pokémon'} saved
            </p>
          </div>
        </div>

        <div className="flex gap-2">
          {/* View Toggle */}
          <div className="flex rounded-lg border border-gray-200 overflow-hidden">
            <button
              onClick={() => setViewMode('grid')}
              className={cn(
                'p-2 transition-colors',
                viewMode === 'grid' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'
              )}
            >
              <Grid className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={cn(
                'p-2 transition-colors',
                viewMode === 'list' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'
              )}
            >
              <List className="w-5 h-5" />
            </button>
          </div>

          {/* Clear All */}
          <button
            onClick={() => {
              if (window.confirm('Are you sure you want to clear all favorites?')) {
                clearFavorites();
              }
            }}
            disabled={favorites.length === 0}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-red-100 text-red-700 hover:bg-red-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Clear All
          </button>
        </div>
      </div>

      {/* Content */}
      {sortedFavorites.length === 0 ? (
        <div className="text-center py-16 bg-gray-50 rounded-xl">
          <Heart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-700 mb-2">No Favorites Yet</h3>
          <p className="text-gray-500 max-w-md mx-auto">
            Start adding your favorite Pokémon by clicking the heart icon on any Pokémon card
            in the Pokédex.
          </p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
          {sortedFavorites.map((pokemon) => (
            <PokemonCard key={pokemon.id} pokemon={pokemon} />
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          {sortedFavorites.map((pokemon) => (
            <FavoriteListItem
              key={pokemon.id}
              pokemon={pokemon}
              onRemove={() => removeFavorite(pokemon.id)}
            />
          ))}
        </div>
      )}

      {/* Stats */}
      {sortedFavorites.length > 0 && (
        <div className="bg-gray-50 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Favorites Summary</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
              label="Total Favorites"
              value={sortedFavorites.length.toString()}
            />
            <StatCard
              label="Unique Types"
              value={getUniqueTypes(sortedFavorites).length.toString()}
            />
            <StatCard
              label="Most Common Type"
              value={getMostCommonType(sortedFavorites) || 'N/A'}
            />
            <StatCard
              label="Generations"
              value={getUniqueGenerations(sortedFavorites).length.toString()}
            />
          </div>
        </div>
      )}
    </div>
  );
}

// Helper components
function FavoriteListItem({
  pokemon,
  onRemove,
}: {
  pokemon: PokemonListItem;
  onRemove: () => void;
}) {
  return (
    <div className="flex items-center gap-4 p-3 bg-white rounded-lg border border-gray-100 hover:shadow-md transition-shadow">
      <img
        src={pokemon.sprite_url || '/placeholder-pokemon.png'}
        alt={pokemon.name}
        className="w-12 h-12 object-contain"
      />
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-400">
            {formatPokedexNumber(pokemon.pokedex_number)}
          </span>
          <a
            href={`/pokemon/${pokemon.id}`}
            className="font-semibold text-gray-800 hover:text-blue-600 truncate"
          >
            {formatPokemonName(pokemon.name)}
          </a>
        </div>
        <div className="flex gap-1 mt-1">
          {pokemon.types.map((t) => (
            <TypeBadge key={t.type.name} type={t.type.name} size="sm" />
          ))}
        </div>
      </div>
      <button
        onClick={onRemove}
        className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
      >
        <Heart className="w-5 h-5 fill-current" />
      </button>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-white rounded-lg p-4 border border-gray-100">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold text-gray-800 capitalize">{value}</p>
    </div>
  );
}

// Helper functions
function getUniqueTypes(pokemon: PokemonListItem[]): string[] {
  const types = new Set<string>();
  pokemon.forEach((p) => p.types.forEach((t) => types.add(t.type.name)));
  return Array.from(types);
}

function getMostCommonType(pokemon: PokemonListItem[]): string | null {
  const typeCounts: Record<string, number> = {};
  pokemon.forEach((p) =>
    p.types.forEach((t) => {
      typeCounts[t.type.name] = (typeCounts[t.type.name] || 0) + 1;
    })
  );
  const entries = Object.entries(typeCounts);
  if (entries.length === 0) return null;
  entries.sort((a, b) => b[1] - a[1]);
  return entries[0][0];
}

function getUniqueGenerations(pokemon: PokemonListItem[]): number[] {
  const gens = new Set<number>();
  pokemon.forEach((p) => {
    if (p.generation) gens.add(p.generation);
  });
  return Array.from(gens).sort((a, b) => a - b);
}
