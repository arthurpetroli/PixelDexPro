import { useState } from 'react';
import { SearchBar } from '@/components/ui/SearchBar';
import { PokemonCard } from '@/components/pokemon/PokemonCard';
import { LoadingPage } from '@/components/ui/Loading';
import { usePokemonList, useTypes } from '@/hooks/useApi';
import { ALL_TYPES, GENERATIONS } from '@/utils/pokemon';
import type { PokemonFilters } from '@/types';

export default function Pokedex() {
  const [filters, setFilters] = useState<PokemonFilters>({
    page: 1,
    page_size: 50,
  });

  const { data, isLoading, error } = usePokemonList(filters);
  const { data: types } = useTypes();

  const handleSearch = (query: string) => {
    setFilters((prev) => ({ ...prev, search: query || undefined, page: 1 }));
  };

  const handleTypeFilter = (type: string) => {
    setFilters((prev) => ({
      ...prev,
      type: type === prev.type ? undefined : type,
      page: 1,
    }));
  };

  const handleGenerationFilter = (gen: number) => {
    setFilters((prev) => ({
      ...prev,
      generation: gen === prev.generation ? undefined : gen,
      page: 1,
    }));
  };

  const handlePageChange = (newPage: number) => {
    setFilters((prev) => ({ ...prev, page: newPage }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">Failed to load Pokémon. Please try again later.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Pokédex</h1>
        <SearchBar
          onSearch={handleSearch}
          showDropdown={false}
          placeholder="Search by name..."
          className="w-full md:w-80"
        />
      </div>

      {/* Filters */}
      <div className="space-y-4">
        {/* Type Filter */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Filter by Type</h3>
          <div className="flex flex-wrap gap-2">
            {ALL_TYPES.map((type) => (
              <button
                key={type}
                onClick={() => handleTypeFilter(type)}
                className={`px-3 py-1 rounded-full text-sm capitalize transition-all ${
                  filters.type === type
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* Generation Filter */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Filter by Generation</h3>
          <div className="flex flex-wrap gap-2">
            {GENERATIONS.map((gen) => (
              <button
                key={gen}
                onClick={() => handleGenerationFilter(gen)}
                className={`px-3 py-1 rounded-full text-sm transition-all ${
                  filters.generation === gen
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                Gen {gen}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      {isLoading ? (
        <LoadingPage message="Loading Pokémon..." />
      ) : data && data.items.length > 0 ? (
        <>
          {/* Results count */}
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Showing {data.items.length} of {data.total} Pokémon
          </p>

          {/* Pokemon Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
            {data.items.map((pokemon) => (
              <PokemonCard key={pokemon.id} pokemon={pokemon} />
            ))}
          </div>

          {/* Pagination */}
          {(data.has_prev || data.has_next) && (
            <div className="flex justify-center gap-2 pt-6">
              <button
                onClick={() => handlePageChange(data.page - 1)}
                disabled={!data.has_prev}
                className="px-4 py-2 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                Previous
              </button>
              <span className="px-4 py-2 text-gray-600 dark:text-gray-400">
                Page {data.page}
              </span>
              <button
                onClick={() => handlePageChange(data.page + 1)}
                disabled={!data.has_next}
                className="px-4 py-2 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                Next
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">No Pokémon found. Try different filters.</p>
        </div>
      )}
    </div>
  );
}
