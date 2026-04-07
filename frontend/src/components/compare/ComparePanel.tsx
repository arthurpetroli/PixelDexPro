import { ArrowLeftRight } from 'lucide-react';
import { TypeBadge } from '@/components/pokemon/TypeBadge';
import { StatBar } from '@/components/pokemon/StatBar';
import { formatPokemonName } from '@/utils/pokemon';
import type { PokemonDetails } from '@/types';
import { cn } from '@/utils/helpers';

interface ComparePanelProps {
  pokemon1: PokemonDetails | null;
  pokemon2: PokemonDetails | null;
  statComparison?: Record<string, any>;
  onSwap?: () => void;
  className?: string;
}

export function ComparePanel({
  pokemon1,
  pokemon2,
  statComparison,
  onSwap,
  className,
}: ComparePanelProps) {
  if (!pokemon1 || !pokemon2) {
    return (
      <div className={cn('text-center py-12 bg-gray-50 rounded-xl', className)}>
        <ArrowLeftRight className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-700 mb-2">
          Select Two Pokémon to Compare
        </h3>
        <p className="text-gray-500 max-w-md mx-auto">
          Choose two Pokémon from the search to see a detailed side-by-side comparison
          of their stats, types, and abilities.
        </p>
      </div>
    );
  }

  const stats = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'];

  return (
    <div className={cn('space-y-6', className)}>
      {/* Header */}
      <div className="grid grid-cols-3 gap-4 items-center">
        <PokemonHeader pokemon={pokemon1} />
        <div className="flex justify-center">
          {onSwap && (
            <button
              onClick={onSwap}
              className="p-3 bg-blue-100 text-blue-600 rounded-full hover:bg-blue-200 transition-colors"
            >
              <ArrowLeftRight className="w-6 h-6" />
            </button>
          )}
        </div>
        <PokemonHeader pokemon={pokemon2} align="right" />
      </div>

      {/* Stats Comparison */}
      <div className="bg-white rounded-lg p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Stats Comparison</h3>
        <div className="space-y-4">
          {stats.map((stat) => {
            const value1 = pokemon1.stats?.[stat as keyof typeof pokemon1.stats] || 0;
            const value2 = pokemon2.stats?.[stat as keyof typeof pokemon2.stats] || 0;
            const winner = value1 > value2 ? 1 : value2 > value1 ? 2 : 0;

            return (
              <div key={stat} className="space-y-1">
                <div className="flex justify-between text-sm text-gray-600">
                  <span className={winner === 1 ? 'font-semibold text-green-600' : ''}>
                    {value1}
                  </span>
                  <span className="capitalize">{stat.replace('_', ' ')}</span>
                  <span className={winner === 2 ? 'font-semibold text-green-600' : ''}>
                    {value2}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <StatBar value={value1} maxValue={255} variant={winner === 1 ? 'success' : 'default'} />
                  <StatBar value={value2} maxValue={255} variant={winner === 2 ? 'success' : 'default'} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Type Comparison */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Types</h4>
          <div className="flex gap-2">
            {pokemon1.types.map((t) => (
              <TypeBadge key={t.type.name} type={t.type.name} size="md" />
            ))}
          </div>
        </div>
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Types</h4>
          <div className="flex gap-2">
            {pokemon2.types.map((t) => (
              <TypeBadge key={t.type.name} type={t.type.name} size="md" />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function PokemonHeader({
  pokemon,
  align = 'left',
}: {
  pokemon: PokemonDetails;
  align?: 'left' | 'right';
}) {
  return (
    <div className={cn('flex flex-col items-center', align === 'right' && 'items-end')}>
      <img
        src={pokemon.sprite_official_url || pokemon.sprite_url || '/placeholder-pokemon.png'}
        alt={pokemon.name}
        className="w-24 h-24 object-contain mb-2"
      />
      <h3 className="text-xl font-bold text-gray-800">
        {formatPokemonName(pokemon.name)}
      </h3>
      <p className="text-sm text-gray-500">#{pokemon.pokedex_number}</p>
    </div>
  );
}
