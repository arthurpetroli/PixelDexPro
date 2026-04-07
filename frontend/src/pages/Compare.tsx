import { useSearchParams } from 'react-router-dom';
import { ArrowLeftRight } from 'lucide-react';
import { SearchBar } from '@/components/ui/SearchBar';
import { TypeBadge } from '@/components/pokemon/TypeBadge';
import { StatsDisplay, StatBar } from '@/components/pokemon/StatBar';
import { WeaknessChart } from '@/components/pokemon/WeaknessChart';
import { LoadingPage } from '@/components/ui/Loading';
import { useCompare, usePokemonDetails } from '@/hooks/useApi';
import { useCompareStore } from '@/store';
import { formatPokemonName, formatStatName, getTypeColor } from '@/utils/pokemon';
import type { PokemonListItem } from '@/types';

export default function Compare() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { pokemon1, pokemon2, setPokemon1, setPokemon2, swap, clear } = useCompareStore();

  // Get IDs from URL or store
  const pokemon1Id = searchParams.get('pokemon1')
    ? parseInt(searchParams.get('pokemon1')!)
    : pokemon1?.id || null;
  const pokemon2Id = searchParams.get('pokemon2')
    ? parseInt(searchParams.get('pokemon2')!)
    : pokemon2?.id || null;

  const { data: details1, isLoading: loading1 } = usePokemonDetails(pokemon1Id);
  const { data: details2, isLoading: loading2 } = usePokemonDetails(pokemon2Id);

  const handleSelectPokemon1 = (pokemon: PokemonListItem) => {
    setPokemon1(pokemon);
    const params = new URLSearchParams(searchParams);
    params.set('pokemon1', pokemon.id.toString());
    setSearchParams(params);
  };

  const handleSelectPokemon2 = (pokemon: PokemonListItem) => {
    setPokemon2(pokemon);
    const params = new URLSearchParams(searchParams);
    params.set('pokemon2', pokemon.id.toString());
    setSearchParams(params);
  };

  const handleSwap = () => {
    swap();
    const params = new URLSearchParams(searchParams);
    if (pokemon1Id) params.set('pokemon2', pokemon1Id.toString());
    if (pokemon2Id) params.set('pokemon1', pokemon2Id.toString());
    setSearchParams(params);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Compare Pokémon</h1>

      {/* Selection */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">First Pokémon</label>
          <SearchBar
            onSelect={handleSelectPokemon1}
            placeholder="Search Pokémon..."
          />
        </div>

        <div className="flex justify-center">
          <button
            onClick={handleSwap}
            className="p-3 rounded-full bg-blue-100 dark:bg-blue-900/50 hover:bg-blue-200 dark:hover:bg-blue-800/50 transition-colors"
            title="Swap Pokémon"
          >
            <ArrowLeftRight className="w-6 h-6 text-blue-600 dark:text-blue-400" />
          </button>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Second Pokémon</label>
          <SearchBar
            onSelect={handleSelectPokemon2}
            placeholder="Search Pokémon..."
          />
        </div>
      </div>

      {/* Loading */}
      {(loading1 || loading2) && <LoadingPage message="Loading comparison..." />}

      {/* Comparison */}
      {details1 && details2 && (
        <div className="space-y-8">
          {/* Header Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[details1, details2].map((pokemon) => {
              const primaryType = pokemon.types[0]?.type.name || 'normal';
              return (
                <div
                  key={pokemon.id}
                  className="rounded-xl overflow-hidden shadow-md"
                  style={{
                    background: `linear-gradient(135deg, ${getTypeColor(primaryType)}40 0%, ${getTypeColor(primaryType)}20 100%)`,
                  }}
                >
                  <div className="p-6 flex items-center gap-4">
                    <img
                      src={pokemon.sprite_url || '/placeholder-pokemon.png'}
                      alt={pokemon.name}
                      className="w-24 h-24 object-contain"
                    />
                    <div>
                      <h3 className="text-xl font-bold text-gray-900">
                        {formatPokemonName(pokemon.name)}
                      </h3>
                      <div className="flex gap-1 mt-2">
                        {pokemon.types.map((t) => (
                          <TypeBadge key={t.type.name} type={t.type.name} size="sm" />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Stats Comparison */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">Stats Comparison</h2>
            <div className="space-y-4">
              {['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed', 'total'].map(
                (stat) => {
                  const val1 = details1.stats?.[stat as keyof typeof details1.stats] || 0;
                  const val2 = details2.stats?.[stat as keyof typeof details2.stats] || 0;
                  const winner = val1 > val2 ? 1 : val2 > val1 ? 2 : 0;

                  return (
                    <div key={stat} className="grid grid-cols-7 gap-4 items-center">
                      <div
                        className={`text-right font-bold ${
                          winner === 1 ? 'text-green-600 dark:text-green-400' : 'text-gray-600 dark:text-gray-300'
                        }`}
                      >
                        {val1}
                      </div>
                      <div className="col-span-2">
                        <div className="h-3 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden flex justify-end">
                          <div
                            className="h-full bg-blue-500 rounded-full"
                            style={{ width: `${(val1 / 255) * 100}%` }}
                          />
                        </div>
                      </div>
                      <div className="text-center text-sm font-medium text-gray-700 dark:text-gray-300">
                        {formatStatName(stat)}
                      </div>
                      <div className="col-span-2">
                        <div className="h-3 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-red-500 rounded-full"
                            style={{ width: `${(val2 / 255) * 100}%` }}
                          />
                        </div>
                      </div>
                      <div
                        className={`font-bold ${
                          winner === 2 ? 'text-green-600 dark:text-green-400' : 'text-gray-600 dark:text-gray-300'
                        }`}
                      >
                        {val2}
                      </div>
                    </div>
                  );
                }
              )}
            </div>
          </div>

          {/* Type Effectiveness */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
              <h3 className="font-bold text-gray-900 dark:text-white mb-4">
                {formatPokemonName(details1.name)} Weaknesses
              </h3>
              <WeaknessChart
                weaknesses={details1.weaknesses}
                resistances={details1.resistances}
                immunities={details1.immunities}
                compact
              />
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
              <h3 className="font-bold text-gray-900 dark:text-white mb-4">
                {formatPokemonName(details2.name)} Weaknesses
              </h3>
              <WeaknessChart
                weaknesses={details2.weaknesses}
                resistances={details2.resistances}
                immunities={details2.immunities}
                compact
              />
            </div>
          </div>
        </div>
      )}

      {/* Empty state */}
      {!details1 && !details2 && !loading1 && !loading2 && (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
          <p className="text-gray-500 dark:text-gray-400">Select two Pokémon to compare them.</p>
        </div>
      )}
    </div>
  );
}
